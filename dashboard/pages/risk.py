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
    path="/risk",
    name="Risk Monitor"
)


# Load the risk data
file_path = (
    Path(__file__).resolve().parents[2]
    / "outputs"
    / "risk_reorder_recommendations.csv"
)

risk_data = pd.read_csv(file_path)

risk_data["date"] = pd.to_datetime(
    risk_data["date"]
)

sites = sorted(
    risk_data["site_id"].unique()
)


# Risk colours
risk_colours = {
    "Normal": "#33d1b4",
    "Low Stock": "#f5b84b",
    "Stockout": "#ff667a",
    "Overcapacity": "#9b7cff"
}


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
                "RISK INTELLIGENCE",
                className="page-eyebrow"
            ),

            html.H2("Operational Risk Monitor"),

            html.P(
                "Identify when and where inventory conditions "
                "require immediate management attention.",
                className="page-description"
            )
        ]),

        html.Div([
            html.P(
                "SELECT SITE",
                className="selector-label"
            ),

            dcc.Dropdown(
                id="risk-site-selector",
                options=[
                    {
                        "label": "All Sites",
                        "value": "All Sites"
                    }
                ] + [
                    {
                        "label": site,
                        "value": site
                    }
                    for site in sites
                ],
                value="All Sites",
                clearable=False,
                className="site-dropdown"
            )
        ], className="site-selector-card")

    ], className="forecast-header"),


    # Risk metrics
    html.Div([

        metric_card(
            "STOCKOUT DAYS",
            "risk-stockout-days",
            "Critical inventory failures",
            "red"
        ),

        metric_card(
            "LOW-STOCK DAYS",
            "risk-low-stock-days",
            "Reorder threshold breaches",
            "amber"
        ),

        metric_card(
            "OVERCAPACITY DAYS",
            "risk-overcapacity-days",
            "Silo capacity breaches",
            "purple"
        ),

        metric_card(
            "NORMAL DAYS",
            "risk-normal-days",
            "Stable inventory positions",
            "teal"
        )

    ], className="kpi-grid forecast-kpi-grid"),


    # Daily risk trend
    html.Div([

        html.P(
            "RISK TIMELINE",
            className="panel-eyebrow"
        ),

        html.H3(
            "Daily inventory risk exposure"
        ),

        dcc.Graph(
            id="daily-risk-chart",
            config={
                "displayModeBar": False
            }
        )

    ], className=(
        "analytics-panel demand-panel "
        "forecast-chart-panel"
    )),


    # Site risk ranking
    html.Div([

        html.P(
            "SITE RISK RANKING",
            className="panel-eyebrow"
        ),

        html.H3(
            "Sites with the highest risk exposure"
        ),

        dcc.Graph(
            id="site-risk-ranking",
            config={
                "displayModeBar": False
            }
        )

    ], className=(
        "analytics-panel demand-panel "
        "forecast-chart-panel"
    ))

], className="overview-page")


# Update the Risk Monitor
@callback(
    Output("daily-risk-chart", "figure"),
    Output("site-risk-ranking", "figure"),
    Output("risk-stockout-days", "children"),
    Output("risk-low-stock-days", "children"),
    Output("risk-overcapacity-days", "children"),
    Output("risk-normal-days", "children"),
    Input("risk-site-selector", "value")
)
def update_risk_monitor(selected_site):

    if selected_site == "All Sites":
        filtered_data = risk_data.copy()
    else:
        filtered_data = risk_data[
            risk_data["site_id"] == selected_site
        ].copy()


    # Calculate risk totals
    risk_counts = (
        filtered_data["risk_status"]
        .value_counts()
    )

    stockout_days = risk_counts.get(
        "Stockout",
        0
    )

    low_stock_days = risk_counts.get(
        "Low Stock",
        0
    )

    overcapacity_days = risk_counts.get(
        "Overcapacity",
        0
    )

    normal_days = risk_counts.get(
        "Normal",
        0
    )


    # Prepare daily risk data
    daily_risk = (
        filtered_data
        .groupby(
            ["date", "risk_status"]
        )
        .size()
        .reset_index(name="Site-days")
    )


    # Build the daily risk chart
    daily_figure = px.bar(
        daily_risk,
        x="date",
        y="Site-days",
        color="risk_status",
        barmode="stack",
        color_discrete_map=risk_colours,
        category_orders={
            "risk_status": [
                "Normal",
                "Low Stock",
                "Stockout",
                "Overcapacity"
            ]
        }
    )

    daily_figure.update_layout(
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
        ),
        bargap=0.18
    )

    daily_figure.update_xaxes(
        title="",
        showgrid=False
    )

    daily_figure.update_yaxes(
        title="Site-days",
        gridcolor="rgba(151,171,196,0.10)"
    )


    # Prepare site risk ranking
    risk_records = filtered_data[
        filtered_data["risk_status"] != "Normal"
    ]

    site_ranking = (
        risk_records
        .groupby("site_id")
        .size()
        .reset_index(name="Risk Days")
        .sort_values(
            "Risk Days",
            ascending=False
        )
        .head(10)
        .sort_values("Risk Days")
    )


    # Build site ranking chart
    ranking_figure = px.bar(
        site_ranking,
        x="Risk Days",
        y="site_id",
        orientation="h",
        color="Risk Days",
        color_continuous_scale=[
            "#f5b84b",
            "#ff667a"
        ],
        text="Risk Days"
    )

    ranking_figure.update_traces(
        textposition="outside"
    )

    ranking_figure.update_layout(
        height=430,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#91a2b6"),
        margin=dict(
            l=10,
            r=40,
            t=25,
            b=10
        ),
        coloraxis_showscale=False
    )

    ranking_figure.update_xaxes(
        title="Risk site-days",
        gridcolor="rgba(151,171,196,0.10)"
    )

    ranking_figure.update_yaxes(
        title=""
    )


    return (
        daily_figure,
        ranking_figure,
        f"{stockout_days}",
        f"{low_stock_days}",
        f"{overcapacity_days}",
        f"{normal_days}"
    )