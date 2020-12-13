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

base_map = go.Figure(
    go.Scattermapbox(
        lat=[36.25],
        lon=[59.55],
        mode='markers',
        marker=go.scattermapbox.Marker(size=9),
        text='Mashhad'
    )
)

base_map.update_layout(
    mapbox = {'style': "stamen-terrain",
              'center': {'lon': 59.55,
                         'lat': 36.25},
              'zoom': 7},
    showlegend = False,
    hovermode='closest',
    margin = {'l':0, 'r':0, 'b':0, 't':0},
    autosize=False)



# Update Aquifer Select Dropdown - Sidebar
@app.callback(Output('aquifer_select_sidebar_tab2', 'options'),
              Input('uploadButton_wellInfo', 'contents'),
              State('uploadButton_wellInfo', 'filename'))
def update_aquifer_select_sidebar_tab2(contents, filename):
    if contents is None:
        return []
    data = parse_contents(contents, filename)
    return [{"label": col, "value": col} for col in data['نام آبخوان'].unique()]


# Update Well Select Dropdown - Sidebar
@app.callback(Output('well_select_sidebar_tab2', 'options'),
              Input('aquifer_select_sidebar_tab2', 'value'),
              Input('uploadButton_wellInfo', 'contents'),
              State('uploadButton_wellInfo', 'filename'))
def update_well_select_sidebar_tab2(aquifer, contents, filename):
    if contents is None or aquifer is None:
        return []
    data = parse_contents(contents, filename)
    data = data[data['نام آبخوان'] == aquifer]
    return [{"label": col, "value": col} for col in data['نام چاه'].unique()]



# Update Map Sidebar
@app.callback(Output('mapSidebarTab2', 'figure'),
              Input('aquifer_select_sidebar_tab2', 'value'),
              Input('well_select_sidebar_tab2', 'value'),
              Input('uploadButton_wellInfo', 'contents'),
              State('uploadButton_wellInfo', 'filename'))
def update_mapSidebarTab2(aquifer, wells, contents, filename):
    if contents is None or wells is None:
        return base_map
    data = parse_contents(contents, filename)
    data['نام آبخوان'] = data['نام آبخوان'].apply(lambda x: x.rstrip())
    data['نام چاه'] = data['نام چاه'].apply(lambda x: x.rstrip())

    data = data[data['نام آبخوان'] == aquifer]

    mah_code = list(data['کد محدوده مطالعاتی'].unique())
    geodf, j_file = read_shapfile_AreaStudy(mah_code=mah_code)

    fig = px.choropleth_mapbox(data_frame=geodf,
                               geojson=j_file,
                               locations='Mah_code',
                               opacity=0.4)

    fig.add_trace(
        go.Scattermapbox(
            lat=data.Y_Decimal,
            lon=data.X_Decimal,
            mode='markers',
            marker=go.scattermapbox.Marker(size=9),
            text=data['نام چاه']
        )
    )

    data = data[data['نام چاه'].isin(wells)]

    fig.add_trace(
        go.Scattermapbox(
            lat=list(data.Y_Decimal.unique()),
            lon=list(data.X_Decimal.unique()),
            mode='markers',
            marker=go.scattermapbox.Marker(size=16,
                                           color='green'),
            text=wells
        )
    )

    fig.update_layout(
        mapbox = {'style': "stamen-terrain",
                  'center': {'lon': data.X_Decimal.unique().mean(),
                             'lat': data.Y_Decimal.unique().mean() },
                  'zoom': 7},
        showlegend = False,
        hovermode='closest',
        margin = {'l':0, 'r':0, 'b':0, 't':0}
    )

    return fig

################################################################################## Injaaaaa ############

# Update Content 1 - Fig
@app.callback(Output('content1Tab2', 'figure'),
              Input('data_storage', 'children'),
              Input('aquifer_select_sidebar_tab2', 'value'),
              Input('well_select_sidebar_tab2', 'value'))
def update_content1Tab2(data, aquifer, wells):
    if data == 'No Data' or aquifer is None or ow is None:
        return {
            "layout": {
                "xaxis": {"visible": False},
                "yaxis": {"visible": False},
                "annotations": [{"text": "No matching data found",
                                 "xref": "paper",
                                 "yref": "paper",
                                 "showarrow": False,
                                 "font": {"size": 28}}],
                'height': 600,
                'width': 1000
            }
        }

    df = pd.read_json(data, orient='split')
    df = df[df['نام آبخوان'] == aquifer]
    df = df[df['نام چاه'] == ow]
    name = aquifer + '-' + ow

    # fig = go.Figure()
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Scatter(
            x=df['Date_Persian'],
            y=df['Well_Head'],
            mode='lines+markers',
            name="ارتفاع سطح آب ایستابی"
        ),
        secondary_y=False
    )

    fig.add_trace(
        go.Scatter(
            x=df['Date_Persian'],
            y=df['Depth_To_Water'],
            mode='lines+markers',
            name="عمق سطح ایستابی"

        ),
        secondary_y=True
    )

    fig.update_layout(
        title=name,
        xaxis_title="تاریخ",
        yaxis_title="",
        legend_title="Observation Well",
        autosize=False,
        width=1000,
        height=600,
        font=dict(family="B Zar",
                  size=18,
                  color="RebeccaPurple"
                  )
    )

    fig.update_layout(xaxis=dict(tickformat="%Y-%m"))

    fig.update_yaxes(title_text="ارتفاع سطح آب ایستابی - متر", secondary_y=False)
    fig.update_yaxes(title_text=" عمق سطح ایستابی - متر", secondary_y=True)

    fig.update_xaxes(rangeslider_visible=True)

    return fig