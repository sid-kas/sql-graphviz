import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html


schema = dbc.Card(
    [
        dbc.CardColumns(
            [
                dbc.Card(
                    [
                        dbc.CardHeader("Another card"),
                        dbc.CardBody(
                            [
                                dbc.CardTitle("This is a title"),
                                dbc.CardText("And some text"),
                            ]
                        ),
                    ],
                    color="dark",
                    outline=True,
                ),
                dbc.Card(
                    [
                        dbc.CardHeader("Yet another card"),
                        dbc.CardBody(
                            [
                                dbc.CardTitle("This is a title"),
                                dbc.CardText("And some text"),
                            ]
                        ),
                    ],
                    color="dark",
                    outline=True,
                ),
                dbc.Card(
                    [
                        dbc.CardHeader("Another card"),
                        dbc.CardBody(
                            [
                                dbc.CardTitle("This is a title"),
                                dbc.CardText("And some text"),
                            ]
                        ),
                    ],
                    color="dark",
                    outline=True,
                ),
                dbc.Card(
                    [
                        dbc.CardHeader("Another card"),
                        dbc.CardBody(
                            [
                                dbc.CardTitle("This is a title"),
                                dbc.CardText("And some text"),
                            ]
                        ),
                    ],
                    color="dark",
                    outline=True,
                ),
                dbc.Card(
                    [
                        dbc.CardHeader("Another card"),
                        dbc.CardBody(
                            [
                                dbc.CardTitle("This is a title"),
                                dbc.CardText("And some text"),
                            ]
                        ),
                    ],
                    color="dark",
                    outline=True,
                ),
            ]
        )

    ],
    className="mt-3",

    
)