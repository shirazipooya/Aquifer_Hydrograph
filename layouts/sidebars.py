import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_daq as daq


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
            )
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