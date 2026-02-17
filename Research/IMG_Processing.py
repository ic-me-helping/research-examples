from PIL import ExifTags, Image

def image_location(img_path):
    """
    Validation through Data Ingestion.
    Extracts spatial metadata from site documentation to visualize conditions with precision.
    """
    img = Image.open(img_path)
    exif_reader = { ExifTags.TAGS[k]: v for k, v in img._getexif().items() if k in ExifTags.TAGS }

    GPS_NS = exif_reader['GPSInfo'][1]
    NS_list = exif_reader['GPSInfo'][2]
    NS_DMS = f"{NS_list[0]} Degs, {NS_list[1]} Mins, {NS_list[2]} Secs"
    NS_decimal = float(NS_list[0]) + float(NS_list[1])/60 + float(NS_list[2])/3600
    
    if GPS_NS == 'S':
        NS_decimal = -NS_decimal
    
    print(GPS_NS)
    print(NS_DMS)
    print(round(NS_decimal, 5))

    GPS_EW = exif_reader['GPSInfo'][3]
    EW_list = exif_reader['GPSInfo'][4]
    EW_DMS = f"{EW_list[0]} Degs, {EW_list[1]} Mins, {EW_list[2]} Secs"
    EW_decimal = float(EW_list[0]) + float(EW_list[1])/60 + float(EW_list[2])/3600
    
    if GPS_EW == 'W':
        EW_decimal = -EW_decimal
    
    print(GPS_EW)
    print(EW_DMS)
    print(round(EW_decimal, 5))

    data = {
        "Latitude": {
            "Direction": GPS_NS,
            "DMS": NS_DMS,
            "Decimal": NS_decimal
        },
        "Longitude": {
            "Direction": GPS_EW,
            "DMS": EW_DMS,
            "Decimal": EW_decimal
        }
    }
    
    return data