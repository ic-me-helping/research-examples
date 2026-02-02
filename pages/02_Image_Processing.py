import streamlit as st
import os
import sys

global BASE_DIR, RESEARCH_DIR

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESEARCH_DIR = os.path.join(BASE_DIR, "Research")
sys.path.append(RESEARCH_DIR)
from IMG_Processing import image_location

# Upload image
# Create a temporary directory if needed
TEMP_DIR = "temp_uploads"
if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)

uploaded_image = st.file_uploader("Upload an image for metadata processing", type=["png", "jpg", "jpeg"], accept_multiple_files=False)


# Display GPS Coordinates
if uploaded_image:
    temp_file_path = os.path.join(TEMP_DIR, uploaded_image.name)
    
    with open(temp_file_path, "wb") as f:
        f.write(uploaded_image.getbuffer())
    
    st.image(temp_file_path, caption="Uploaded Image")

    # Extract GPS data
    gps_data = image_location(temp_file_path)
    st.subheader("Extracted GPS Data:")
    st.json(gps_data)

    # Delete temporary file
    os.remove(temp_file_path)