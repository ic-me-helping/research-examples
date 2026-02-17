import streamlit as st
import os
import sys
import pandas as pd

# --- PATH CONFIGURATION ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESEARCH_DIR = os.path.join(BASE_DIR, "Research")
sys.path.append(RESEARCH_DIR)
from IMG_Processing import image_location

# --- PAGE SETUP ---
st.set_page_config(page_title="Image Metadata Ingestion | IC.ME", layout="wide")

# --- HEADER BLOCKS (NASA Power Style) ---
st.warning("This tool is a Metadata Extraction utility. It anchors site documentation to geospatial coordinates. For real-time critical safety decisions, ensure that the source hardware (mobile/camera) has been calibrated for GPS accuracy.")
st.info("Validation through Data Ingestion: This module extracts raw spatial information to visualize site conditions with precision.")

# --- UI PARAMETERS ---
st.title("Validation: Image Metadata Ingestion")

# Establish Row 1: Ingestion and Visualization
row1_col1, row1_col2 = st.columns(spec=[1, 1], border=True, gap="large")

with row1_col1:
    st.subheader("Data Ingestion")
    uploaded_image = st.file_uploader(
        "Upload site documentation for metadata processing", 
        type=["png", "jpg", "jpeg"], 
        accept_multiple_files=False
    )
    
    if uploaded_image:
        st.success("File Ingested.")
        # Store file temporarily for processing
        TEMP_DIR = "temp_uploads"
        if not os.path.exists(TEMP_DIR): os.makedirs(TEMP_DIR)
        temp_file_path = os.path.join(TEMP_DIR, uploaded_image.name)
        with open(temp_file_path, "wb") as f:
            f.write(uploaded_image.getbuffer())

with row1_col2:
    st.subheader("Source Visualization")
    if uploaded_image:
        st.image(uploaded_image, caption="Validation Source", use_container_width=True)
    else:
        st.write("Awaiting image ingestion...")

# Establish Row 2: Extracted Data Results
st.divider()
st.subheader("Extracted Spatial Validation Points")

if uploaded_image:
    try:
        # Extract GPS data via Engineering Logic
        gps_data = image_location(temp_file_path)
        
        # Display Metrics (Mirroring the 'High Level' data view)
        m_col1, m_col2, m_col3 = st.columns(3)
        
        lat = gps_data['Latitude']['Decimal']
        lon = gps_data['Longitude']['Decimal']
        
        m_col1.metric("Latitude", f"{lat:.5f}°")
        m_col2.metric("Longitude", f"{lon:.5f}°")
        m_col3.metric("Data Status", "Compliance Valid")

        # Table Display (NASA Power Style)
        # Convert GPS DMS to a simple dataframe for display
        display_data = {
            "Dimension": ["Latitude", "Longitude"],
            "Decimal Degrees": [lat, lon],
            "DMS Notation": [
                f"{gps_data['Latitude']['Direction']} {gps_data['Latitude']['DMS']}",
                f"{gps_data['Longitude']['Direction']} {gps_data['Longitude']['DMS']}"
            ]
        }
        df = pd.DataFrame(display_data)
        st.dataframe(df, use_container_width=True, hide_index=True)

        # JSON Metadata Bridge
        with st.expander("View Full Metadata Schema"):
            st.json(gps_data)

        # Sidebar Integration (NASA Power Style)
        st.sidebar.subheader("Compliance Actions")
        st.sidebar.download_button(
            label="Download Metadata as JSON",
            data=str(gps_data),
            file_name=f"metadata_{uploaded_image.name}.json",
            mime="application/json"
        )
        
    except Exception as e:
        st.error("Compliance Alert: Exif tags could not be validated. Ensure the source image contains GPS metadata.")
    
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
else:
    st.info("Ingest an image to determine the compliance path.")

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
    if st.button("→ Bridge to Audio Matrix Controller"):
        st.switch_page("pages/03_Audio_Matrix.py")