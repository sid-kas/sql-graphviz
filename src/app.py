import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from components.navbar import navbar, toggle_navbar_collapse
from components.body import body


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([navbar, body])

app.callback(
    Output(f"navbar-collapse", "is_open"),
    [Input(f"navbar-toggler", "n_clicks")],
    [State(f"navbar-collapse", "is_open")],
)(toggle_navbar_collapse)


if __name__ == "__main__":
    app.run_server(debug=True)