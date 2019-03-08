import dash
import dash_table
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

import time, os, sys
parent_folder_path = os.path.dirname( os.path.abspath(__file__)).split(r'src')[0]
sys.path.append(parent_folder_path)


query_table =  dbc.Card(
    [
        dbc.CardBody(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Textarea(
                                    id= "query_input", bs_size="lg", placeholder="Enter SQL Query", className="mb-2",
                                    autoFocus=True, debounce=True,
                                ),
                                dbc.Button("Execute", id="execute-button", color="secondary", className="mb-2 mr-2"),
                                dbc.Button("Show Table", id="show-table-button", color="secondary", className="mb-2 mr-2"),
                                html.Div(id="data-table",className="mt-2"),    
                            ],
                            md=5,
                        ),
                        dbc.Col([
                            dbc.Row([
                                dbc.Col([
                                    dcc.Dropdown(
                                        id='dropdown-column-options',
                                        multi=True,
                                        className="mb-2"
                                    ),
                                ]),
                                dbc.Col([
                                    dbc.Button("Plot graph", id="plot-button", color="secondary", className="mb-2 ml-2")
                                ], md=3),
                            ],no_gutters=True,align="center"),
                            html.Div(id="data-graph") 
                        ]),
                    ]
                ),
            ]
        ),

    ],
    className="mt-3",
    
)


