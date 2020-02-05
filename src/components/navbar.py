import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

nav_item = dbc.NavItem(dbc.NavLink("Schema", href="#"))

navbar = dbc.Navbar(
    [
        html.A(
            dbc.Row(
                [
                    dbc.Col(html.Img(src="./assets/rpi.png", height="50px")),
                    dbc.Col(dbc.NavbarBrand("SQL Graph Visualization", className = "ml-2")),
                ],
                align="center",
                no_gutters=True,
            ),
            href="#",
        ),
        dbc.NavbarToggler(id="navbar-toggler"),
        dbc.Collapse(
            dbc.Nav(
                [nav_item], className="ml-auto", navbar=True
            ),
            id="navbar-collapse",
            navbar=True,
        ), 

    ],
    color="dark",
    dark=True,
    className="mb-2",
           
)



