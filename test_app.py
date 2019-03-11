import dash
import dash_html_components as html
import dash_bootstrap_components as dbc
import sd_material_ui

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

ds = [
    "af", "ks_flat(n_clicks_flat: int, n_clicks_flat_prev: int):", "flat(n_clicks_flat: int, n_clicks_flat_prev: int):", "be"]
# A FlatButton on Paper

body = html.Div([
    sd_material_ui.AutoComplete(id="auto-complete", hintText="type some thing",
                                floatingLabelText="full", openOnFocus=True, fullWidth=True, dataSource=ds,style={"width": "320px"})
],style={"width":"320px"})




app.layout = dbc.Container([body], style={"max-width": "90%"})


@app.callback(
    dash.dependencies.Output('auto-complete', 'dataSource'),
    [dash.dependencies.Input('auto-complete',"searchText")]
)
def update_auto_complete(val):
    print(val)
    return ds

if __name__ == '__main__':
    app.run_server(debug=True)
