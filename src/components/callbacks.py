import time, os, sys, json
import dash, dash_table
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from plotly import graph_objs as go
from dash.exceptions import PreventUpdate
import numpy as np
import pandas as pd

parent_folder_path = os.path.dirname( os.path.abspath(__file__)).split(r'src')[0]
sys.path.append(parent_folder_path)

from src.common.logging_service import getLogger

querry_logger = getLogger("Queries","queries.log")
logger = getLogger("callbacks")

def register_callbacks(app, sql_db):

   
    @app.callback(
        Output('shared-data', 'data'),
        [Input("execute-button", "n_clicks")],
        [State("query_input", "value")],
    )
    def update_shared_data(n_clicks, input_value):
        if n_clicks and input_value:
            if len(input_value)>0:
                querry_logger.info(str(input_value).encode())
            data = sql_db.excecutescript(input_value)                
            return data
        else:
            raise PreventUpdate

    @app.callback(
        Output('dropdown-column-options', 'options'),
        [Input("shared-data","data")]
    )
    def update_dropdown_options(data):
        if data:
            return  [{'label':key,'value':key} for key in data.keys()]
        else:
            raise PreventUpdate

    @app.callback(
        Output('dropdown-column-options', 'value'),
        [Input("shared-data","data")]
    )
    def update_dropdown_value(data):
        if data:
            return [key for key in data.keys()]
        else:
            raise PreventUpdate

           
           
    @app.callback(
        Output('data-graph', 'children'),
        [Input("plot-button", "n_clicks")],
        [State("dropdown-column-options", "value"),
         State("shared-data","data")]
    )
    def update_graph(n_clicks, value, data):
        if n_clicks and data:
            card = dbc.Card([
                        dbc.CardHeader("Graph view"),
                        dcc.Graph(figure=generate_graph(data,value)),
                    ])
            return card
        else:
            raise PreventUpdate
        

   
    @app.callback(Output('data-table', 'children'),
                [Input("shared-data","data"),
                Input("check-list","values")])
    def on_data_set_table(data,values):
        val = ','.join(values)
        if data:
            if "show-table" in val:
                df = pd.DataFrame(data=data,columns=data.keys())
                table = dash_table.DataTable(
                    data=df.to_dict("rows"),
                    columns=[{'id': c, 'name': c, "deletable": True} for c in data.keys()],
                    n_fixed_rows=1,
                    filtering=True,
                    sorting=True,
                    style_cell={'textAlign': 'left'},
                    style_header={
                        'backgroundColor': 'white',
                        'fontWeight': 'bold'
                    },
                    style_table={'maxHeight': '500px',},
                    # style_cell={'padding': '5px'},
                    # style_as_list_view=True,
                )
                card = dbc.Card([dbc.CardHeader("Table View"),dbc.CardBody(table)],className="mt-3 mb-3")
                return card
            else:
                return html.Div()
        else:
            raise PreventUpdate



    @app.callback(
        Output("navbar-collapse", "is_open"),
        [Input("navbar-toggler", "n_clicks")],
        [State("navbar-collapse", "is_open")],
    )
    def toggle_navbar_collapse(n, is_open):
        if n:
            return not is_open
        return is_open

    @app.callback(Output("shared-query-history","data"), [Input('url', 'pathname')])
    def get_query_history(path_name):
        if path_name=="/":
            queries = set()
            logs_file_path = parent_folder_path+"logs/queries.log"
            with open(logs_file_path,mode='r') as f:
                lines = f.readlines()
                for line in lines:
                    query = line.split(' - ')[-1]
                    queries.add(query.replace("'\n",'').replace(r"\n",'').replace("b\'",'').replace("\\",''))
                l = [{'label':query,'value':query} for query in queries]
            return l
        else:
            raise PreventUpdate

    @app.callback(
        Output("query_input", "value"), 
        [Input('dropdown-query-history', 'value')])
    def update_query_input_from_dropdown(value):
        if value:
            return value
        else:
            raise PreventUpdate

    @app.callback(
        Output('dropdown-query-history', 'options'),
        [Input("shared-query-history","data")]
    )
    def update_query_history(queries):
        if queries:
            return queries


    @app.callback(Output("schema", "children"), [Input("tabs", "active_tab")])
    def get_schema(active_tab):
        if active_tab=="tab1":
            schema = html.Div(
                [
                    dbc.CardColumns([
                            generate_card(key,val) for key,val in sql_db.schema.items()
                        ],
                    ),
                ],
                className="mt-3",
            )

            return schema



    
def generate_graph(data,columns):
    layout = go.Layout(
        xaxis=dict(
            showgrid=False,
            showline=False,
            zeroline=False,
        ),
        margin=go.layout.Margin(
            t=45,
            l=50,
            r=50
        )
    )
    trace_list = []
    for key in columns:
        trace = go_scatter_plot(data[key],key) 
        if trace:
            trace_list.append(trace)

    figure = go.Figure(
                data=trace_list,
                layout=layout
            )
    return figure


def go_scatter_plot(data, name):
    dtype = str(type(data[0])).lower()
    if ("int" in dtype or "float" in dtype) and ('id' not in name.lower()):
        trace = go.Scatter(
            y= list(data),
            mode='lines',
            name=name
        )
        return trace
    else:
        pass


def generate_card(title,contents):
    return dbc.Card(
        [
            dbc.CardHeader(title),
            dbc.CardBody(
                generate_table(["id","name","type"],contents),
            ),
        ],
        outline=True,
        color="dark",
        
    )

def generate_table(head,contents):
    table = dbc.Table([
                html.Thead(html.Tr([html.Th(h) for h in head])),
                html.Tbody([html.Tr([html.Td(cont) for cont in content]) for content in contents]),
            ],bordered=True,hover=True,responsive=True,striped=True,)

    return table


   


