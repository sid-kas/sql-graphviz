import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import argparse

from components.navbar import navbar
from components.body import body
from components.callbacks import register_callbacks
from sql.sqlite_db import SqliteDB

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "sql tool"
app.layout = dbc.Container([navbar, body], style={"max-width": "80%"})



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('file_path',help='Path to db file')
    parser.add_argument("-d", "--debug",  action='store_true', help="debug mode")
    parser.add_argument("-H", "--host", type=str, default="127.0.0.1")
    parser.add_argument("-P", "--port", type=int, default=8060, help="port")
    args = parser.parse_args()
    
    sqlite_db = SqliteDB(args.file_path)
    sqlite_db.get_schema()
    register_callbacks(app,sqlite_db)
    app.run_server(host=args.host, port=args.port, debug=args.debug)
