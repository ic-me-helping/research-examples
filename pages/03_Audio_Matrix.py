import streamlit as st
import numpy as np

st.set_page_config(page_title="Audio Matrix | IC.ME", layout="wide")

st.title("Compliance Bridge: Audio Matrix Controller")

st.markdown("""
### Altruistic Logic Implementation
This tool manages on-site communication by prioritizing 'Stationary' (Desk) inputs over 'Field' (Wireless) inputs. 
Following the principle of Altruistic Logic, the **Safety** channel is never ducked, ensuring critical information 
always reaches the final mix.
""")

# Logic Simulation
st.header("Logic Gate Simulation")
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Stationary Input")
    st_level = st.slider("Desk Mic Level (dB)", -60, 0, -45)
    st.info("Trigger threshold: -35.0 dB")

with col2:
    st.subheader("Field Input")
    field_level = st.slider("Wireless Headset Level (dB)", -60, 0, -10)

with col3:
    st.subheader("Resulting Mix")
    # Simulation of the logic
    is_ducking = st_level > -35.0
    status = "STATIONARY PRIORITY" if is_ducking else "FIELD ACTIVE"
    color = "red" if is_ducking else "blue"
    st.markdown(f"**Current Path:** :{color}[{status}]")

st.divider()

st.markdown("""
### Local Implementation
The live audio engine requires direct hardware access. To implement this on-site with your wireless headsets 
and stationary microphones, download the engine from the repository and run it locally.
""")

with st.expander("View Engineering Logic (Local Script)"):
    st.code("""
# IC.ME Audio Matrix Controller
# Strategic Priority Logic: Stationary > Field (Safety = Constant)

import sounddevice as sd
import numpy as np

# Config
AGG_DEVICE_NAME = "AutoDucker"
OUT_DEVICE_NAME = "BlackHole 2ch"

# Logic Thresholds
THRESHOLD_DB = -35.0   
ATTACK_TIME = 0.05     
RELEASE_TIME = 0.5     

# [The rest of the cleaned AudioEngine class follows...]
    """, language="python")

st.write("For custom logic gate implementation or VDC/IT SOP development, [reach out here.](https://ilyasclouse.me)")

# Footer Navigation
st.divider()
nav_col1, nav_col2, nav_col3 = st.columns(3)
with nav_col1:
    if st.button("*← Return to Engineering Hub"):
        st.switch_page("StreamlitHome.py")
with nav_col2:
    if st.button("← Bridge to NASA Power Query"):
        st.switch_page("pages/01_NASA_Power_Data_Query.py")
with nav_col3:
    if st.button("← Bridge to Image Processing"):
        st.switch_page("pages/02_Image_Processing.py")