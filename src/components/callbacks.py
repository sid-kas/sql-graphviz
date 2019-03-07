import time, os, sys
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

parent_folder_path = os.path.dirname( os.path.abspath(__file__)).split(r'src')[0]
sys.path.append(parent_folder_path)



def register_callbacks(app, sql_db):

    @app.callback(
        Output('dropdown-column-options', 'options'),
        [Input("execute-button", "n_clicks"),
         Input("execute-button", "n_clicks_timestamp"),
         Input("query_input", "value")]
    )
    def update_dropdown_options(n_clicks, ts, value):
        if n_clicks:
            if str(int(time.time())) == str(ts)[:-3]:
                sql_db.excecutescript(value)
                # time.sleep(0.5)
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
        if n_clicks:
            if str(int(time.time())) == str(ts)[:-3]:
                return ','.join(list(sql_db.shared_data))
        else:
            return []


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
   


