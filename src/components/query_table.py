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
                                dcc.Store(id="shared-query-history"),
                                dcc.Store(id="shared-data"),
                                dbc.Textarea(
                                    id= "query_input", bs_size="lg", placeholder="Enter SQL Query", className="mb-2",
                                    autoFocus=True, debounce=True,value='',
                                ),
                                
                                dbc.Row([
                                    dbc.Col([
                                        dbc.Button("Execute", id="execute-button", color="secondary", className="mb-2"),
                                    ],width=3),
                                    dbc.Col([
                                        dcc.Checklist(
                                            id="check-list",
                                            options=[
                                                {'label': 'Show Table', 'value': 'show-table'},
                                            ],
                                            values=['show-table'],
                                            labelStyle={'display': 'inline-block'}
                                        ),
                                    ],width=3 ),
                                ],no_gutters=True,align="center",justify='start'),
                                                                
                            ],
                            md=5,
                        ),
                        dbc.Col([
                            html.Div([
                                dcc.Dropdown(
                                    id='dropdown-query-history',
                                    className="mb-2",
                                    placeholder="Load query from preloads/history",
                                ),
                            ]),
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

                        ]),
                    ]
                ),
            ]
        ),

    ],
    className="mt-3 mb-3",
    
)


