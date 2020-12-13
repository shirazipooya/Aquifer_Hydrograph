from server import app
from layouts.main import main_layout

app.layout = main_layout

from callbacks.main import *

if __name__ == '__main__':
    app.run_server(
        host='127.0.0.1',
        port='8080',
        debug=True
    )