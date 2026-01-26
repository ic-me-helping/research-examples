import streamlit as st
import pandas as pd
import os
import sys
import time
import geopandas as gpd
from shapely.geometry import Point

global debug, BASE_DIR, RESEARCH_DIR
debug = True
if st.sidebar.toggle("Debug Mode:"):
    debug = True
else:
    debug = False

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESEARCH_DIR = os.path.join(BASE_DIR, "Research")
sys.path.append(RESEARCH_DIR)
from NASA_Power_API import nasa_power_api
print(BASE_DIR)

## NASA Power API Parameters
start = st.date_input("Start Date (YYYYMMDD):", format="YYYY/MM/DD")
if start:
    start = str(start).replace("-", "")
    if debug: print(start)
end = st.date_input("End Date (YYYYMMDD):", format="YYYY/MM/DD")
if end:
    end = str(end).replace("-", "")
    if debug: print(end)
latitude = st.number_input("Latitude (Decimal Degrees):", format="%.4f")
if debug: print(latitude)
longitude = st.number_input("Longitude (Decimal Degrees):", format="%.4f")
if debug: print(longitude)
community = st.selectbox("Community:", options=["re"])
available_parameters = {
    "T2M": "Temperature at 2 Meters",
    "WD50M": "Wind Direction at 50 Meters"
}
if st.toggle("Parameter Input: Checkbox"):
    selected_parameters = []
    for param in available_parameters:
        parameter = st.checkbox(param)
        if parameter:
            selected_parameters.append(param)
    parameter = ",".join(selected_parameters)
else:
    parameter = st.text_input("Parameters comma-seperated (T2M, WS2M, etc.):")
if debug: print(parameter)
site_elevation = st.number_input("Site Elevation (Meters):", format="%.3f")
if debug: print(site_elevation)
wind_elevation = st.number_input("Wind Elevation (Meters, Requires Wind Surface if Elevation is Entered):", format="%.3f")
if wind_elevation:
    wind_surface = st.selectbox("Wind Surface:", options=[""])
    if debug: print(wind_elevation)
    if debug: print(wind_surface)
else:
    wind_elevation = ""
    wind_surface = ""
format_string = "json"
if debug: print(format_string)
units = st.radio("Units:", options=["metric", "imperial"])
if debug: print(units)
header = st.radio("Header:", options=["true", "false"])
if debug: print(header)
time_standard = st.radio("Time Standard:", options=["utc", "lst"])
if debug: print(time_standard)

if "api_data" not in st.session_state:
    st.session_state.api_data = None

class NASAPowerData:
    def __init__(self, parameters):
        self.parameters = parameters
        self.data = st.session_state.api_data 

    def fetch_data(self):
        fetched = nasa_power_api(parameters=self.parameters, user_input=False)
        if fetched and isinstance(fetched, dict):
            st.session_state.api_data = fetched
            self.data = fetched
            st.success("Data Retrieved Successfully!")
            if debug: print("Fetched data:", self.data)
        else:
            st.error("Failed to Retrieve Data from NASA Power API.")
            if isinstance(self.data, dict):
                error_code = self.data.get("error", {}).get("code", "Unknown Error")
                st.error(f"API Error Code: {error_code}")
            else:
                st.error("Unexpected data format received from API.")

    def process_data(self):
        if not self.data or not isinstance(self.data, dict):
            st.error("No valid data available. Please fetch data first.")
            if debug: print("Error: self.data is None or not a dictionary.")
            return

        if "parameters" not in self.data:
            st.error("The data does not contain the expected 'parameters' key.")
            if debug: print(f"Error: 'parameters' key not found in data: {self.data}")
            return

        nasa_parameter_info = self.data["parameters"]

        parameter_info_list = []
        for param_data in nasa_parameter_info:
            param = nasa_parameter_info[param_data]
            parameter_info_list.append({
                "Parameter Tag": param_data,
                "Parameter Name": param.get("longname", "Unknown"),
                "Parameter Units": param.get("units", "Unknown")
            })
        parameter_info_df = pd.DataFrame(parameter_info_list)
        st.dataframe(parameter_info_df, width="stretch")

    def process_parameter_values(self):
        if not self.data:
            st.error("No data available. Please fetch data first.")
            return

        nasa_parameter_data = self.data["properties"]["parameter"]
        nasa_parameter_info = self.data["parameters"]

        combined_geojson_data = []
        crs_options = {
            "WGS 84 (EPSG:4326)": "EPSG:4326"
        }
        selected_crs = st.sidebar.selectbox("Select Coordinate Reference System (CRS):", options=list(crs_options.keys()), index=0)
        selected_crs_code = crs_options[selected_crs]

        for param in nasa_parameter_data:
            parameter_values_list = []
            for date, value in nasa_parameter_data[param].items():
                try:
                    parsed_date = pd.to_datetime(date, format="%Y%m%d%H")
                except ValueError:
                    parsed_date = pd.to_datetime(date, format="%Y%m%d")

                parameter_values_list.append({
                    "Date": parsed_date,
                    "Value": value,
                    "Units": nasa_parameter_info[param]["units"]
                })

            parameter_values_df = pd.DataFrame(parameter_values_list)
            parameter_values_df["Date"] = parameter_values_df["Date"].dt.strftime("%Y-%m-%d %H:%M:%S")

            parameter_values_df["Latitude"] = self.parameters["latitude"]
            parameter_values_df["Longitude"] = self.parameters["longitude"]
            parameter_values_df["Parameter"] = param

            parameter_values_df["geometry"] = parameter_values_df.apply(
                lambda row: Point(row["Longitude"], row["Latitude"]), axis=1
            )

            gdf = gpd.GeoDataFrame(parameter_values_df, geometry="geometry", crs=selected_crs_code)

            st.sidebar.download_button(
                label=f"{param} GeoJSON",
                data=gdf.to_json(),
                file_name=f"{param}_data.geojson",
                mime="application/geo+json"
            )

            combined_geojson_data.append(gdf)

            parameter_values_df["geometry_wkt"] = parameter_values_df["geometry"].apply(lambda geom: geom.wkt if geom else None)

            display_df = parameter_values_df.drop(columns=["geometry"])

            st.dataframe(display_df, width="stretch")

        if combined_geojson_data:
            combined_gdf = gpd.GeoDataFrame(pd.concat(combined_geojson_data, ignore_index=True))
            st.sidebar.download_button(
                label="All Data as GeoJSON",
                data=combined_gdf.to_json(),
                file_name="all_parameters_data.geojson",
                mime="application/geo+json"
            )

parameters = {
    "start": start,
    "end": end,
    "latitude": latitude,
    "longitude": longitude,
    "community": community,
    "parameters": parameter,
    "format": format_string,
    "units": units,
    "header": header,
    "time-standard": time_standard,
    "site-elevation": site_elevation,
    "wind-elevation": wind_elevation,
    "wind-surface": wind_surface
}

nasa_power_api_instance = NASAPowerData(parameters=parameters)

if st.button("Get NASA Power Data"):
    nasa_power_api_instance.fetch_data()

if st.session_state.api_data is not None:
    nasa_power_api_instance.data = st.session_state.api_data
    nasa_power_api_instance.process_data()
    nasa_power_api_instance.process_parameter_values()
