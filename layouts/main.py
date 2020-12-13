import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from layouts.tabs import tab1, tab2

main_layout = dbc.Tabs(
    className='mainLayoutTabs',
    children=[
        dbc.Tab(
            id='Tab1',
            label='ورود داده ها',
            tabClassName='tabClassName',
            labelClassName='labelClassName',
            children=[
                tab1
            ]
        ),
        dbc.Tab(
            id='Tab2',
            label='چاه های مشاهده ای',
            tabClassName='tabClassName',
            labelClassName='labelClassName',
            children=[
                tab2
            ]
        ),
        dbc.Tab(
            id='Tab3',
            label='Tab3',
            tabClassName='tabClassName',
            labelClassName='labelClassName',
            children=[
                'Tab3'
            ]
        )
    ]
)
