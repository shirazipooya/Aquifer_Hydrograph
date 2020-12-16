import dash_html_components as html
from layouts.sidebars import *
from layouts.visualization import *

tab1 = html.Div(
    className='containerTab1',
    children=[
        html.Div(
            className='sidebarTab1',
            children=sidebarTab1
        ),
        html.Div(
            className='content1Tab1',
            children=content1Tab1
        ),
        html.Div(
            className='content2Tab1',
            children=content2Tab1
        ),
        html.Div(
            className='content3Tab1',
            children=content3Tab1
        ),
    ]
)


tab2 = html.Div(
    className='containerTab2',
    children=[
        html.Div(
            className='sidebarTab2',
            children=sidebarTab2
        ),
        html.Div(
            className='content1Tab2',
            children=content1Tab2
        )
    ]
)


tab3 = html.Div(
    className='containerTab3',
    children=[
        html.Div(
            className='sidebarTab3',
            children=sidebarTab3
        ),
        html.Div(
            className='content1Tab3',
            children=content1Tab3
        )
    ]
)