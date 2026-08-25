from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
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
    path="/site",
    name="Site Drilldown"
)


# Locate the project folder
project_root = (
    Path(__file__)
    .resolve()
    .parents[2]
)


# Locate the output files
forecast_path = (
    project_root
    / "outputs"
    / "random_forest_forecasts.csv"
)

operations_path = (
    project_root
    / "outputs"
    / "risk_reorder_recommendations.csv"
)


# Load the datasets
forecast_data = pd.read_csv(
    forecast_path
)

operations_data = pd.read_csv(
    operations_path
)


# Remove accidental spaces from column names
forecast_data.columns = (
    forecast_data.columns.str.strip()
)

operations_data.columns = (
    operations_data.columns.str.strip()
)


# Convert dates
forecast_data["date"] = pd.to_datetime(
    forecast_data["date"]
)

operations_data["date"] = pd.to_datetime(
    operations_data["date"]
)


# Keep sites available in both datasets
sites = sorted(
    set(forecast_data["site_id"])
    & set(operations_data["site_id"])
)


# Initial site selection
default_site = sites[0]


# Cement types available at the first site
default_cement_types = sorted(
    operations_data.loc[
        operations_data["site_id"]
        == default_site,
        "cement_type"
    ].dropna().unique()
)

default_cement_type = (
    default_cement_types[0]
)


# Create a reusable metric card
def metric_card(
    label,
    card_id,
    note,
    colour
):

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


# Apply consistent dashboard chart styling
def style_chart(
    figure,
    height=420
):

    figure.update_layout(
        height=height,
        hovermode="x unified",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            color="#91a2b6"
        ),
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
        gridcolor=(
            "rgba(151,171,196,0.10)"
        )
    )

    return figure


# Page layout
layout = html.Div([

    # Page heading and selectors
    html.Div([

        html.Div([

            html.P(
                "SITE-LEVEL INTELLIGENCE",
                className="page-eyebrow"
            ),

            html.H2(
                "Site Drilldown"
            ),

            html.P(
                "Review site-wide demand alongside "
                "cement-type inventory, risk and "
                "recommended operational actions.",
                className="page-description"
            )

        ]),

        html.Div([

            # Site selector
            html.Div([

                html.P(
                    "SELECT SITE",
                    className="selector-label"
                ),

                dcc.Dropdown(
                    id="drilldown-site-selector",
                    options=[
                        {
                            "label": site,
                            "value": site
                        }
                        for site in sites
                    ],
                    value=default_site,
                    clearable=False,
                    className="site-dropdown"
                )

            ]),

            # Cement-type selector
            html.Div([

                html.P(
                    "SELECT CEMENT TYPE",
                    className="selector-label"
                ),

                dcc.Dropdown(
                    id="drilldown-cement-selector",
                    options=[
                        {
                            "label": cement_type,
                            "value": cement_type
                        }
                        for cement_type
                        in default_cement_types
                    ],
                    value=default_cement_type,
                    clearable=False,
                    className="site-dropdown"
                )

            ], style={
                "marginTop": "14px"
            })

        ], className="site-selector-card")

    ], className="forecast-header"),


    # Site metrics
    html.Div([

        metric_card(
            "HORIZON FORECAST",
            "drilldown-total-forecast",
            "Total site forecast demand",
            "blue"
        ),

        metric_card(
            "PEAK DAILY FORECAST",
            "drilldown-peak-forecast",
            "Highest site forecast day",
            "purple"
        ),

        metric_card(
            "MINIMUM INVENTORY",
            "drilldown-minimum-inventory",
            "Lowest selected-type position",
            "red"
        ),

        metric_card(
            "RISK DAYS",
            "drilldown-risk-days",
            "Selected-type exception days",
            "amber"
        )

    ], className=(
        "kpi-grid forecast-kpi-grid"
    )),


    # Demand chart
    html.Div([

        html.P(
            "DEMAND PERFORMANCE",
            className="panel-eyebrow"
        ),

        html.H3(
            "Site-wide actual versus forecast demand"
        ),

        dcc.Graph(
            id="drilldown-demand-chart",
            config={
                "displayModeBar": False
            }
        )

    ], className=(
        "analytics-panel demand-panel "
        "forecast-chart-panel"
    )),


    # Inventory chart
    html.Div([

        html.P(
            "INVENTORY OUTLOOK",
            className="panel-eyebrow"
        ),

        html.H3(
            "Projected inventory, reorder point "
            "and silo capacity"
        ),

        dcc.Graph(
            id="drilldown-inventory-chart",
            config={
                "displayModeBar": False
            }
        )

    ], className=(
        "analytics-panel demand-panel "
        "forecast-chart-panel"
    )),


    # Risk and action table
    html.Div([

        html.P(
            "SITE ACTION QUEUE",
            className="panel-eyebrow"
        ),

        html.H3(
            "Upcoming risk days and "
            "recommended actions"
        ),

        html.P(
            "Only exception days are displayed. "
            "An empty table means the selected "
            "cement type has no projected risk.",
            className="kpi-note"
        ),

        dash_table.DataTable(

            id="drilldown-action-table",

            columns=[

                {
                    "name": "Date",
                    "id": "date"
                },

                {
                    "name": "Inventory (t)",
                    "id": "inventory_tonnes"
                },

                {
                    "name": "Reorder Point (t)",
                    "id": "reorder_point_tonnes"
                },

                {
                    "name": "Risk Status",
                    "id": "risk_status"
                },

                {
                    "name": "Order Quantity (t)",
                    "id": (
                        "reorder_quantity_tonnes"
                    )
                },

                {
                    "name": "Recommended Action",
                    "id": "recommended_action"
                }

            ],

            page_size=12,

            sort_action="native",

            style_table={
                "overflowX": "auto",
                "marginTop": "18px"
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
                            '{risk_status} '
                            '= "Stockout"'
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
                            '{risk_status} '
                            '= "Low Stock"'
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
                            '{risk_status} '
                            '= "Overcapacity"'
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


# Update cement types when the site changes
@callback(
    Output(
        "drilldown-cement-selector",
        "options"
    ),
    Output(
        "drilldown-cement-selector",
        "value"
    ),
    Input(
        "drilldown-site-selector",
        "value"
    )
)
def update_cement_types(
    selected_site
):

    cement_types = sorted(
        operations_data.loc[
            operations_data["site_id"]
            == selected_site,
            "cement_type"
        ].dropna().unique()
    )

    options = [
        {
            "label": cement_type,
            "value": cement_type
        }
        for cement_type in cement_types
    ]

    return (
        options,
        cement_types[0]
    )


# Update the complete Site Drilldown page
@callback(
    Output(
        "drilldown-demand-chart",
        "figure"
    ),
    Output(
        "drilldown-inventory-chart",
        "figure"
    ),
    Output(
        "drilldown-total-forecast",
        "children"
    ),
    Output(
        "drilldown-peak-forecast",
        "children"
    ),
    Output(
        "drilldown-minimum-inventory",
        "children"
    ),
    Output(
        "drilldown-risk-days",
        "children"
    ),
    Output(
        "drilldown-action-table",
        "data"
    ),
    Input(
        "drilldown-site-selector",
        "value"
    ),
    Input(
        "drilldown-cement-selector",
        "value"
    )
)
def update_site_drilldown(
    selected_site,
    selected_cement_type
):

    # Cement types available at the site
    available_types = sorted(
        operations_data.loc[
            operations_data["site_id"]
            == selected_site,
            "cement_type"
        ].dropna().unique()
    )

    # Handle the brief change between sites
    if (
        selected_cement_type
        not in available_types
    ):
        selected_cement_type = (
            available_types[0]
        )


    # Demand forecasts are aggregated by site.
    # Therefore, cement_type is not used here.
    demand_rows = forecast_data[
        forecast_data["site_id"]
        == selected_site
    ].sort_values("date")


    # Inventory and risk retain cement type.
    operations_rows = operations_data[
        (
            operations_data["site_id"]
            == selected_site
        )
        & (
            operations_data["cement_type"]
            == selected_cement_type
        )
    ].sort_values("date")


    # Calculate metrics
    total_forecast = (
        demand_rows[
            "predicted_tonnes"
        ].sum()
    )

    peak_forecast = (
        demand_rows[
            "predicted_tonnes"
        ].max()
    )

    minimum_inventory = (
        operations_rows[
            "inventory_tonnes"
        ].min()
    )

    risk_statuses = [
        "Low Stock",
        "Stockout",
        "Overcapacity"
    ]

    risk_days = (
        operations_rows["risk_status"]
        .isin(risk_statuses)
        .sum()
    )


    # Create demand chart
    demand_figure = go.Figure()

    demand_figure.add_scatter(
        x=demand_rows["date"],
        y=demand_rows["consumed_tonnes"],
        name="Actual Demand",
        mode="lines",
        line=dict(
            color="#91a2b6",
            width=3
        )
    )

    demand_figure.add_scatter(
        x=demand_rows["date"],
        y=demand_rows["predicted_tonnes"],
        name="Forecast Demand",
        mode="lines",
        line=dict(
            color="#33d1b4",
            width=3
        )
    )

    demand_figure = style_chart(
        demand_figure
    )


    # Create inventory chart
    inventory_figure = go.Figure()

    inventory_figure.add_scatter(
        x=operations_rows["date"],
        y=operations_rows[
            "inventory_tonnes"
        ],
        name="Inventory",
        mode="lines",
        line=dict(
            color="#33d1b4",
            width=3
        )
    )

    inventory_figure.add_scatter(
        x=operations_rows["date"],
        y=operations_rows[
            "reorder_point_tonnes"
        ],
        name="Reorder Point",
        mode="lines",
        line=dict(
            color="#f5b84b",
            width=2,
            dash="dot"
        )
    )

    inventory_figure.add_scatter(
        x=operations_rows["date"],
        y=operations_rows[
            "silo_capacity"
        ],
        name="Silo Capacity",
        mode="lines",
        line=dict(
            color="#4f8cff",
            width=2,
            dash="dash"
        )
    )

    inventory_figure.add_hline(
        y=0,
        line_color="#ff667a",
        line_dash="dot",
        annotation_text=(
            "Stockout boundary"
        )
    )

    inventory_figure = style_chart(
        inventory_figure
    )


    # Prepare the exception table
    action_table = operations_rows[
        operations_rows["risk_status"]
        .isin(risk_statuses)
    ].copy()

    action_table["date"] = (
        action_table["date"]
        .dt.strftime("%Y-%m-%d")
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


    # Return the updated content
    return (
        demand_figure,
        inventory_figure,
        f"{total_forecast:,.2f} t",
        f"{peak_forecast:,.2f} t",
        f"{minimum_inventory:,.2f} t",
        f"{risk_days}",
        action_table.to_dict("records")
    )