from server import app
from callbacks.data import *

import pandas as pd

import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import plotly.express as px

No_Matching_Data_Found_Fig = {
    "layout": {
        "xaxis": {"visible": False},
        "yaxis": {"visible": False},
        "annotations": [
            {
                "text": "No matching data found",
                "xref": "paper",
                "yref": "paper",
                "showarrow": False,
                "font": {"size": 24}
            }
        ]
    }
}



# Update Upload Button Input Data
@app.callback(Output('uploadButtonInfo_rawData', 'children'),
              Output('uploadButtonInfo_rawData', 'color'),
              Input('uploadButton_rawData', 'contents'),
              State('uploadButton_rawData', 'filename'))
def uploadButtonInfo_rawData_update(contents, filename):
    if contents is None:
        return "فایلی انتخاب نشده است!", 'danger'
    return filename, 'success'


# Data Generator
@app.callback(Output('infoData', 'children'),
              Output('rawData', 'children'),
              Input('uploadButton_rawData', 'contents'),
              State('uploadButton_rawData', 'filename'))
def data_generator(contents, filename):
    if contents is None:
        return 'No Data', 'No Data'

    # raw_data - Dictionary Format
    raw_data = read_excel_data(contents, filename)

    data = data_cleansing(
        well_info_data_all=raw_data['Info'],
        dtw_data_all=raw_data['Depth_To_Water'],
        thiessen_data_all=raw_data['Thiessen'],
        sc_data_all=raw_data['Storage_Coefficient']
    )

    return raw_data['Info'].to_json(date_format='iso', orient='split'), data.to_json(date_format='iso', orient='split')


# Update Card - Sidebar
@app.callback(Output('number_aquifer_sidebar_tab1', 'children'),
              Output('number_well_sidebar_tab1', 'children'),
              Input('infoData', 'children'))
def number_aquifer_sidebar_tab1(infoData):
    if infoData is None or infoData == 'No Data':
        return 'داده ای پیدا نشد', 'داده ای پیدا نشد'
    data = pd.read_json(infoData, orient='split')
    aquifers = list(data['کد محدوده مطالعاتی'].unique())
    wells = list(data['نام چاه'].unique())

    return f'{len(aquifers)} عدد', f'{len(wells)} عدد'




# Update Content 1 - Map
@app.callback(Output('content1Tab1', 'figure'),
              Input('infoData', 'children'))
def update_content1Tab1(infoData):
    if infoData is None or infoData == 'No Data':
        return No_Matching_Data_Found_Fig
    data = pd.read_json(infoData, orient='split')
    mah_code = list(data['کد محدوده مطالعاتی'].unique())
    geodf, j_file = read_shapfile_AreaStudy(os_moteval='خراسان رضوي', mah_code=mah_code)

    fig = px.choropleth_mapbox(data_frame=geodf,
                               geojson=j_file,
                               locations='Mah_code',
                               opacity=0.3)

    for mc in mah_code:
        df = data[data['کد محدوده مطالعاتی'] == mc]

        fig.add_trace(
            go.Scattermapbox(
                lat=df.Y_Decimal,
                lon=df.X_Decimal,
                mode='markers',
                marker=go.scattermapbox.Marker(size=9),
                text=df['نام چاه']
            )
        )

    fig.update_layout(
        mapbox = {'style': "stamen-terrain",
                  'center': {'lon': 58.8,
                             'lat': 35.9 },
                  'zoom': 5.5},
        showlegend = False,
        hovermode='closest',
        margin = {'l':0, 'r':0, 'b':0, 't':0}
    )

    return fig



# Update Content 2 - Map
@app.callback(Output('content2Tab1', 'figure'),
              Input('infoData', 'children'))
def update_content2Tab1(infoData):
    if infoData == 'No Data':
        return No_Matching_Data_Found_Fig

    geodf, j_file = read_shapfile_AreaStudy(os_moteval='خراسان رضوي', mah_code=None)
    fig = px.choropleth_mapbox(data_frame=geodf,
                               geojson=j_file,
                               locations='Mah_code',
                               opacity=0.6,
                               hover_data={'Mah_Name': True,
                                           'Mah_code': True,
                                           'os_moteval': True,
                                           'Area': ':.2f'})
    fig.update_layout(
        mapbox = {'style': "stamen-terrain",
                  'center': {'lon': 58.8,
                             'lat': 35.9},
                  'zoom': 5.5},
        showlegend = False,
        hovermode='closest',
        margin = {'l':0, 'r':0, 'b':0, 't':0}
    )

    fig.update_layout(
        hoverlabel=dict(
            bgcolor="white",
            font_size=14,
            font_family="B Koodak"
        )
    )

    return fig






# Update Content 2 - Table
@app.callback(Output('content3Tab1', 'data'),
              Output('content3Tab1', 'columns'),
              Input('infoData', 'children'))
def update_content3Tab1(infoData):
    if infoData is None or infoData == 'No Data':
        return [{}], []
    data = pd.read_json(infoData, orient='split')
    return data.to_dict('records'), [{"name": i, "id": i} for i in data.columns]