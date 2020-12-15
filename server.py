import dash
import dash_bootstrap_components as dbc

bWLwgP = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(
    name=__name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP, bWLwgP]
)