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
                                    id= "query_input", bs_size="lg", placeholder="Enter SQL Query", className="mb-2"
                                ),
                                dbc.Button("Execute", id="execute-button", color="secondary", className="mb-2"),
                                dcc.Dropdown(
                                    id='dropdown-column-options',
                                    multi=True,
                                    className="mb-2"
                                ),
                                dbc.Button(
                                        "Plot graph", id="plot-button", color="secondary", className="mb-2"),
                                    
                            ],
                            md=4,
                        ),
                        dbc.Col(
                            [
                                dbc.Card([
                                    dbc.CardHeader("Results"),
                                    dbc.CardBody(
                                        [
                                            dbc.CardTitle("This is a title"),
                                            dbc.CardText("And some text"),
                                        ]
                                    ),
                                ])
                                
                            ]
                        ),
                    ]
                ),
            ]
        ),

    ],
    className="mt-3",
    
)


