import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_daq as daq
import numpy as np


from layouts.visualization import *

sidebarTab1 = [
    html.H3(
        className='headerText',
        children=['بارگذاری فایل های ورودی']
    ),
    html.Hr(),
    dbc.Form(
        className='formSidebar',
        children=[
            dbc.FormGroup(
                className='formgroupSidebar',
                children=[
                    dbc.Label(
                        children=[
                            'انتخاب داده های مورد نیاز:'
                        ]
                    ),
                    dbc.Row(
                        align='baseline',
                        children=[
                            dcc.Upload(
                                id='uploadButton_rawData',
                                className='uploadButton',
                                children=[
                                    html.Button('انتخاب فایل')
                                ],
                            ),
                            dbc.FormText(
                                id='uploadButtonInfo_rawData',
                                className='uploadButtonInfo'
                            )
                        ]
                    )
                ]
            ),
            html.Br(),
            dbc.Card(
                className='card_sidebar_tab1',
                children=[
                    dbc.CardHeader("اطلاعات داده های ورودی"),
                    dbc.CardBody(
                        [
                            html.H5("تعداد آبخوان های موجود", className="card-title"),
                            html.P(
                                id='number_aquifer_sidebar_tab1',
                                className="card-text",
                            ),
                        ]
                    ),
                    html.Hr(),
                    dbc.CardBody(
                        [
                            html.H5("تعداد چاه های مشاهده ای موجود", className="card-title"),
                            html.P(
                                id='number_well_sidebar_tab1',
                                className="card-text",
                            ),
                        ]
                    ),
                    html.Br(),
                ],
                color="primary",
                outline=True
            ),
            # Hidden div inside the app that stores info and raw data
            html.Div(
                id='infoData',
                style={
                    'display': 'none'
                }
            ),
            html.Div(
                id='rawData',
                style={
                    'display': 'none'
                }
            ),
            html.Div(
                id='finalData',
                style={
                    'display': 'none'
                }
            ),
        ]
    )
]



sidebarTab2 = [
    html.H3(
        className='headerText',
        children=['اطلاعات ورودی']
    ),
    html.Hr(),
    dbc.Form(
        className='formSidebar',
        children=[
            dbc.FormGroup(
                className='formgroupSidebar',
                children=[
                    dbc.Label(
                        children=[
                            'انتخاب آبخوان:'
                        ]
                    ),
                    dcc.Dropdown(
                        id='aquifer_select_sidebar_tab2',
                        placeholder="یک آبخوان انتخاب کنید",
                        className='dropdown'
                    ),
                ]
            ),
            html.Br(),
            dbc.FormGroup(
                className='formgroupSidebar',
                children=[
                    dbc.Label(
                        children=[
                            'انتخاب چاه مشاهده ای:'
                        ]
                    ),
                    dcc.Dropdown(
                        id='well_select_sidebar_tab2',
                        placeholder="یک یا چند چاه مشاهده ای را انتخاب کنید",
                        multi=True,
                        className='dropdown'
                    ),
                ]
            ),
            html.Br(),
            dbc.FormGroup(
                children=[
                    html.Div(
                        className='div_switch',
                        children=[
                            daq.BooleanSwitch(
                                id='boolean_switch_sidebar_tab2',
                                on=False,
                                color="#9B51E0",
                                label='نشان دادن عمق آب چاه مشاهده ای',
                                labelPosition="top",
                                disabled=False
                            )
                        ]
                    )
                ]
            ),
            html.Br(),
            dbc.FormGroup(
                className='formgroupSidebar',
                children=mapSidebarTab2
            ),
        ]
    )
]



sidebarTab3 = [
    html.H3(
        className='headerText',
        children=['اطلاعات ورودی']
    ),
    html.Hr(),
    dbc.Form(
        className='formSidebar',
        children=[
            dbc.FormGroup(
                className='formgroupSidebar',
                children=[
                    dbc.Label(
                        children=[
                            'انتخاب آبخوان:'
                        ]
                    ),
                    dcc.Dropdown(
                        id='aquifer_select_sidebar_tab3',
                        placeholder="یک آبخوان انتخاب کنید",
                        className='dropdown'
                    ),
                ]
            ),
            dbc.FormGroup(
                className='formgroupSidebar',
                children=mapSidebarTab3
            ),
            html.Br(),
            dbc.FormGroup(
                className='formgroupSidebar',
                children=[
                    dbc.Label(
                        children=[
                            'انتخاب حد مجاز اختلاف ارتفاع سطح ایستابی:'
                        ]
                    ),
                    html.Div(
                        className='div_show_delta_select',
                        children=[
                            dbc.Label(
                                className='show_delta_select',
                                id='show_delta_select_sidebar_tab3'
                            )
                        ]
                    ),
                    dcc.Slider(
                        className='sider_sidebar_tab3',
                        id="delta_select_sidebar_tab3",
                        min=0,
                        max=5,
                        step=0.1,
                        value=0.5,
                        marks={i: str(i) for i in np.arange(0, 5.1, 0.5).tolist()}
                    ),
                    html.Br(),
                    html.Div(
                        className='ss',
                        children=[
                            dcc.Checklist(
                                id='select_mean_aquifer_head',
                                options=[
                                    {'label': '   میانگین حسابی', 'value': 'Arithmetic'},
                                    {'label': '   میانگین هندسی', 'value': 'Geometric'},
                                    {'label': '   میانگین هارمونیک', 'value': 'Harmonic'}
                                ],
                                value=['Arithmetic'],
                                labelStyle = {'display': 'block'}
                            )
                        ]
                    ),
                    html.Br(),
                    html.Div(
                        className='calculate_button_div',
                        children=[
                            dbc.Button("محاسبه",
                                       id='calculate_button_sidebar_tab3',
                                       className='calculate_button',
                                       outline=True,
                                       color="secondary",
                                       n_clicks=0)
                        ]
                    )
                ]
            )
        ]
    )
]
