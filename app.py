import dash
from dash import dcc
from dash import html
import pandas as pd
import numpy as np
from dash.dependencies import Output, Input

data = pd.read_csv("insecurity_data.csv")
data["Date"] = pd.to_datetime(data["Date"], format="%m/%d/%Y")
data.sort_values("Date", inplace=True)

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = "Insecurity Tracker!"

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.P(children="👋", className="header-emoji"),
                html.H1(
                    children=" CAPE Economic Research and Consulting Insecurity Tracker", className="header-title"
                ),
                html.P(
                    children="State-by-state insecurity tracker in Nigeria",
                    "",
                    "from 2011 till date",
                    className="header-description",
                ),
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="State", className="menu-title"),
                        dcc.Dropdown(
                            id="state-filter",
                            options=[
                                {"label": state, "value": state}
                                for state in np.sort(data.state.unique())
                            ],
                            value="Adamawa",
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(children=" Violence Type", className="menu-title"),
                        dcc.Dropdown(
                            id="type-filter",
                            options=[
                                {"label": violence_type, "value": violence_type}
                                for violence_type in data.type.unique()
                            ],
                            value="Boko Haram",
                            clearable=False,
                            searchable=False,
                            className="dropdown",
                        ),
                    ],
                ),
                html.Div(
                    children=[
                        html.Div(
                            children="Date Range", className="menu-title"
                        ),
                        dcc.DatePickerRange(
                            id="date-range",
                            min_date_allowed=data.Date.min().date(),
                            max_date_allowed=data.Date.max().date(),
                            start_date=data.Date.min().date(),
                            end_date=data.Date.max().date(),
                        ),
                    ]
                ),
            ],
            className="menu",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="death-chart",
                        config={"displayModeBar": False},
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
    ]
)


@app.callback(
    Output("death-chart", "figure"),
    [
        Input("state-filter", "value"),
        Input("type-filter", "value"),
        Input("date-range", "start_date"),
        Input("date-range", "end_date"),
    ],
)
def update_charts(state, avocado_type, start_date, end_date):
    mask = (
        (data.state == state)
        & (data.type == avocado_type)
        & (data.Date >= start_date)
        & (data.Date <= end_date)
    )
    filtered_data = data.loc[mask, :]
    death_chart_figure = {
        "data": [
            {
                "x": filtered_data["Date"],
                "y": filtered_data["Death"],
                "type": "lines",
            },
        ],
        "layout": {
            "title": {"text": "Number of Deaths Recorded", "x": 0.05, "xanchor": "left"},
            "xaxis": {"fixedrange": True},
            "yaxis": {"fixedrange": True},
            "colorway": ["#E12D39"],
        }
    }
    return death_chart_figure


if __name__ == "__main__":
    app.run_server(debug=True)
