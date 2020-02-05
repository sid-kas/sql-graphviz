import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

import time, os, sys
parent_folder_path = os.path.dirname( os.path.abspath(__file__)).split(r'src')[0]
sys.path.append(parent_folder_path)
from src.components.tabs import tabs

body = html.Div([
    dcc.Location(id='url', refresh=False),
    dbc.Col(
        tabs,
    )
]) 
