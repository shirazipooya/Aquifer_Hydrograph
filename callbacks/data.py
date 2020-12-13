import base64
import io
import pandas as pd
import numpy as np
import json
import geopandas as gpd


# Function for Parses *.csv or *.xlsx Files
def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    if 'csv' in filename:
        # Assume That The User Uploaded a CSV File
        return pd.read_csv(
            io.StringIO(decoded.decode('utf-8'))
        )
    elif 'xlsx' in filename:
        # Assume That The User Uploaded An EXCEL File
        return pd.read_excel(
            io.BytesIO(decoded)
        )

# Function for Read AreaStudy Shapefile
def read_shapfile_AreaStudy(
        file_path="./assets/data/ShapeFiles/AreaStudy/AreaStudy.shp",
        mah_code = [4740]
):
    geodf = gpd.read_file(file_path)
    geodf = geodf[geodf['Mah_code'].isin(mah_code)]
    j_file = json.loads(geodf.to_json())

    for feature in j_file["features"]:
        feature['id'] = feature['properties']['Mah_code']

    return geodf, j_file
