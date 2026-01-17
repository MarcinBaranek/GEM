from dash import dcc, html
from datetime import datetime, timedelta
from config import TICKERS


# coding=utf-8
layout = html.Div(
    style={"width": "80%", "margin": "auto"},
    children=[
        html.H2("GEM"),

        html.Label("Select ETFs"),
        dcc.Dropdown(
            id="ticker-dropdown",
            options=[{"label": k, "value": v} for k, v in TICKERS.items()],
            value=["^GSPC"],
            multi=True
        ),

        html.Br(),

        html.Label("Select Date Range\t"),
        dcc.DatePickerRange(
            id="date-picker",
            min_date_allowed=datetime(1980, 1, 1),
            max_date_allowed=datetime.today(),
            start_date=datetime.today() - timedelta(days=365),
            end_date=datetime.today(),
            # display_format="YYYY-MM-DD",
            # calendar_orientation="vertical",
            # number_of_months_shown=12
        ),
        dcc.Checklist(
            id="currency-toggle",
            options=[
                {"label": "PLN", "value": True}
            ],
            value=[],  # unchecked by default
            inline=True
        ),

        html.Br(),
        html.Br(),

        dcc.Loading(
            type="default",
            children=[dcc.Graph(id="price-chart")],
        ),
        html.H4("RoR Table"),
        dcc.Loading(
            type="default",
            children=[
                html.Div(id="price-table")
            ]
        ),
        html.Div(style={"height": "150px"})
    ]
)
