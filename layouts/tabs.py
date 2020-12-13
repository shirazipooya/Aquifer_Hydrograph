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