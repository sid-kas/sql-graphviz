import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

import time, os, sys
parent_folder_path = os.path.dirname( os.path.abspath(__file__)).split(r'src')[0]
sys.path.append(parent_folder_path)
from src.components.query_table import query_table

collapse = html.Div([
    
])

tabs = dbc.Tabs(
    [
        dbc.Tab(html.Div([
                dbc.Card(
                id="schema",
            ),
        ]), label="Schema",tab_id = 'tab1'),

        dbc.Tab(
            html.Div([

                query_table,
                html.Div(id="data-graph"),
                html.Div(id="data-table",className="mt-2"), 
            ]),
            label="GraphQuery", tab_id='tab2'
        ),
    ],
    id="tabs",
    active_tab="tab2",
)


