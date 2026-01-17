# coding=utf-8
from dash import html, Input, Output
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go

from config import TICKERS
from app import app

@app.callback(
    [
        Output("price-chart", "figure"),
        Output("price-table", "children")
    ],
    [
        Input("ticker-dropdown", "value"),
        Input("date-picker", "start_date"),
        Input("date-picker", "end_date"),
        Input("currency-toggle", "value"),
    ]
)
def update_output(selected_tickers, start_date: str, end_date: str, currency):
    start_date = start_date.split("T")[0]
    end_date = end_date.split("T")[0]

    if not selected_tickers:
        fig = go.Figure()
        fig.update_layout(
            title="Rate of returns",
            xaxis_title="Date",
            yaxis_title="Price",
            template="plotly_dark",  # Dark chart template
            paper_bgcolor="#121212",  # Container background
            plot_bgcolor="#121212",  # Plot area background
            font=dict(color="#ffffff")  # Text color
        )
        return fig, "No tickers selected."
    if currency:
        selected_tickers.append("EURPLN=X")

    # Download data
    data = yf.download(
        tickers=selected_tickers,
        start=start_date,
        end=end_date,
        auto_adjust=True,
        progress=False
    )["Close"]

    if isinstance(data, pd.Series):
        data = data.to_frame()

    data.fillna(method="ffill", inplace=True)


    for col in data.columns:
        if col == "EURPLN=X":
            continue
        data[col] = data[col] / data.loc[data.index[0], col]
        if currency:
            data[col] *= data["EURPLN=X"]
    if currency:
        data.drop(columns=["EURPLN=X"], inplace=True)

    data.rename(columns={v: k for k, v in TICKERS.items()}, inplace=True)
    data -= 1
    data *= 100
    # -------------------------
    # Create price chart
    # -------------------------
    fig = go.Figure()

    for ticker in data.columns:
        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data[ticker],
                mode="lines",
                name=ticker
            )
        )

    fig.update_layout(
        title="Historical Prices",
        xaxis_title="Date",
        yaxis_title="Rate of Return",
        template="plotly_dark",  # Dark chart template
        paper_bgcolor="#121212",  # Container background
        plot_bgcolor="#121212",  # Plot area background
        font=dict(color="#ffffff")  # Text color
    )



    # -------------------------
    # Create data table
    # -------------------------
    table = html.Table(
        style={
            "width": "100%",
            "borderCollapse": "collapse",
            "fontSize": "16px",
            "textAlign": "center",
            "border": "1px solid #888",
        },
        children=[
            html.Thead(
                html.Tr(
                    [html.Th(
                        "Date",
                        style={
                            "border": "1px solid #888",
                            "padding": "8px",
                            "fontWeight": "bold"
                        }
                    )] +
                    [
                        html.Th(
                            col,
                            style={
                                "border": "1px solid #888",
                                "padding": "8px",
                                "fontWeight": "bold"
                            }
                        )
                        for col in data.columns
                    ]
                )
            ),
            html.Tbody(
                [
                    html.Tr(
                        [html.Td(
                            idx.strftime("%Y-%m-%d"),
                            style={
                                "border": "1px solid #888",
                                "padding": "8px"
                            }
                        )] +
                        [
                            html.Td(
                                f"{val:.2f}%",
                                style={
                                    "border": "1px solid #888",
                                    "padding": "8px"
                                }
                            )
                            for val in row
                        ]
                    )
                    for idx, row in data.tail(1).iterrows()
                ]
            )
        ]
    )

    return fig, table