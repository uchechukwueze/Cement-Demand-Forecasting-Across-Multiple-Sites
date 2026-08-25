from pathlib import Path

import pandas as pd
import plotly.express as px
import dash

from dash import (
    html,
    dcc,
    callback,
    Input,
    Output
)


# Register the page
dash.register_page(
    __name__,
    path="/forecast",
    name="Demand Forecast"
)


# Load the Random Forest forecast
file_path = (
    Path(__file__).resolve().parents[2]
    / "outputs"
    / "random_forest_forecasts.csv"
)

forecast_data = pd.read_csv(file_path)

forecast_data["date"] = pd.to_datetime(
    forecast_data["date"]
)

sites = sorted(
    forecast_data["site_id"].unique()
)


# Create a reusable metric card
def metric_card(label, card_id, note, colour):
    return html.Div([

        html.P(
            label,
            className="kpi-label"
        ),

        html.H3(
            "--",
            id=card_id
        ),

        html.P(
            note,
            className="kpi-note"
        )

    ], className=f"kpi-card {colour}")


# Page layout
layout = html.Div([

    # Page heading and site selector
    html.Div([

        html.Div([
            html.P(
                "FORECAST INTELLIGENCE",
                className="page-eyebrow"
            ),

            html.H2("Site demand forecast"),

            html.P(
                "Compare predicted and actual cement demand "
                "across the eight-week planning horizon.",
                className="page-description"
            )
        ]),

        html.Div([
            html.P(
                "SELECT SITE",
                className="selector-label"
            ),

            dcc.Dropdown(
                id="site-selector",
                options=[
                    {
                        "label": site,
                        "value": site
                    }
                    for site in sites
                ],
                value=sites[0],
                clearable=False,
                className="site-dropdown"
            )
        ], className="site-selector-card")

    ], className="forecast-header"),


    # Forecast metrics
    html.Div([

        metric_card(
            "SITE MAPE",
            "site-mape",
            "Non-zero demand days",
            "blue"
        ),

        metric_card(
            "SITE RMSE",
            "site-rmse",
            "Forecast error in tonnes",
            "purple"
        ),

        metric_card(
            "AVERAGE FORECAST",
            "average-forecast",
            "Average tonnes per day",
            "teal"
        ),

        metric_card(
            "PEAK FORECAST",
            "peak-forecast",
            "Highest predicted demand",
            "amber"
        )

    ], className="kpi-grid forecast-kpi-grid"),


    # Forecast chart
    html.Div([

        html.P(
            "SITE DEMAND SIGNAL",
            className="panel-eyebrow"
        ),

        html.H3(
            "Actual versus predicted demand"
        ),

        dcc.Graph(
            id="forecast-line-chart",
            config={
                "displayModeBar": False
            }
        )

    ], className=(
        "analytics-panel demand-panel "
        "forecast-chart-panel"
    ))

], className="overview-page forecast-page")


# Update the selected site's results
@callback(
    Output("forecast-line-chart", "figure"),
    Output("site-mape", "children"),
    Output("site-rmse", "children"),
    Output("average-forecast", "children"),
    Output("peak-forecast", "children"),
    Input("site-selector", "value")
)
def update_forecast(selected_site):

    site_data = forecast_data[
        forecast_data["site_id"] == selected_site
    ].sort_values("date")

    actual = site_data["consumed_tonnes"]
    predicted = site_data["predicted_tonnes"]

    non_zero = actual > 0

    if non_zero.any():
        mape = (
            (
                actual[non_zero]
                - predicted[non_zero]
            ).abs()
            / actual[non_zero]
        ).mean() * 100
    else:
        mape = 0

    rmse = (
        (
            actual - predicted
        ) ** 2
    ).mean() ** 0.5

    average_forecast = predicted.mean()
    peak_forecast = predicted.max()


    # Rename columns for the chart legend
    chart_data = site_data.rename(columns={
        "consumed_tonnes": "Actual Demand",
        "predicted_tonnes": "Forecast Demand"
    })


    # Build the chart
    figure = px.line(
        chart_data,
        x="date",
        y=[
            "Actual Demand",
            "Forecast Demand"
        ],
        color_discrete_map={
            "Actual Demand": "#91a2b6",
            "Forecast Demand": "#33d1b4"
        }
    )

    figure.update_traces(
        line=dict(width=3)
    )

    figure.update_layout(
        height=430,
        hovermode="x unified",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#91a2b6"),
        margin=dict(
            l=10,
            r=10,
            t=35,
            b=10
        ),
        legend=dict(
            orientation="h",
            title="",
            x=0,
            y=1.10
        )
    )

    figure.update_xaxes(
        title="",
        showgrid=False
    )

    figure.update_yaxes(
        title="Tonnes",
        gridcolor="rgba(151,171,196,0.10)"
    )


    return (
        figure,
        f"{mape:.2f}%",
        f"{rmse:.2f} t",
        f"{average_forecast:.2f} t",
        f"{peak_forecast:.2f} t"
    )