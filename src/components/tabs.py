import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

import time, os, sys
parent_folder_path = os.path.dirname( os.path.abspath(__file__)).split(r'src')[0]
sys.path.append(parent_folder_path)
from src.components.query_table import query_table
from src.components.schema import schema, collapse

tabs = dbc.Tabs(
    [
        dbc.Tab(
            html.Div([
                collapse,
                query_table,
            ]),
            label="GraphQuery"
        ),
        dbc.Tab(schema, label="Other Stuff"),
    ]
)