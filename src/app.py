import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from components.navbar import navbar, toggle_navbar_collapse
from components.body import body
from components.query_graph import update_dropdown_options, update_dropdown_value
from components.schema import toggle_collapse

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "sql tool"
app.layout = html.Div([navbar, body])

app.callback(
    Output(f"navbar-collapse", "is_open"),
    [Input(f"navbar-toggler", "n_clicks")],
    [State(f"navbar-collapse", "is_open")],
)(toggle_navbar_collapse)

app.callback(
    Output('dropdown-column-options', 'options'),
    [Input("execute-button", "n_clicks"), 
    Input("query_input", "value")]
)(update_dropdown_options)

app.callback(
    Output('dropdown-column-options', 'value'),
    [Input("execute-button", "n_clicks"),
     Input("query_input", "value")]
)(update_dropdown_value)


app.callback(
    Output("collapse", "is_open"),
    [Input("collapse-button", "n_clicks")],
    [State("collapse", "is_open")],
)(toggle_collapse)


if __name__ == "__main__":
    app.run_server(debug=True)
