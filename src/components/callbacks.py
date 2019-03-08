import time, os, sys
import dash, dash_table
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from plotly import graph_objs as go
from dash.exceptions import PreventUpdate

parent_folder_path = os.path.dirname( os.path.abspath(__file__)).split(r'src')[0]
sys.path.append(parent_folder_path)

from src.common.logging_service import getLogger

logger = getLogger("Queries","queries.log",path=parent_folder_path+"src/assets")

def register_callbacks(app, sql_db):

    @app.callback(
        Output('dropdown-column-options', 'options'),
        [Input("execute-button", "n_clicks"),
         Input("execute-button", "n_clicks_timestamp"),
         Input("query_input", "n_clicks"),
         Input("query_input", "value"),]
    )
    def update_dropdown_options(n_clicks_button, ts,n_clicks_input, value):
        if n_clicks_button and n_clicks_input:
            if str(int(time.time())) == str(ts)[:-3]:
                logger.info(str(value))
                sql_db.excecutescript(value)
                return [{'label': col, 'value': col} for col in sql_db.shared_data.columns.values]
        else:
            return []

    @app.callback(
        Output('dropdown-column-options', 'value'),
        [Input("execute-button", "n_clicks"),
         Input("execute-button", "n_clicks_timestamp"),
         Input("query_input", "value")]
    )
    def update_dropdown_value(n_clicks, ts, value):
        time.sleep(0.5)
        if n_clicks and sql_db.shared_data.shape[0]>0:
            return list(sql_db.shared_data)
        else:
            return []

    @app.callback(
        Output('data-graph', 'children'),
        [Input("plot-button", "n_clicks"),
         Input("plot-button", "n_clicks_timestamp"),
         Input("dropdown-column-options", "value")]
    )
    def update_graph(n_clicks, ts, value):
        if n_clicks:
            if str(int(time.time())) == str(ts)[:-3]:
                card = dbc.Card([
                            dbc.CardHeader("Graph view"),
                            dcc.Graph(figure=generate_graph(sql_db.shared_data,value)),
                        ])
                return card

   
    @app.callback(Output('data-table', 'children'),
                [Input("show-table-button", "n_clicks"),
                Input("show-table-button", "n_clicks_timestamp"),])
    def on_data_set_table(n_clicks, ts):
        if n_clicks:
            if str(int(time.time())) == str(ts)[:-3]:
                table = dash_table.DataTable(
                            data=sql_db.shared_data.to_dict('rows'),
                            columns=[{'id': c, 'name': c} for c in sql_db.shared_data.columns],
                            n_fixed_rows=1,
                            style_cell={'textAlign': 'left','width': '50px'},
                            style_cell_conditional=[{
                                'if': {'row_index': 'odd'},
                                'backgroundColor': 'rgb(248, 248, 248)'
                            }],
                            style_header={
                                'backgroundColor': '#3D9970',
                                'fontWeight': 'bold',
                                'color': 'white'
                            },
                            style_table={'maxHeight': '300',},
                        )
                card = dbc.Card([dbc.CardHeader("Table View"),dbc.CardBody(table)],className="mt-2")
                return card



    @app.callback(
        Output(f"navbar-collapse", "is_open"),
        [Input(f"navbar-toggler", "n_clicks")],
        [State(f"navbar-collapse", "is_open")],
    )
    def toggle_navbar_collapse(n, is_open):
        if n:
            return not is_open
        return is_open


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
        trace = go_scatter_plot(data[key].values, data[key].dtype,key) 
        if trace:
            trace_list.append(trace)

    figure = go.Figure(
                data=trace_list,
                layout=layout
            )
    return figure


def go_scatter_plot(data, dtype, name):
    if ("int" in str(dtype).lower() or "float" in str(dtype).lower()) and ('id' not in name.lower()):
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
            ], bordered=True)

    return table


   


