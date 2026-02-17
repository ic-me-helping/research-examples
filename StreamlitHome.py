import streamlit as st

# --- HUB CONFIGURATION ---
st.set_page_config(
    page_title="IC.ME | Engineering & Compliance Hub", 
    layout="wide"
)

# --- BRANDING & VISION ---
st.title("IC.ME | Engineering & Compliance Hub")

st.markdown("""
### Strategic Data Bridging
This platform serves as the bridge between static project storage and dynamic representation. 
Following the *Engineering Approach to Compliance*, we replace manual oversight with 
engineered validation points. Our methodology ensures that tedious, disconnected data is 
transformed into normalized, GIS-aligned structures for high stakes decision making.
""")

st.info("**The Mirror Model:** See yourself in the data and manage your own predictions.")

st.divider()

# --- SERVICE MATRIX ---
col1, col2, col3 = st.columns(3, gap="large")

with col1:
    st.subheader("Environmental Modeling")
    st.write("""
    **Service E:** Utilizing open-source geospatial data (NASA Power) to understand 
    open-field conditions. This module anchors public data to GPS-specific readings 
    for risk assessment and LEED consideration.
    """)
    if st.button("Launch NASA Query", use_container_width=True):
        st.switch_page("pages/01_NASA_Power_Data_Query.py")

with col2:
    st.subheader("Image Validation")
    st.write("""
    **Validation through Ingestion:** Extracting metadata and spatial information 
    from raw site documentation. We visualize site conditions with precision by 
    turning static images into GIS-anchored data points.
    """)
    if st.button("Launch Image Processor", use_container_width=True):
        st.switch_page("pages/02_Image_Processing.py")

with col3:
    st.subheader("Audio Matrix")
    st.write("""
    **Compliance Path Determination:** An 'Altruistic Logic' engine that manages 
    on-site communication. It ensures stationary priority while maintaining 
    constant safety channel compliance through logic gates.
    """)
    if st.button("View Audio Logic", use_container_width=True):
        st.switch_page("pages/03_Audio_Matrix.py")

st.divider()

# --- ORGANIZATIONAL PRINCIPLES ---
st.markdown("### Guiding Principles")
p1, p2 = st.columns(2)

with p1:
    st.markdown("**Credit-less Logic**")
    st.caption("Prototypes and logic are encouraged to be used, adapted, and owned by the results they produce.")

with p2:
    st.markdown("**Altruistic Logic**")
    st.caption("Compliance prioritizes safety and accountability, ensuring high-stakes specifications are met automatically.")

st.sidebar.success("Select a Compliance Path above.")