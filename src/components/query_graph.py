import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

query_graph =  dbc.Card(
    [
        dbc.CardBody(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Textarea(
                                    bs_size="lg", placeholder="Enter SQL Query", className="mb-2"
                                ),
                                dbc.Button("Execute", id="execute-button", color="secondary"),
                                dcc.Dropdown(
                                    id='dropdown-column-options',
                                    multi=True
                                ),
                            ],
                            md=4,
                        ),
                        dbc.Col(
                            [
                                html.H2("Graph"),
                                dcc.Graph(
                                    figure={"data": [{"x": [1, 2, 3], "y": [1, 4, 9]}]}
                                ),
                            ]
                        ),
                    ]
                ),
            ]
        ),

    ],
    className="mt-3",
    
)


@app.callback(
    dash.dependencies.Output('dropdown-column-options', 'options'),
    [Input("execute-button", "n_clicks"), Input("input", "value")]
)
def update_date_dropdown(name):

    return 