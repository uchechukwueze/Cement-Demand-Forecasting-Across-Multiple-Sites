from pathlib import Path

import pandas as pd
import plotly.express as px
import dash

from dash import (
    html,
    dcc,
    dash_table,
    callback,
    Input,
    Output
)


# Register the page
dash.register_page(
    __name__,
    path="/reorder",
    name="Reorder Recommendations"
)


# Load the reorder data
file_path = (
    Path(__file__).resolve().parents[2]
    / "outputs"
    / "risk_reorder_recommendations.csv"
)

reorder_data = pd.read_csv(file_path)

reorder_data["date"] = pd.to_datetime(
    reorder_data["date"]
)

forecast_dates = sorted(
    reorder_data["date"].unique()
)


# Dropdown date options
date_options = [
    {
        "label": pd.Timestamp(date).strftime(
            "%d %b %Y"
        ),
        "value": pd.Timestamp(date).strftime(
            "%Y-%m-%d"
        )
    }
    for date in forecast_dates
]


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

    # Page heading and date selector
    html.Div([

        html.Div([
            html.P(
                "REPLENISHMENT INTELLIGENCE",
                className="page-eyebrow"
            ),

            html.H2("Reorder Recommendations"),

            html.P(
                "Translate forecast inventory risks into "
                "clear daily supply actions and order quantities.",
                className="page-description"
            )
        ]),

        html.Div([
            html.P(
                "SELECT FORECAST DATE",
                className="selector-label"
            ),

            dcc.Dropdown(
                id="reorder-date-selector",
                options=date_options,
                value=date_options[0]["value"],
                clearable=False,
                className="site-dropdown"
            )
        ], className="site-selector-card")

    ], className="forecast-header"),


    # Reorder metrics
    html.Div([

        metric_card(
            "EMERGENCY REORDERS",
            "emergency-reorders",
            "Immediate replenishment",
            "red"
        ),

        metric_card(
            "STANDARD REORDERS",
            "standard-reorders",
            "Low-stock replenishment",
            "amber"
        ),

        metric_card(
            "PAUSED DELIVERIES",
            "paused-deliveries",
            "Overcapacity prevention",
            "purple"
        ),

        metric_card(
            "RECOMMENDED TONNES",
            "recommended-tonnes",
            "Total for selected date",
            "teal"
        )

    ], className="kpi-grid forecast-kpi-grid"),


    # Reorder quantity chart
    html.Div([

        html.P(
            "ORDER ALLOCATION",
            className="panel-eyebrow"
        ),

        html.H3(
            "Recommended reorder quantity by site"
        ),

        dcc.Graph(
            id="reorder-quantity-chart",
            config={
                "displayModeBar": False
            }
        )

    ], className=(
        "analytics-panel demand-panel "
        "forecast-chart-panel"
    )),


    # Daily action table
    html.Div([

        html.P(
            "DAILY ACTION QUEUE",
            className="panel-eyebrow"
        ),

        html.H3(
            "Site-level supply recommendations"
        ),

        dash_table.DataTable(
            id="reorder-action-table",

            columns=[
                {
                    "name": "Site",
                    "id": "site_id"
                },
                {
                    "name": "Cement Type",
                    "id": "cement_type"
                },
                {
                    "name": "Inventory",
                    "id": "inventory_tonnes"
                },
                {
                    "name": "Reorder Point",
                    "id": "reorder_point_tonnes"
                },
                {
                    "name": "Order Quantity",
                    "id": "reorder_quantity_tonnes"
                },
                {
                    "name": "Recommended Action",
                    "id": "recommended_action"
                }
            ],

            page_size=15,
            sort_action="native",

            style_table={
                "overflowX": "auto",
                "marginTop": "20px"
            },

            style_cell={
                "padding": "14px",
                "fontFamily": "Segoe UI",
                "fontSize": "12px",
                "textAlign": "left",
                "border": (
                    "1px solid "
                    "rgba(151,171,196,0.10)"
                )
            },

            style_header={
                "color": "#91a2b6",
                "fontWeight": "700",
                "backgroundColor": "#102437",
                "border": "none"
            },

            style_data={
                "color": "#f4f7fb",
                "backgroundColor": "#0d1c2b"
            },

            style_data_conditional=[

                {
                    "if": {
                        "filter_query": (
                            '{recommended_action} '
                            '= "Emergency Reorder"'
                        )
                    },
                    "color": "#ff8b9b",
                    "backgroundColor": (
                        "rgba(255,102,122,0.08)"
                    )
                },

                {
                    "if": {
                        "filter_query": (
                            '{recommended_action} '
                            '= "Place Reorder"'
                        )
                    },
                    "color": "#f5c765",
                    "backgroundColor": (
                        "rgba(245,184,75,0.07)"
                    )
                },

                {
                    "if": {
                        "filter_query": (
                            '{recommended_action} '
                            '= "Pause Delivery"'
                        )
                    },
                    "color": "#b6a2ff",
                    "backgroundColor": (
                        "rgba(155,124,255,0.07)"
                    )
                }

            ]
        )

    ], className=(
        "analytics-panel demand-panel "
        "forecast-chart-panel"
    ))

], className="overview-page")


# Update the Reorder Recommendations page
@callback(
    Output("reorder-quantity-chart", "figure"),
    Output("reorder-action-table", "data"),
    Output("emergency-reorders", "children"),
    Output("standard-reorders", "children"),
    Output("paused-deliveries", "children"),
    Output("recommended-tonnes", "children"),
    Input("reorder-date-selector", "value")
)
def update_reorder_page(selected_date):

    selected_date = pd.to_datetime(
        selected_date
    )

    day_data = reorder_data[
        reorder_data["date"] == selected_date
    ].copy()


    # Calculate daily action totals
    emergency_reorders = (
        day_data["recommended_action"]
        == "Emergency Reorder"
    ).sum()

    standard_reorders = (
        day_data["recommended_action"]
        == "Place Reorder"
    ).sum()

    paused_deliveries = (
        day_data["recommended_action"]
        == "Pause Delivery"
    ).sum()

    recommended_tonnes = (
        day_data["reorder_quantity_tonnes"]
        .sum()
    )


    # Keep only positive order quantities
    order_data = day_data[
        day_data["reorder_quantity_tonnes"] > 0
    ].sort_values(
        "reorder_quantity_tonnes",
        ascending=False
    )


    # Build reorder quantity chart
    reorder_figure = px.bar(
        order_data,
        x="site_id",
        y="reorder_quantity_tonnes",
        color="recommended_action",
        color_discrete_map={
            "Emergency Reorder": "#ff667a",
            "Place Reorder": "#f5b84b"
        },
        labels={
            "site_id": "Site",
            "reorder_quantity_tonnes": "Tonnes",
            "recommended_action": "Action"
        }
    )

    reorder_figure.update_layout(
        height=430,
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
        bargap=0.25
    )

    reorder_figure.update_xaxes(
        title="",
        showgrid=False
    )

    reorder_figure.update_yaxes(
        title="Recommended tonnes",
        gridcolor="rgba(151,171,196,0.10)"
    )


    # Prepare the daily action queue
    priority_order = {
        "Emergency Reorder": 1,
        "Place Reorder": 2,
        "Pause Delivery": 3,
        "No Action": 4
    }

    action_table = day_data[
        day_data["recommended_action"]
        != "No Action"
    ].copy()

    action_table["priority"] = (
        action_table["recommended_action"]
        .map(priority_order)
    )

    action_table = action_table.sort_values(
        [
            "priority",
            "reorder_quantity_tonnes"
        ],
        ascending=[
            True,
            False
        ]
    )

    numeric_columns = [
        "inventory_tonnes",
        "reorder_point_tonnes",
        "reorder_quantity_tonnes"
    ]

    action_table[numeric_columns] = (
        action_table[numeric_columns]
        .round(2)
    )


    return (
        reorder_figure,
        action_table.to_dict("records"),
        f"{emergency_reorders}",
        f"{standard_reorders}",
        f"{paused_deliveries}",
        f"{recommended_tonnes:,.2f} t"
    )