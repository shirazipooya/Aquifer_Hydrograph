from server import app
from callbacks.data import *

import pandas as pd

import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go

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


# Update Upload Button Info - Well Info
@app.callback(Output('uploadButtonInfo_wellInfo', 'children'),
              Output('uploadButtonInfo_wellInfo', 'color'),
              Input('uploadButton_wellInfo', 'contents'),
              State('uploadButton_wellInfo', 'filename'))
def uploadButtonInfo_wellInfo_update(contents, filename):
    if contents is None:
        return "فایلی انتخاب نشده است!", 'danger'
    return filename, 'success'



# Update Upload Button Info - Data
@app.callback(Output('uploadButtonInfo_data', 'children'),
              Output('uploadButtonInfo_data', 'color'),
              Input('uploadButton_data', 'contents'),
              State('uploadButton_data', 'filename'))
def uploadButtonInfo_data_update(contents, filename):
    if contents is None:
        return "فایلی انتخاب نشده است!", 'danger'
    return filename, 'success '



# Update Content 1 - Map
@app.callback(Output('content1Tab1', 'figure'),
              Input('uploadButton_wellInfo', 'contents'),
              State('uploadButton_wellInfo', 'filename'))
def update_content1Tab1(contents, filename):
    if contents is None:
        return No_Matching_Data_Found_Fig
    data = parse_contents(contents, filename)
    fig = go.Figure(
        go.Scattermapbox(
            lat=data.Y_Decimal,
            lon=data.X_Decimal,
            mode='markers',
            marker=go.scattermapbox.Marker(size=9),
            text=data['نام چاه']
        )
    )
    fig.update_layout(
        mapbox = {'style': "stamen-terrain",
                  'center': {'lon': data.X_Decimal[30],
                             'lat': data.Y_Decimal[30] },
                  'zoom': 8},
        showlegend = False,
        hovermode='closest',
        margin = {'l':0, 'r':0, 'b':0, 't':0})
    return fig



# Update Content 2 - Map
@app.callback(Output('content2Tab1', 'figure'),
              Input('uploadButton_wellInfo', 'contents'),
              State('uploadButton_wellInfo', 'filename'))
def update_content2Tab1(contents, filename):
    if contents is None:
        return No_Matching_Data_Found_Fig
    return No_Matching_Data_Found_Fig



# Update Content 2 - Table
@app.callback(Output('content3Tab1', 'data'),
              Output('content3Tab1', 'columns'),
              Input('uploadButton_wellInfo', 'contents'),
              State('uploadButton_wellInfo', 'filename'))
def update_content3Tab1(contents, filename):
    if contents is None:
        return [{}], []
    data = parse_contents(contents, filename)
    return data.to_dict('records'), [{"name": i, "id": i} for i in data.columns]