import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

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
                            'مشخصات چاه های مشاهده ای:'
                        ]
                    ),
                    dbc.Row(
                        align='baseline',
                        children=[
                            dcc.Upload(
                                id='uploadButton_wellInfo',
                                className='uploadButton',
                                children=[
                                    html.Button('انتخاب فایل')
                                ],
                            ),
                            dbc.FormText(
                                id='uploadButtonInfo_wellInfo',
                                className='uploadButtonInfo'
                            )
                        ]
                    )
                ]
            ),
            html.Br(),
            dbc.FormGroup(
                className='formgroupSidebar',
                children=[
                    dbc.Label(
                        children=[
                            'داده های مورد نیاز:'
                        ]
                    ),
                    dbc.Row(
                        align='baseline',
                        children=[
                            dcc.Upload(
                                id='uploadButton_data',
                                className='uploadButton',
                                children=[
                                    html.Button('انتخاب فایل')
                                ],
                            ),
                            dbc.FormText(
                                id='uploadButtonInfo_data',
                                className='uploadButtonInfo'
                            )
                        ]
                    )
                ]
            )
        ]
    )
]