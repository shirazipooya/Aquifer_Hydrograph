from server import app
from callbacks.data import *

import pandas as pd

import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_daq as daq
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

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
              'zoom': 5.5},
    showlegend = False,
    hovermode='closest',
    margin = {'l':0, 'r':0, 'b':0, 't':0},
    autosize=False)



# Update Aquifer Select Dropdown - Sidebar
@app.callback(Output('aquifer_select_sidebar_tab2', 'options'),
              Input('infoData', 'children'))
def update_aquifer_select_sidebar_tab2(infoData):
    if infoData is None or infoData == 'No Data':
        return []
    data = pd.read_json(infoData, orient='split')
    return [{"label": col, "value": col} for col in data['نام آبخوان'].unique()]


# Update Well Select Dropdown - Sidebar
@app.callback(Output('well_select_sidebar_tab2', 'options'),
              Input('aquifer_select_sidebar_tab2', 'value'),
              Input('infoData', 'children'))
def update_well_select_sidebar_tab2(aquifer, infoData):
    if infoData == 'No Data' or aquifer is None:
        return []
    data = pd.read_json(infoData, orient='split')
    data = data[data['نام آبخوان'] == aquifer]
    return [{"label": col, "value": col} for col in data['نام چاه'].unique()]



# Update Map Sidebar
@app.callback(Output('mapSidebarTab2', 'figure'),
              Input('aquifer_select_sidebar_tab2', 'value'),
              Input('well_select_sidebar_tab2', 'value'),
              Input('infoData', 'children'))
def update_mapSidebarTab2(aquifer, wells, infoData):
    if infoData == 'No Data' or wells is None:
        return base_map
    data = pd.read_json(infoData, orient='split')
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
                  'center': {'lon': data.X_Decimal.mean(),
                             'lat': data.Y_Decimal.mean() },
                  'zoom': 7},
        showlegend = False,
        hovermode='closest',
        margin = {'l':0, 'r':0, 'b':0, 't':0}
    )

    return fig



# Disabled Boolean Switch
@app.callback(Output('boolean_switch_sidebar_tab2', 'disabled'),
              Output('boolean_switch_sidebar_tab2', 'on'),
              Input('well_select_sidebar_tab2', 'value'))
def disabled_boolean_switch(wells):
    if wells is None:
        return True, False
    elif len(wells) == 1:
        return False, False
    else:
        return True, False


# Update Content 1 - Fig
@app.callback(Output('content1Tab2', 'figure'),
              Input('rawData', 'children'),
              Input('aquifer_select_sidebar_tab2', 'value'),
              Input('well_select_sidebar_tab2', 'value'),
              Input('boolean_switch_sidebar_tab2', 'disabled'),
              Input('boolean_switch_sidebar_tab2', 'on'))
def update_content1Tab2(data, aquifer, wells, switch_disable, switch_on):
    if data == 'No Data' or aquifer is None or wells is None:
        return No_Matching_Data_Found_Fig

    df = pd.read_json(data, orient='split')
    df = df[df['نام آبخوان'] == aquifer]
    df = df[df['نام چاه'].isin(wells)]

    fig = make_subplots(specs=[[{"secondary_y": True}]])


    # fig = go.Figure()
    if len(wells) == 1:
        df_well = df[df['نام چاه'] == wells[0]]
        fig.add_trace(
            go.Scatter(
                x=df_well['Date_Persian'],
                y=df_well['Well_Head'],
                mode='lines+markers',
                name='ارتفاع سطح آب ایستابی'),
            secondary_y=False
        )
    elif len(wells) > 1:
        for well in wells:
            df_well = df[df['نام چاه'] == well]
            fig.add_trace(
                go.Scatter(
                    x=df_well['Date_Persian'],
                    y=df_well['Well_Head'],
                    mode='lines+markers',
                    name=well),
                secondary_y=False
            )

    fig.update_layout(
        xaxis_title="تاریخ",
        yaxis_title="",
        autosize=False,
        font=dict(
            family="B Koodak",
            size=16,
            color="RebeccaPurple"
        ),
        xaxis=dict(
            tickformat="%Y-%m"
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0
        )
    )

    fig.update_yaxes(title_text="ارتفاع سطح آب ایستابی - متر", secondary_y=False)

    if switch_disable is False and switch_on is True:
        fig.add_trace(
            go.Scatter(
                x=df_well['Date_Persian'],
                y=df_well['Depth_To_Water'],
                mode='lines+markers',
                name='عمق سطح ایستابی'
            ),
            secondary_y=True
        )

        fig.update_yaxes(title_text="عمق سطح ایستابی - متر", secondary_y=True)
        fig.update_xaxes(rangeslider_visible=True)

    return fig