
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open
    
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


def update_dropdown_options(n_clicks, value):
    if n_clicks:
        return getColumns(value)


def update_dropdown_value(n_clicks, value):
    if n_clicks:
        return [ls['value'] for ls in getColumns(value)]


def getColumns(value):
    print(value)
    return [{'label': 'Save data', 'value': 'save'},
            {'label': 'View file status', 'value': 'fileStatus'},
            {'label': 'Accumulate data', 'value': 'accumulate'}]
