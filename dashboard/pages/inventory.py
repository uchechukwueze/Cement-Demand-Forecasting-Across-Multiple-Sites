from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
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
    path="/inventory",
    name="Inventory Control"
)


# Load the inventory data
file_path = (
    Path(__file__).resolve().parents[2]
    / "outputs"
    / "risk_reorder_recommendations.csv"
)

inventory_data = pd.read_csv(file_path)

inventory_data["date"] = pd.to_datetime(
    inventory_data["date"]
)

sites = sorted(
    inventory_data["site_id"].unique()
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
                "INVENTORY INTELLIGENCE",
                className="page-eyebrow"
            ),

            html.H2("Inventory Control"),

            html.P(
                "Monitor future inventory positions, capacity "
                "limits and supply movement for every site.",
                className="page-description"
            )
        ]),

        html.Div([
            html.P(
                "SELECT SITE",
                className="selector-label"
            ),

            dcc.Dropdown(
                id="inventory-site-selector",
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


    # Inventory metrics
    html.Div([

        metric_card(
            "STARTING INVENTORY",
            "starting-inventory",
            "Inventory at forecast start",
            "blue"
        ),

        metric_card(
            "MINIMUM INVENTORY",
            "minimum-inventory",
            "Lowest forecast position",
            "red"
        ),

        metric_card(
            "MAXIMUM INVENTORY",
            "maximum-inventory",
            "Highest forecast position",
            "teal"
        ),

        metric_card(
            "SILO CAPACITY",
            "site-capacity",
            "Maximum storage level",
            "amber"
        )

    ], className="kpi-grid forecast-kpi-grid"),


    # Inventory position chart
    html.Div([

        html.P(
            "INVENTORY POSITION",
            className="panel-eyebrow"
        ),

        html.H3(
            "Inventory versus reorder point and capacity"
        ),

        dcc.Graph(
            id="inventory-position-chart",
            config={
                "displayModeBar": False
            }
        )

    ], className=(
        "analytics-panel demand-panel "
        "forecast-chart-panel"
    )),


    # Supply movement chart
    html.Div([

        html.P(
            "SUPPLY MOVEMENT",
            className="panel-eyebrow"
        ),

        html.H3(
            "Deliveries versus forecast demand"
        ),

        dcc.Graph(
            id="inventory-flow-chart",
            config={
                "displayModeBar": False
            }
        )

    ], className=(
        "analytics-panel risk-panel "
        "forecast-chart-panel"
    ))

], className="overview-page")


# Update the selected site's inventory
@callback(
    Output("inventory-position-chart", "figure"),
    Output("inventory-flow-chart", "figure"),
    Output("starting-inventory", "children"),
    Output("minimum-inventory", "children"),
    Output("maximum-inventory", "children"),
    Output("site-capacity", "children"),
    Input("inventory-site-selector", "value")
)
def update_inventory(selected_site):

    site_data = inventory_data[
        inventory_data["site_id"] == selected_site
    ].sort_values("date")


    # Inventory metrics
    starting_inventory = (
        site_data["starting_inventory"].iloc[0]
    )

    minimum_inventory = (
        site_data["inventory_tonnes"].min()
    )

    maximum_inventory = (
        site_data["inventory_tonnes"].max()
    )

    silo_capacity = (
        site_data["silo_capacity"].iloc[0]
    )


    # Prepare the inventory chart
    chart_data = site_data.rename(columns={
        "inventory_tonnes": "Inventory",
        "reorder_point_tonnes": "Reorder Point",
        "silo_capacity": "Silo Capacity"
    })

    inventory_figure = px.line(
        chart_data,
        x="date",
        y=[
            "Inventory",
            "Reorder Point",
            "Silo Capacity"
        ],
        color_discrete_map={
            "Inventory": "#33d1b4",
            "Reorder Point": "#f5b84b",
            "Silo Capacity": "#4f8cff"
        }
    )

    inventory_figure.update_traces(
        line=dict(width=3)
    )

    for trace in inventory_figure.data:

        if trace.name == "Reorder Point":
            trace.update(
                line=dict(
                    width=2,
                    dash="dot"
                )
            )

        if trace.name == "Silo Capacity":
            trace.update(
                line=dict(
                    width=2,
                    dash="dash"
                )
            )

    inventory_figure.add_hline(
        y=0,
        line_color="#ff667a",
        line_dash="dot",
        annotation_text="Stockout boundary"
    )

    inventory_figure.update_layout(
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

    inventory_figure.update_xaxes(
        title="",
        showgrid=False
    )

    inventory_figure.update_yaxes(
        title="Tonnes",
        gridcolor="rgba(151,171,196,0.10)"
    )


    # Build the supply movement chart
    flow_figure = go.Figure()

    flow_figure.add_bar(
        x=site_data["date"],
        y=site_data["deliveries_tonnes"],
        name="Deliveries",
        marker_color="#4f8cff"
    )

    flow_figure.add_scatter(
        x=site_data["date"],
        y=site_data["predicted_tonnes"],
        name="Forecast Demand",
        mode="lines",
        line=dict(
            color="#33d1b4",
            width=3
        )
    )

    flow_figure.update_layout(
        height=390,
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

    flow_figure.update_xaxes(
        title="",
        showgrid=False
    )

    flow_figure.update_yaxes(
        title="Tonnes",
        gridcolor="rgba(151,171,196,0.10)"
    )


    return (
        inventory_figure,
        flow_figure,
        f"{starting_inventory:.2f} t",
        f"{minimum_inventory:.2f} t",
        f"{maximum_inventory:.2f} t",
        f"{silo_capacity:.0f} t"
    )