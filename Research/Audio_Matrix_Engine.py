import sounddevice as sd
import numpy as np
import os

# --- COMPLIANCE CONFIGURATION ---
AGG_DEVICE_NAME = "AutoDucker"
OUT_DEVICE_NAME = "BlackHole 2ch"
SAMPLE_RATE = 48000 
BLOCK_SIZE = 1024 

# --- PATH DETERMINATION PARAMETERS ---
THRESHOLD_DB = -35.0   
ATTACK_TIME = 0.05     
RELEASE_TIME = 0.5     

# --- UI CONSTANTS ---
GREEN, YELLOW, RED, BLUE = "\033[92m", "\033[93m", "\033[91m", "\033[94m"
CYAN, WHITE, RESET, BOLD = "\033[96m", "\033[97m", "\033[0m", "\033[1m"
HIDE_CURSOR, SHOW_CURSOR, TOP_LEFT = "\033[?25l", "\033[?25h", "\033[H"

class Microphone:
    """
    Validation through Data Ingestion: Represents a site-specific audio input.
    """
    def __init__(self, name, channel_index, location="FIELD", gain=1.0):
        self.name = name
        self.index = channel_index
        self.location = location  
        self.gain = gain
        self.current_rms = 0.0

    def get_signal(self, indata):
        if self.index >= indata.shape[1]: return np.zeros(indata.shape[0])
        signal = indata[:, self.index].flatten() * self.gain
        self.current_rms = np.sqrt(np.mean(signal**2))
        return signal

    def get_meter(self, threshold_lin, width=20):
        val = min(self.current_rms * 10, 1.0)
        level = int(val * width)
        if self.location == "SAFETY": color = RED
        elif self.location == "DESK": color = GREEN if self.current_rms > threshold_lin else BLUE
        else: color = CYAN if self.current_rms > 0.01 else WHITE
        bar = "█" * level + "░" * (width - level)
        return f"{color}{bar}{RESET}"

class AudioEngine:
    """
    The main processing engine for Compliance Path Determination.
    """
    def __init__(self):
        self.fader = 0.0
        self.mics = [
            Microphone("Main Station", 0, location="DESK", gain=6.0),
            Microphone("Wireless Field", 2, location="FIELD", gain=3.0)
        ]
        
        self.threshold_lin = 10.0 ** (THRESHOLD_DB / 20.0)
        self.lp_attack = 1.0 - np.exp(-1.0 / (SAMPLE_RATE * ATTACK_TIME / BLOCK_SIZE))
        self.lp_release = 1.0 - np.exp(-1.0 / (SAMPLE_RATE * RELEASE_TIME / BLOCK_SIZE))

    def process(self, indata, outdata, frames, time, status):
        # Data Sanitization and Bus Assignment
        stat_sigs, wire_sigs, safe_sigs = [], [], []
        max_stat_rms = 0.0

        for mic in self.mics:
            sig = mic.get_signal(indata)
            if mic.location == "DESK":
                stat_sigs.append(sig)
                max_stat_rms = max(max_stat_rms, mic.current_rms)
            elif mic.location == "SAFETY":
                safe_sigs.append(sig)
            else:
                wire_sigs.append(sig)

        # Altruistic Logic Gate: Stationary Priority
        target = 1.0 if max_stat_rms > self.threshold_lin else 0.0
        alpha = self.lp_attack if target > self.fader else self.lp_release
        self.fader += (target - self.fader) * alpha
        self.fader = np.clip(self.fader, 0.0, 1.0)

        def smart_sum(signals):
            if not signals: return np.zeros(frames)
            rms_values = [np.sqrt(np.mean(s**2)) for s in signals]
            leader_idx = np.argmax(rms_values)
            combined = np.zeros(frames)
            for i, s in enumerate(signals):
                weight = 1.0 if i == leader_idx else 0.4
                combined += s * weight
            return combined

        stat_bus = smart_sum(stat_sigs)
        wire_bus = smart_sum(wire_sigs)
        safe_bus = smart_sum(safe_sigs)

        # Summation and Safety Bypass
        gain_stat = self.fader
        gain_wire = (1.0 - self.fader)**2 
        mixed = (stat_bus * gain_stat) + (wire_bus * gain_wire)
        mixed += safe_bus # Constant compliance path
        
        mixed = np.clip(mixed, -0.9, 0.9) 

        outdata[:, 0] = mixed
        outdata[:, 1] = mixed
        self.render_dashboard()

    def render_dashboard(self):
        out = f"{TOP_LEFT}{YELLOW}{BOLD}=== IC.ME Matrix Hub ==={RESET}\n"
        out += f"{'UNIT':<15} | {'LOCATION':<10} | {'SIGNAL LEVEL':<20}\n"
        out += "-" * 55 + "\n"

        for mic in self.mics:
            threshold = self.threshold_lin if mic.location == "DESK" else 0.01
            meter = mic.get_meter(threshold)
            out += f"{mic.name:15} | {mic.location:10} | {meter}\n"

        mode = f"{RED}STATIONARY PRIORITY{RESET}" if self.fader > 0.5 else f"{BLUE}FIELD ACTIVE{RESET}"
        out += f"\n{BOLD}MATRIX FADER: {self.fader:.2f} | STATUS: {mode}{RESET}\n"
        print(out, end="")

if __name__ == "__main__":
    engine = AudioEngine()
    all_indices = [m.index for m in engine.mics]
    total_ch = max(all_indices) + 1 if all_indices else 1
    os.system('clear' if os.name == 'posix' else 'cls')
    print(HIDE_CURSOR)
    try:
        with sd.Stream(device=(AGG_DEVICE_NAME, OUT_DEVICE_NAME),
                       samplerate=SAMPLE_RATE, blocksize=BLOCK_SIZE,
                       channels=(total_ch, 2), callback=engine.process):
            while True: sd.sleep(1000)
    except KeyboardInterrupt:
        print(f"\n{SHOW_CURSOR}{RED}Matrix Engine Offline.{RESET}")