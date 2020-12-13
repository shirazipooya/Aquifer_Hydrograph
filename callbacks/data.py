import base64
import io
import pandas as pd
import numpy as np


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



