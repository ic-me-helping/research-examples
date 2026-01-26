import requests


# Scientific Functions
## Creates NASA Power API URL and retrieves data
def nasa_power_api(parameters, user_input=False):
    
    # Allow users to input parameters through terminal
    if user_input:
        start = input("Start Date (YYYYMMDD):")
        end = input("End Date (YYYYMMDD):")
        latitude = input("Latitude (Decimal Degrees):")
        longitude = input("Longitude (Deicmal Degress)")
        community = input("Community (AG, SB, etc.):")
        parameter = input("Parameter (T2M, WS2M, etc.):")
        format_string = input("Format (json, csv):")
        units = input("Units (metric, imperial):")
        header = input("Header (true, false):")
        time_standard = input("Time Standard (utc, lst):")
        site_elevation = input("Site Elevation (Meters):")
        wind_elevation = input("Wind Elevation (Meters, Requires Wind Surface in Next Prompt):")
        wind_surface = input("Wind Surface (Required with Wind Elevation):")
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

    # Establish empty URL Request
    url = []
    
    # Load API base URL into empty URL
    base_url = "https://power.larc.nasa.gov/api/temporal/hourly/point?"
    url.append(base_url)
    
    # Load parameters into URL after base URL
    for param in parameters:
        if parameters[param] != "":
            url.append(f"&{param}={parameters[param]}")
    
    url[1] = url[1].replace("&", "") # Adds the first parameter without an & at the start
    url = "".join(url)
    print(url)
    response = requests.get(url)
    json_data = response.json()
    return json_data

if __name__ == "__main__":
    start = 20260115
    end = 20260121
    latitude = 45.4201
    longitude = -75.7003
    community = "re"
    parameter = "WD50M"
    format_string = "json"
    units = "metric"
    header = "true"
    time_standard = "lst"
    site_elevation = "0"
    wind_elevation = ""
    wind_surface = ""

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
    data = nasa_power_api(parameters)
    
    nasa_parameter_data = data["properties"]["parameter"]

    nasa_header_info = data["header"]
    nasa_parameter_info = data["parameters"]
    for param_data in nasa_parameter_info:
        param = nasa_parameter_info[param_data]
        param_tag = param_data
        param_name = param["longname"]
        param_units = param["units"]
        print(f"Parameter Tag: {param_tag}")
        print(f"Parameter Name: {param_name}")
        print(f"Parameter Units: {param_units}")

    for param in nasa_parameter_data:
        for date in nasa_parameter_data[param]:
            param_value = nasa_parameter_data[param][date]
            value_data = f"Date: {date}, Value: {param_value} {nasa_parameter_info[param]["units"]}"
            print(value_data)