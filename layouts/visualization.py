import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table

# Tab 1 - Content 1 - Map 1
content1Tab1 = [
    dcc.Graph(
        id='content1Tab1',
        className='mapTab1'
    )
]

# Tab 1 - Content 2 - Map 2
content2Tab1 = [
    dcc.Graph(
        id='content2Tab1',
        className='mapTab1'
    )
]

# Tab 1 - Content 3 - Table
content3Tab1 = dash_table.DataTable(
    id='content3Tab1',
    style_table={
        'overflowX': 'auto',
        'overflowY': 'auto',
        'padding':'5px'
    },
    style_cell={
        'border': '1px solid grey',
        'font-size': '12px',
        'font_family': 'B Koodak',
        'font_size': '12px',
        'text_align': 'right',
        'minWidth': 100,
        'maxWidth': 150,
        'width': 125
    },
    fixed_rows={
        'headers': True
    },
    style_header={
        'backgroundColor': 'rgb(230, 230, 230)',
        'fontWeight': 'bold',
        'whiteSpace': 'normal',
    },
    page_size=10
)


# Tab 2 - Sidebar - Map
mapSidebarTab2 = [
    dcc.Graph(
        id='mapSidebarTab2',
        className='mapSidebarTab2'
    )
]

# Tab 2 - Content 1 - Fig
content1Tab2 = [
    dcc.Graph(
        id='content1Tab2',
        className='figTab2'
    )
]

# Tab 3 - Sidebar - Map
mapSidebarTab3 = [
    dcc.Graph(
        id='mapSidebarTab3',
        className='mapSidebarTab3'
    )
]

# Tab 3 - Content 1 - Fig
content1Tab3 = [
    dcc.Graph(
        id='content1Tab3',
        className='figTab3'
    )
]