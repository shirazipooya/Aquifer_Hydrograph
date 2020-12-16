import base64
import io
import pandas as pd
import numpy as np
import json
import geopandas as gpd
from itertools import compress
from srtm import Srtm1HeightMapCollection
import assets.jalali as jalali
import statistics



# Function for Read AreaStudy Shapefile
def read_shapfile_AreaStudy(
        file_path = "./assets/data/ShapeFiles/AreaStudy/AreaStudy.shp",
        os_moteval = 'خراسان رضوي',
        mah_code = None
):
    if mah_code is not None:
        geodf = gpd.read_file(file_path, encoding='windows-1256')
        geodf = geodf[geodf['os_moteval'] == os_moteval]
        geodf = geodf[geodf['Mah_code'].isin(mah_code)]
        j_file = json.loads(geodf.to_json())

        for feature in j_file["features"]:
            feature['id'] = feature['properties']['Mah_code']

        return geodf, j_file
    else:
        geodf = gpd.read_file(file_path, encoding='windows-1256')
        geodf = geodf[geodf['os_moteval'] == os_moteval]
        j_file = json.loads(geodf.to_json())

        for feature in j_file["features"]:
            feature['id'] = feature['properties']['Mah_code']

        return geodf, j_file




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



# Get Data From File Input Tab - Excel File with Several Sheet
def read_excel_data(contents, filename):
    if 'xlsx' in filename:
        data = {}
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        xlsx_file = pd.ExcelFile(io.BytesIO(decoded))
        for sheet_name in xlsx_file.sheet_names:
            data[sheet_name] = xlsx_file.parse(sheet_name)
        return data



# Data Cleansing
def data_cleansing(well_info_data_all, dtw_data_all, thiessen_data_all, sc_data_all):
    result = pd.DataFrame()

    for aquifer in well_info_data_all['نام آبخوان'].unique():
        well_info_data = well_info_data_all[well_info_data_all['نام آبخوان'] == aquifer]
        dtw_data = dtw_data_all[dtw_data_all['نام آبخوان'] == aquifer]
        thiessen_data = thiessen_data_all[thiessen_data_all['نام آبخوان'] == aquifer]
        sc_data = sc_data_all[sc_data_all['نام آبخوان'] == aquifer]

        # Well Info Data:------------------------------------------------------
        Columns_Info = list(compress(well_info_data.columns.tolist(),
                                     list(map(lambda x: isinstance(x, str),
                                              well_info_data.columns.tolist()))))

        Well_Info = well_info_data[Columns_Info]

        Well_Info['نام آبخوان'] = Well_Info['نام آبخوان'].apply(lambda x: x.rstrip())
        Well_Info['نام چاه'] = Well_Info['نام چاه'].apply(lambda x: x.rstrip())

        # Depth to Water (DTW) Data:--------------------------------------------

        # Extract Dates From Columns Name
        id_vars = list(compress(dtw_data.columns.tolist(),
                                list(map(lambda x: isinstance(x, str),
                                         dtw_data.columns.tolist()))))

        dtw_data['نام آبخوان'] = dtw_data['نام آبخوان'].apply(lambda x: x.rstrip())
        dtw_data['نام چاه'] = dtw_data['نام چاه'].apply(lambda x: x.rstrip())

        # Convert DTW Data to Wide Format
        DTW_Wide = pd.melt(frame=dtw_data,
                           id_vars=id_vars,
                           var_name="Date",
                           value_name="Depth_To_Water").pivot(index='Date',
                                                              columns='کلاسه (کد شناسایی) چاه',
                                                              values='Depth_To_Water').reset_index()

        # Modify Columns Name
        DTW_Wide.columns = [col for col in DTW_Wide.columns]

        # Modified Date - Add Gregorian Date
        DTW_Wide["Date_Gregorian"] = list(map(lambda i: pd.to_datetime(i - 2, unit='D', origin='1900-01-01').date(),
                                              DTW_Wide["Date"]))

        # Modified Date - Add Persian Date
        DTW_Wide["Date_Persian"] = list(map(lambda i: jalali.Gregorian(i).persian_string(),
                                            DTW_Wide["Date_Gregorian"]))

        # Reorder Columns
        DTW_Wide = DTW_Wide.reindex(columns=(['Date', 'Date_Gregorian', 'Date_Persian'] + list(
            [a for a in DTW_Wide.columns if a not in ['Date', 'Date_Gregorian', 'Date_Persian']])))

        # Convert DTW_Wide Data Into A Tidy Format
        DTW = pd.melt(frame=DTW_Wide,
                      id_vars=['Date_Gregorian', 'Date', 'Date_Persian'],
                      value_name='Depth_To_Water',
                      var_name='ID').sort_values(['ID', 'Date_Gregorian']).drop('Date', axis=1)
        DTW = DTW[['ID', 'Date_Gregorian', 'Date_Persian', 'Depth_To_Water']]

        # Thiessen Weights Data:----------------------------------------------

        # Extract Dates From Columns Name
        id_vars = list(compress(thiessen_data.columns.tolist(),
                                list(map(lambda x: isinstance(x, str),
                                         thiessen_data.columns.tolist()))))

        thiessen_data['نام آبخوان'] = thiessen_data['نام آبخوان'].apply(lambda x: x.rstrip())
        thiessen_data['نام چاه'] = thiessen_data['نام چاه'].apply(lambda x: x.rstrip())

        # Convert Thiessen Data to Wide Format
        Thiessen_Wide = pd.melt(frame=thiessen_data,
                                id_vars=id_vars,
                                var_name="Date",
                                value_name="Area").pivot(index='Date',
                                                         columns='کلاسه (کد شناسایی) چاه',
                                                         values='Area').reset_index()

        # Modify Columns Name
        Thiessen_Wide.columns = [col for col in Thiessen_Wide.columns]

        # Modified Date - Add Gregorian Date
        Thiessen_Wide["Date_Gregorian"] = list(map(lambda i: pd.to_datetime(i - 2, unit='D', origin='1900-01-01').date(),
                                                   Thiessen_Wide["Date"]))

        # Modified Date - Add Persian Date
        Thiessen_Wide["Date_Persian"] = list(map(lambda i: jalali.Gregorian(i).persian_string(),
                                                 Thiessen_Wide["Date_Gregorian"]))

        # Reorder Columns
        Thiessen_Wide = Thiessen_Wide.reindex(columns=(['Date', 'Date_Gregorian', 'Date_Persian'] + list(
            [a for a in Thiessen_Wide.columns if a not in ['Date', 'Date_Gregorian', 'Date_Persian']])))

        # Convert DTW_Wide Data Into A Tidy Format
        Thiessen = pd.melt(frame=Thiessen_Wide,
                           id_vars=['Date_Gregorian', 'Date', 'Date_Persian'],
                           value_name='Area',
                           var_name='ID').sort_values(['ID', 'Date_Gregorian']).drop('Date', axis=1)
        Thiessen = Thiessen[['ID', 'Date_Gregorian', 'Date_Persian', 'Area']]

        # Sum Thiessen for Each Month (Area Aquifer)
        Thiessen = pd.merge(left=Thiessen,
                            right=Thiessen.groupby(by='Date_Gregorian').sum().reset_index().rename(
                                columns={'Area': 'Aquifer_Area'}),
                            how='outer',
                            on='Date_Gregorian').sort_values(['ID', 'Date_Gregorian'])

        # Storage Coefficient Data:------------------------------------------

        # Extract Dates From Columns Name
        id_vars = list(compress(sc_data.columns.tolist(),
                                list(map(lambda x: isinstance(x, str),
                                         sc_data.columns.tolist()))))

        sc_data['نام آبخوان'] = sc_data['نام آبخوان'].apply(lambda x: x.rstrip())
        sc_data['نام چاه'] = sc_data['نام چاه'].apply(lambda x: x.rstrip())

        # Convert Storage Coefficient Data to Wide Format
        Storage_Coefficient_Wide = pd.melt(frame=sc_data,
                                           id_vars=id_vars,
                                           var_name="Date",
                                           value_name="Storage_Coefficient").pivot(index='Date',
                                                                                   columns='کلاسه (کد شناسایی) چاه',
                                                                                   values='Storage_Coefficient').reset_index()

        # Modify Columns Name
        Storage_Coefficient_Wide.columns = [col for col in Storage_Coefficient_Wide.columns]

        # Modified Date - Add Gregorian Date
        Storage_Coefficient_Wide["Date_Gregorian"] = list(
            map(lambda i: pd.to_datetime(i - 2, unit='D', origin='1900-01-01').date(),
                Storage_Coefficient_Wide["Date"]))

        # Modified Date - Add Persian Date
        Storage_Coefficient_Wide["Date_Persian"] = list(map(lambda i: jalali.Gregorian(i).persian_string(),
                                                            Storage_Coefficient_Wide["Date_Gregorian"]))

        # Reorder Columns
        Storage_Coefficient_Wide = Storage_Coefficient_Wide.reindex(columns=(
                    ['Date', 'Date_Gregorian', 'Date_Persian'] + list(
                [a for a in Storage_Coefficient_Wide.columns if a not in ['Date', 'Date_Gregorian', 'Date_Persian']])))

        # Convert Storage_Coefficient_Wide Data Into A Tidy Format
        Storage_Coefficient = pd.melt(frame=Storage_Coefficient_Wide,
                                      id_vars=['Date_Gregorian', 'Date', 'Date_Persian'],
                                      value_name='Storage_Coefficient',
                                      var_name='ID').sort_values(['ID', 'Date_Gregorian']).drop('Date', axis=1)
        Storage_Coefficient = Storage_Coefficient[['ID', 'Date_Gregorian', 'Date_Persian', 'Storage_Coefficient']]

        # Surface Elevation of Observation Well:----------------------------
        # Extract Surface Elevation of Observation Well From NASA Shuttle Radar Topography Mission (SRTM) Version 3.0
        srtm1_data = Srtm1HeightMapCollection()

        Well_Info["G.S.L_DEM_SRTM1"] = list(
            map(lambda LonLat: srtm1_data.get_altitude(longitude=LonLat[0], latitude=LonLat[1]),
                zip(Well_Info.X_Decimal, Well_Info.Y_Decimal)))

        Elevation = Well_Info[['کلاسه (کد شناسایی) چاه', 'G.S.L_M.S.L', 'Final Elevation', 'G.S.L_DEM_SRTM1']]
        # Elevation = Well_Info[['کلاسه (کد شناسایی) چاه', 'G.S.L_M.S.L', 'Final Elevation']]

        Elevation.columns = ['ID', 'MSL_Elevation', 'Final_Elevation', 'Elevation']
        # Elevation.columns = ['ID', 'MSL_Elevation', 'Final_Elevation']

        # Combine Data:-----------------------------------------------------
        data = pd.merge(left=DTW,
                        right=Elevation,
                        how='outer',
                        on=['ID']).merge(right=Thiessen,
                                         how='outer',
                                         on=['ID', 'Date_Gregorian', 'Date_Persian']).merge(right=Storage_Coefficient,
                                                                                            how='outer',
                                                                                            on=['ID', 'Date_Gregorian',
                                                                                                'Date_Persian']).sort_values(
            ['ID', 'Date_Gregorian'])

        # Calculate Aquifer Storage Coefficient:------------------------------------
        data['Unit_Aquifer_Storage_Coefficient'] = (data['Storage_Coefficient'] * data['Area']) / data['Aquifer_Area']

        # Sum Aquifer Storage Coefficient for Each Month (Aquifer Storage Coefficient)
        df = data.groupby(by=['Date_Gregorian', 'Date_Persian']).sum().reset_index()[
            ['Date_Gregorian', 'Date_Persian', 'Unit_Aquifer_Storage_Coefficient']].rename(
            columns={'Unit_Aquifer_Storage_Coefficient': 'Aquifer_Storage_Coefficient'})

        data = data.merge(right=df,
                          how='outer',
                          on=['Date_Gregorian', 'Date_Persian']).sort_values(['ID', 'Date_Gregorian'])

        #  Calculate Well Head:----------------------------------------------
        data['Well_Head'] = data['Final_Elevation'] - data['Depth_To_Water']

        # Calculate Aquifer Head:--------------------------------------------
        data['Unit_Aquifer_Head'] = (data['Well_Head'] * data['Area']) / data['Aquifer_Area']

        # Sum Units Aquifer Head for Each Month (Aquifer_Head)
        df = data.groupby(by=['Date_Gregorian', 'Date_Persian']).sum().reset_index()[
            ['Date_Gregorian', 'Date_Persian', 'Unit_Aquifer_Head']].rename(columns={'Unit_Aquifer_Head': 'Aquifer_Head'})

        data = data.merge(right=df,
                          how='outer',
                          on=['Date_Gregorian', 'Date_Persian']).sort_values(['ID', 'Date_Gregorian'])

        df = data[['Date_Gregorian', 'Date_Persian', 'Well_Head']].groupby(by=['Date_Gregorian', 'Date_Persian']).agg({
            'Well_Head': [statistics.mean, statistics.geometric_mean, statistics.harmonic_mean]
        }).reset_index()

        df.columns = [col for col in df.columns]

        df.columns = ['Date_Gregorian', 'Date_Persian', 'Aquifer_Head_Arithmetic_Mean', 'Aquifer_Head_Geometric_Mean', 'Aquifer_Head_Harmonic_Mean']

        data = data.merge(right=df,
                          how='outer',
                          on=['Date_Gregorian', 'Date_Persian']).sort_values(['ID', 'Date_Gregorian'])

        # Add Name Well
        data = data.merge(right=Well_Info[
            ['نام محدوده مطالعاتی', 'نام آبخوان', 'نام چاه', 'کلاسه (کد شناسایی) چاه', 'X_UTM', 'Y_UTM', 'X_Decimal',
             'Y_Decimal']],
                          how='outer',
                          left_on=['ID'],
                          right_on=['کلاسه (کد شناسایی) چاه']).sort_values(['ID', 'Date_Gregorian'])


        result = result.append(data)

    return result