from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import dash

from dash import (
    html,
    dcc,
    callback,
    Input,
    Output,
    ctx
)


# Register the page
dash.register_page(
    __name__,
    path="/scenario",
    name="Scenario Simulator"
)


# Load scenario data
project_root = (
    Path(__file__)
    .resolve()
    .parents[2]
)

file_path = (
    project_root
    / "outputs"
    / "risk_reorder_recommendations.csv"
)

scenario_data = pd.read_csv(
    file_path
)

scenario_data.columns = (
    scenario_data.columns.str.strip()
)

scenario_data["date"] = pd.to_datetime(
    scenario_data["date"]
)


# Prepare initial selections
sites = sorted(
    scenario_data["site_id"]
    .dropna()
    .unique()
)

default_site = sites[0]

default_cement_types = sorted(
    scenario_data.loc[
        scenario_data["site_id"]
        == default_site,
        "cement_type"
    ].dropna().unique()
)

default_cement_type = (
    default_cement_types[0]
)


# Reusable KPI card
def metric_card(
    label,
    value_id,
    delta_id,
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
            id=value_id
        ),

        html.P(
            "--",
            id=delta_id,
            style={
                "margin": "4px 0 7px",
                "fontSize": "11px",
                "fontWeight": "700"
            }
        ),

        html.P(
            note,
            className="kpi-note"
        )

    ], className=f"kpi-card {colour}")


# Reusable scenario preset button
def preset_button(
    title,
    description,
    button_id,
    colour
):

    return html.Button([

        html.Strong(
            title,
            style={
                "display": "block",
                "fontSize": "13px"
            }
        ),

        html.Span(
            description,
            style={
                "display": "block",
                "marginTop": "4px",
                "fontSize": "10px",
                "opacity": "0.78"
            }
        )

    ],
        id=button_id,
        n_clicks=0,
        style={
            "width": "100%",
            "padding": "13px 14px",
            "color": colour,
            "textAlign": "left",
            "cursor": "pointer",
            "border": (
                f"1px solid {colour}"
            ),
            "borderRadius": "11px",
            "background": (
                "rgba(13,28,43,0.78)"
            )
        }
    )


# Apply common chart styling
def style_chart(
    figure,
    height=440
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
            t=40,
            b=10
        ),
        legend=dict(
            orientation="h",
            title="",
            x=0,
            y=1.11
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


# Calculate sequential inventory
def calculate_inventory(
    starting_inventory,
    deliveries,
    demand
):

    current_inventory = float(
        starting_inventory
    )

    inventory_values = []

    for delivery, daily_demand in zip(
        deliveries,
        demand
    ):

        current_inventory = (
            current_inventory
            + float(delivery)
            - float(daily_demand)
        )

        inventory_values.append(
            current_inventory
        )

    return inventory_values


# Calculate inventory-risk conditions
def calculate_risk_masks(
    inventory,
    reorder_point,
    capacity
):

    stockout_mask = (
        inventory < 0
    )

    overcapacity_mask = (
        inventory > capacity
    )

    low_stock_mask = (
        (inventory >= 0)
        & (inventory <= reorder_point)
    )

    risk_mask = (
        stockout_mask
        | overcapacity_mask
        | low_stock_mask
    )

    return (
        stockout_mask,
        low_stock_mask,
        overcapacity_mask,
        risk_mask
    )


# Format inventory changes
def inventory_delta_label(
    difference
):

    if abs(difference) < 0.005:
        difference = 0

    if difference > 0:
        colour = "#33d1b4"
    elif difference < 0:
        colour = "#ff667a"
    else:
        colour = "#91a2b6"

    return html.Span(
        f"{difference:+,.2f} t vs baseline",
        style={
            "color": colour
        }
    )


# Format risk-day changes
def risk_delta_label(
    difference
):

    difference = int(
        difference
    )

    if difference < 0:
        colour = "#33d1b4"
    elif difference > 0:
        colour = "#ff667a"
    else:
        colour = "#91a2b6"

    return html.Span(
        f"{difference:+d} days vs baseline",
        style={
            "color": colour
        }
    )


# Create management-banner styling
def conclusion_style(
    colour,
    background
):

    return {
        "marginTop": "22px",
        "padding": "24px 28px",
        "border": (
            f"1px solid {colour}"
        ),
        "borderLeft": (
            f"5px solid {colour}"
        ),
        "borderRadius": "16px",
        "background": background,
        "boxShadow": (
            "0 18px 45px "
            "rgba(0,0,0,0.16)"
        )
    }


# Create intervention summary item
def intervention_item(
    label,
    value_id
):

    return html.Div([

        html.P(
            label,
            style={
                "margin": "0 0 7px",
                "color": "#91a2b6",
                "fontSize": "9px",
                "fontWeight": "700",
                "letterSpacing": "0.12em"
            }
        ),

        html.Strong(
            "--",
            id=value_id,
            style={
                "display": "block",
                "color": "#f4f7fb",
                "fontSize": "17px"
            }
        )

    ], style={
        "padding": "14px 16px",
        "border": (
            "1px solid "
            "rgba(151,171,196,0.12)"
        ),
        "borderRadius": "11px",
        "background": (
            "rgba(7,20,32,0.28)"
        )
    })


# Page layout
layout = html.Div([

    # Heading and selectors
    html.Div([

        html.Div([

            html.P(
                "WHAT-IF INTELLIGENCE",
                className="page-eyebrow"
            ),

            html.H2(
                "Scenario Simulator"
            ),

            html.P(
                "Stress-test how changes in demand, "
                "delivery quantities and supply timing "
                "affect future inventory and risk.",
                className="page-description"
            )

        ]),

        html.Div([

            html.Div([

                html.P(
                    "SELECT SITE",
                    className="selector-label"
                ),

                dcc.Dropdown(
                    id="scenario-site-selector",
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

            html.Div([

                html.P(
                    "SELECT CEMENT TYPE",
                    className="selector-label"
                ),

                dcc.Dropdown(
                    id="scenario-cement-selector",
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


    # One-click scenario presets
    html.Div([

        html.P(
            "QUICK SCENARIOS",
            className="panel-eyebrow"
        ),

        html.H3(
            "Apply a predefined operating stress test"
        ),

        html.Div([

            preset_button(
                "Demand Surge",
                "+20% forecast demand",
                "preset-demand-surge",
                "#33d1b4"
            ),

            preset_button(
                "Supply Disruption",
                "-25% deliveries · 3-day delay",
                "preset-supply-disruption",
                "#ff667a"
            ),

            preset_button(
                "Recovery Plan",
                "+25% planned deliveries",
                "preset-recovery-plan",
                "#4f8cff"
            ),

            preset_button(
                "Reset to Baseline",
                "Return every control to zero",
                "reset-scenario-button",
                "#91a2b6"
            )

        ], style={
            "display": "grid",
            "gridTemplateColumns": (
                "repeat("
                "auto-fit, "
                "minmax(170px, 1fr)"
                ")"
            ),
            "gap": "12px",
            "marginTop": "16px"
        })

    ], className=(
        "analytics-panel forecast-chart-panel"
    )),


    # Manual scenario controls
    html.Div([

        html.Div([

            html.P(
                "DEMAND ASSUMPTION",
                className="panel-eyebrow"
            ),

            html.H3(
                "Forecast demand adjustment"
            ),

            html.P(
                id="demand-change-value",
                className="kpi-note"
            ),

            dcc.Slider(
                id="demand-change-slider",
                min=-30,
                max=50,
                step=5,
                value=0,
                marks={
                    -30: "-30%",
                    -15: "-15%",
                    0: "0%",
                    15: "+15%",
                    30: "+30%",
                    50: "+50%"
                },
                tooltip={
                    "placement": "bottom",
                    "always_visible": False
                }
            )

        ], className="analytics-panel"),


        html.Div([

            html.P(
                "SUPPLY ASSUMPTION",
                className="panel-eyebrow"
            ),

            html.H3(
                "Planned delivery adjustment"
            ),

            html.P(
                id="delivery-change-value",
                className="kpi-note"
            ),

            dcc.Slider(
                id="delivery-change-slider",
                min=-50,
                max=50,
                step=5,
                value=0,
                marks={
                    -50: "-50%",
                    -25: "-25%",
                    0: "0%",
                    25: "+25%",
                    50: "+50%"
                },
                tooltip={
                    "placement": "bottom",
                    "always_visible": False
                }
            )

        ], className="analytics-panel"),


        html.Div([

            html.P(
                "TIMING ASSUMPTION",
                className="panel-eyebrow"
            ),

            html.H3(
                "Delivery delay"
            ),

            html.P(
                id="delivery-delay-value",
                className="kpi-note"
            ),

            dcc.Slider(
                id="delivery-delay-slider",
                min=0,
                max=7,
                step=1,
                value=0,
                marks={
                    0: "0",
                    1: "1",
                    3: "3",
                    5: "5",
                    7: "7 days"
                },
                tooltip={
                    "placement": "bottom",
                    "always_visible": False
                }
            )

        ], className="analytics-panel")

    ], style={
        "display": "grid",
        "gridTemplateColumns": (
            "repeat("
            "auto-fit, "
            "minmax(270px, 1fr)"
            ")"
        ),
        "gap": "20px",
        "marginTop": "22px"
    }),


    # Scenario metrics
    html.Div([

        metric_card(
            "ENDING INVENTORY",
            "scenario-ending-inventory",
            "scenario-ending-delta",
            "Inventory at horizon end",
            "blue"
        ),

        metric_card(
            "MINIMUM INVENTORY",
            "scenario-minimum-inventory",
            "scenario-minimum-delta",
            "Lowest scenario position",
            "red"
        ),

        metric_card(
            "STOCKOUT DAYS",
            "scenario-stockout-days",
            "scenario-stockout-delta",
            "Days below zero inventory",
            "purple"
        ),

        metric_card(
            "TOTAL RISK DAYS",
            "scenario-risk-days",
            "scenario-risk-delta",
            "All scenario exceptions",
            "amber"
        )

    ], className=(
        "kpi-grid forecast-kpi-grid"
    )),


    # Management assessment
    html.Div([

        html.P(
            "MANAGEMENT ASSESSMENT",
            className="panel-eyebrow"
        ),

        html.H3(
            id="scenario-conclusion-title",
            style={
                "margin": "8px 0 10px"
            }
        ),

        html.P(
            id="scenario-conclusion-message",
            style={
                "margin": "0",
                "maxWidth": "1050px",
                "color": "#b7c5d5",
                "fontSize": "14px",
                "lineHeight": "1.7"
            }
        ),

        html.Div([

            intervention_item(
                "RECOMMENDED ACTION",
                "scenario-intervention-action"
            ),

            intervention_item(
                "QUANTITY ADJUSTMENT",
                "scenario-intervention-quantity"
            ),

            intervention_item(
                "ACTION DEADLINE",
                "scenario-intervention-date"
            )

        ], style={
            "display": "grid",
            "gridTemplateColumns": (
                "repeat("
                "auto-fit, "
                "minmax(190px, 1fr)"
                ")"
            ),
            "gap": "12px",
            "marginTop": "20px"
        })

    ],
        id="scenario-conclusion-banner",
        style=conclusion_style(
            "#91a2b6",
            "rgba(145,162,182,0.06)"
        )
    ),


    # Inventory comparison
    html.Div([

        html.P(
            "SCENARIO COMPARISON",
            className="panel-eyebrow"
        ),

        html.H3(
            "Baseline versus scenario inventory"
        ),

        dcc.Graph(
            id="scenario-inventory-chart",
            config={
                "displayModeBar": False,
                "responsive": True
            },
            style={
                "width": "100%"
            }
        )

    ], className=(
        "analytics-panel demand-panel "
        "forecast-chart-panel"
    )),


    # Scenario operating flow
    html.Div([

        html.P(
            "ADJUSTED OPERATING FLOW",
            className="panel-eyebrow"
        ),

        html.H3(
            "Scenario deliveries versus demand"
        ),

        dcc.Graph(
            id="scenario-flow-chart",
            config={
                "displayModeBar": False,
                "responsive": True
            },
            style={
                "width": "100%"
            }
        )

    ], className=(
        "analytics-panel demand-panel "
        "forecast-chart-panel"
    ))

], className="overview-page")


# Update cement-type options
@callback(
    Output(
        "scenario-cement-selector",
        "options"
    ),
    Output(
        "scenario-cement-selector",
        "value"
    ),
    Input(
        "scenario-site-selector",
        "value"
    )
)
def update_scenario_cement_types(
    selected_site
):

    cement_types = sorted(
        scenario_data.loc[
            scenario_data["site_id"]
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


# Apply presets or reset the simulator
@callback(
    Output(
        "demand-change-slider",
        "value"
    ),
    Output(
        "delivery-change-slider",
        "value"
    ),
    Output(
        "delivery-delay-slider",
        "value"
    ),

    Input(
        "preset-demand-surge",
        "n_clicks"
    ),
    Input(
        "preset-supply-disruption",
        "n_clicks"
    ),
    Input(
        "preset-recovery-plan",
        "n_clicks"
    ),
    Input(
        "reset-scenario-button",
        "n_clicks"
    ),

    prevent_initial_call=True
)
def apply_scenario_preset(
    demand_clicks,
    disruption_clicks,
    recovery_clicks,
    reset_clicks
):

    triggered_button = (
        ctx.triggered_id
    )

    if (
        triggered_button
        == "preset-demand-surge"
    ):
        return (
            20,
            0,
            0
        )

    if (
        triggered_button
        == "preset-supply-disruption"
    ):
        return (
            0,
            -25,
            3
        )

    if (
        triggered_button
        == "preset-recovery-plan"
    ):
        return (
            0,
            25,
            0
        )

    return (
        0,
        0,
        0
    )


# Update the complete scenario analysis
@callback(
    Output(
        "scenario-inventory-chart",
        "figure"
    ),
    Output(
        "scenario-flow-chart",
        "figure"
    ),

    Output(
        "scenario-ending-inventory",
        "children"
    ),
    Output(
        "scenario-ending-delta",
        "children"
    ),

    Output(
        "scenario-minimum-inventory",
        "children"
    ),
    Output(
        "scenario-minimum-delta",
        "children"
    ),

    Output(
        "scenario-stockout-days",
        "children"
    ),
    Output(
        "scenario-stockout-delta",
        "children"
    ),

    Output(
        "scenario-risk-days",
        "children"
    ),
    Output(
        "scenario-risk-delta",
        "children"
    ),

    Output(
        "demand-change-value",
        "children"
    ),
    Output(
        "delivery-change-value",
        "children"
    ),
    Output(
        "delivery-delay-value",
        "children"
    ),

    Output(
        "scenario-conclusion-title",
        "children"
    ),
    Output(
        "scenario-conclusion-message",
        "children"
    ),
    Output(
        "scenario-conclusion-banner",
        "style"
    ),

    Output(
        "scenario-intervention-action",
        "children"
    ),
    Output(
        "scenario-intervention-quantity",
        "children"
    ),
    Output(
        "scenario-intervention-date",
        "children"
    ),

    Input(
        "scenario-site-selector",
        "value"
    ),
    Input(
        "scenario-cement-selector",
        "value"
    ),
    Input(
        "demand-change-slider",
        "value"
    ),
    Input(
        "delivery-change-slider",
        "value"
    ),
    Input(
        "delivery-delay-slider",
        "value"
    )
)
def update_scenario(
    selected_site,
    selected_cement_type,
    demand_change,
    delivery_change,
    delivery_delay
):

    demand_change = (
        demand_change or 0
    )

    delivery_change = (
        delivery_change or 0
    )

    delivery_delay = int(
        delivery_delay or 0
    )


    # Handle the brief change between sites
    available_types = sorted(
        scenario_data.loc[
            scenario_data["site_id"]
            == selected_site,
            "cement_type"
        ].dropna().unique()
    )

    if (
        selected_cement_type
        not in available_types
    ):
        selected_cement_type = (
            available_types[0]
        )


    # Filter the selected operation
    site_rows = scenario_data[
        (
            scenario_data["site_id"]
            == selected_site
        )
        & (
            scenario_data["cement_type"]
            == selected_cement_type
        )
    ].sort_values("date").copy()


    # Starting inventory
    starting_inventory = float(
        site_rows[
            "starting_inventory"
        ].iloc[0]
    )


    # Calculate baseline inventory
    site_rows["baseline_inventory"] = (
        calculate_inventory(
            starting_inventory,
            site_rows[
                "deliveries_tonnes"
            ],
            site_rows[
                "predicted_tonnes"
            ]
        )
    )


    # Apply scenario assumptions
    demand_factor = (
        1 + demand_change / 100
    )

    delivery_factor = (
        1 + delivery_change / 100
    )

    site_rows["scenario_demand"] = (
        site_rows["predicted_tonnes"]
        * demand_factor
    )

    adjusted_deliveries = (
        site_rows["deliveries_tonnes"]
        * delivery_factor
    )

    site_rows["scenario_deliveries"] = (
        adjusted_deliveries.shift(
            periods=delivery_delay,
            fill_value=0
        )
    )


    # Calculate scenario inventory
    site_rows["scenario_inventory"] = (
        calculate_inventory(
            starting_inventory,
            site_rows[
                "scenario_deliveries"
            ],
            site_rows[
                "scenario_demand"
            ]
        )
    )


    # Baseline risk
    (
        baseline_stockout_mask,
        baseline_low_stock_mask,
        baseline_overcapacity_mask,
        baseline_risk_mask
    ) = calculate_risk_masks(
        site_rows[
            "baseline_inventory"
        ],
        site_rows[
            "reorder_point_tonnes"
        ],
        site_rows[
            "silo_capacity"
        ]
    )


    # Scenario risk
    (
        scenario_stockout_mask,
        scenario_low_stock_mask,
        scenario_overcapacity_mask,
        scenario_risk_mask
    ) = calculate_risk_masks(
        site_rows[
            "scenario_inventory"
        ],
        site_rows[
            "reorder_point_tonnes"
        ],
        site_rows[
            "silo_capacity"
        ]
    )


    # Baseline metrics
    baseline_ending_inventory = (
        site_rows[
            "baseline_inventory"
        ].iloc[-1]
    )

    baseline_minimum_inventory = (
        site_rows[
            "baseline_inventory"
        ].min()
    )

    baseline_stockout_days = int(
        baseline_stockout_mask.sum()
    )

    baseline_risk_days = int(
        baseline_risk_mask.sum()
    )


    # Scenario metrics
    scenario_ending_inventory = (
        site_rows[
            "scenario_inventory"
        ].iloc[-1]
    )

    scenario_minimum_inventory = (
        site_rows[
            "scenario_inventory"
        ].min()
    )

    scenario_stockout_days = int(
        scenario_stockout_mask.sum()
    )

    scenario_low_stock_days = int(
        scenario_low_stock_mask.sum()
    )

    scenario_overcapacity_days = int(
        scenario_overcapacity_mask.sum()
    )

    scenario_risk_days = int(
        scenario_risk_mask.sum()
    )


    # Differences from baseline
    ending_difference = (
        scenario_ending_inventory
        - baseline_ending_inventory
    )

    minimum_difference = (
        scenario_minimum_inventory
        - baseline_minimum_inventory
    )

    stockout_difference = (
        scenario_stockout_days
        - baseline_stockout_days
    )

    risk_difference = (
        scenario_risk_days
        - baseline_risk_days
    )


    # Build inventory comparison chart
    inventory_figure = go.Figure()


    # Shade negative-inventory area
    chart_minimum = min(
        baseline_minimum_inventory,
        scenario_minimum_inventory,
        0
    )

    if chart_minimum < 0:

        lower_boundary = (
            chart_minimum
            - max(
                abs(chart_minimum) * 0.12,
                5
            )
        )

        inventory_figure.add_hrect(
            y0=lower_boundary,
            y1=0,
            fillcolor=(
                "rgba(255,102,122,0.09)"
            ),
            line_width=0,
            layer="below"
        )


    # Reorder threshold with amber shading
    inventory_figure.add_scatter(
        x=site_rows["date"],
        y=site_rows[
            "reorder_point_tonnes"
        ],
        name="Low-stock Zone",
        mode="lines",
        fill="tozeroy",
        fillcolor=(
            "rgba(245,184,75,0.08)"
        ),
        line=dict(
            color="#f5b84b",
            width=2,
            dash="dot"
        )
    )


    # Silo capacity
    inventory_figure.add_scatter(
        x=site_rows["date"],
        y=site_rows[
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


    # Baseline inventory
    inventory_figure.add_scatter(
        x=site_rows["date"],
        y=site_rows[
            "baseline_inventory"
        ],
        name="Baseline Inventory",
        mode="lines",
        line=dict(
            color="#91a2b6",
            width=3
        )
    )


    # Scenario inventory
    inventory_figure.add_scatter(
        x=site_rows["date"],
        y=site_rows[
            "scenario_inventory"
        ],
        name="Scenario Inventory",
        mode="lines",
        line=dict(
            color="#33d1b4",
            width=3
        )
    )


    # Stockout boundary
    inventory_figure.add_hline(
        y=0,
        line_color="#ff667a",
        line_dash="dot",
        annotation_text=(
            "Stockout boundary"
        )
    )


    # Mark first stockout
    if scenario_stockout_days > 0:

        first_stockout_index = (
            site_rows.loc[
                scenario_stockout_mask
            ].index[0]
        )

        first_stockout_date = (
            site_rows.loc[
                first_stockout_index,
                "date"
            ]
        )

        first_stockout_value = (
            site_rows.loc[
                first_stockout_index,
                "scenario_inventory"
            ]
        )

        inventory_figure.add_scatter(
            x=[
                first_stockout_date
            ],
            y=[
                first_stockout_value
            ],
            name="First Stockout",
            mode="markers+text",
            text=[
                "First stockout"
            ],
            textposition="top left",
            marker=dict(
                color="#ff667a",
                size=13,
                symbol="x",
                line=dict(
                    width=2
                )
            ),
            hovertemplate=(
                "<b>First stockout</b><br>"
                "%{x|%d %b %Y}<br>"
                "%{y:.2f} tonnes"
                "<extra></extra>"
            )
        )


    # Mark worst scenario point
    worst_index = (
        site_rows[
            "scenario_inventory"
        ].idxmin()
    )

    worst_date = site_rows.loc[
        worst_index,
        "date"
    ]

    worst_value = site_rows.loc[
        worst_index,
        "scenario_inventory"
    ]

    worst_colour = (
        "#ff667a"
        if worst_value < 0
        else "#f5b84b"
    )

    inventory_figure.add_scatter(
        x=[
            worst_date
        ],
        y=[
            worst_value
        ],
        name="Worst Scenario Point",
        mode="markers+text",
        text=[
            "Worst point"
        ],
        textposition="bottom right",
        marker=dict(
            color=worst_colour,
            size=13,
            symbol="diamond",
            line=dict(
                color="#f4f7fb",
                width=1
            )
        ),
        hovertemplate=(
            "<b>Worst scenario point</b><br>"
            "%{x|%d %b %Y}<br>"
            "%{y:.2f} tonnes"
            "<extra></extra>"
        )
    )

    inventory_figure = style_chart(
        inventory_figure
    )


    # Build operating-flow chart
    flow_figure = go.Figure()

    flow_figure.add_bar(
        x=site_rows["date"],
        y=site_rows[
            "scenario_deliveries"
        ],
        name="Scenario Deliveries",
        marker_color="#4f8cff"
    )

    flow_figure.add_scatter(
        x=site_rows["date"],
        y=site_rows[
            "scenario_demand"
        ],
        name="Scenario Demand",
        mode="lines",
        line=dict(
            color="#33d1b4",
            width=3
        )
    )

    flow_figure = style_chart(
        flow_figure
    )


    # Management assessment and intervention
    if scenario_stockout_days > 0:

        first_stockout_timestamp = (
            site_rows.loc[
                scenario_stockout_mask,
                "date"
            ].iloc[0]
        )

        first_stockout_text = (
            first_stockout_timestamp
            .strftime("%d %b %Y")
        )

        additional_supply = abs(
            min(
                scenario_minimum_inventory,
                0
            )
        )

        conclusion_title = (
            "Critical: stockout exposure"
        )

        conclusion_message = (
            f"Inventory falls below zero on "
            f"{scenario_stockout_days} days. "
            f"The first projected stockout occurs "
            f"on {first_stockout_text}. At least "
            f"{additional_supply:,.2f} tonnes of "
            f"cumulative additional supply must "
            f"arrive before this date to remove "
            f"the modelled deficit."
        )

        if scenario_overcapacity_days > 0:

            conclusion_message += (
                f" Because this scenario also creates "
                f"{scenario_overcapacity_days} "
                f"overcapacity days, split or "
                f"reschedule the intervention rather "
                f"than delivering it as one shipment."
            )

        intervention_action = (
            "Emergency replenishment"
        )

        intervention_quantity = (
            f"+{additional_supply:,.2f} t"
        )

        intervention_date = (
            f"Before {first_stockout_text}"
        )

        banner_colour = "#ff667a"

        banner_background = (
            "rgba(255,102,122,0.07)"
        )


    elif scenario_overcapacity_days > 0:

        first_overcapacity_timestamp = (
            site_rows.loc[
                scenario_overcapacity_mask,
                "date"
            ].iloc[0]
        )

        first_overcapacity_text = (
            first_overcapacity_timestamp
            .strftime("%d %b %Y")
        )

        maximum_excess = (
            (
                site_rows[
                    "scenario_inventory"
                ]
                - site_rows[
                    "silo_capacity"
                ]
            )
            .clip(lower=0)
            .max()
        )

        conclusion_title = (
            "Warning: overcapacity exposure"
        )

        conclusion_message = (
            f"Projected inventory exceeds silo "
            f"capacity on "
            f"{scenario_overcapacity_days} days. "
            f"Reduce, split or postpone at least "
            f"{maximum_excess:,.2f} tonnes before "
            f"the first breach on "
            f"{first_overcapacity_text}."
        )

        intervention_action = (
            "Reduce or postpone delivery"
        )

        intervention_quantity = (
            f"-{maximum_excess:,.2f} t"
        )

        intervention_date = (
            f"Before {first_overcapacity_text}"
        )

        banner_colour = "#9b7cff"

        banner_background = (
            "rgba(155,124,255,0.07)"
        )


    elif scenario_low_stock_days > 0:

        first_low_stock_timestamp = (
            site_rows.loc[
                scenario_low_stock_mask,
                "date"
            ].iloc[0]
        )

        first_low_stock_text = (
            first_low_stock_timestamp
            .strftime("%d %b %Y")
        )

        buffer_gap = (
            (
                site_rows[
                    "reorder_point_tonnes"
                ]
                - site_rows[
                    "scenario_inventory"
                ]
            )
            .where(
                scenario_low_stock_mask,
                0
            )
            .clip(lower=0)
            .max()
        )

        conclusion_title = (
            "Caution: reorder threshold breach"
        )

        conclusion_message = (
            f"Inventory remains above zero but "
            f"falls below the reorder threshold "
            f"on {scenario_low_stock_days} days. "
            f"Add approximately "
            f"{buffer_gap:,.2f} tonnes before "
            f"{first_low_stock_text} to restore "
            f"the operating buffer."
        )

        intervention_action = (
            "Standard replenishment"
        )

        intervention_quantity = (
            f"+{buffer_gap:,.2f} t"
        )

        intervention_date = (
            f"Before {first_low_stock_text}"
        )

        banner_colour = "#f5b84b"

        banner_background = (
            "rgba(245,184,75,0.07)"
        )


    else:

        conclusion_title = (
            "Stable: scenario remains within limits"
        )

        conclusion_message = (
            "The selected scenario produces no "
            "stockout, low-stock or overcapacity "
            "days across the forecast horizon. "
            "Inventory remains within the defined "
            "operating boundaries."
        )

        intervention_action = (
            "No intervention required"
        )

        intervention_quantity = (
            "0.00 t"
        )

        intervention_date = (
            "No deadline"
        )

        banner_colour = "#33d1b4"

        banner_background = (
            "rgba(51,209,180,0.07)"
        )


    # Return updated results
    return (
        inventory_figure,
        flow_figure,

        f"{scenario_ending_inventory:,.2f} t",
        inventory_delta_label(
            ending_difference
        ),

        f"{scenario_minimum_inventory:,.2f} t",
        inventory_delta_label(
            minimum_difference
        ),

        f"{scenario_stockout_days}",
        risk_delta_label(
            stockout_difference
        ),

        f"{scenario_risk_days}",
        risk_delta_label(
            risk_difference
        ),

        (
            f"Current demand adjustment: "
            f"{demand_change:+.0f}%"
        ),

        (
            f"Current delivery adjustment: "
            f"{delivery_change:+.0f}%"
        ),

        (
            f"Current delivery delay: "
            f"{delivery_delay} "
            f"{'day' if delivery_delay == 1 else 'days'}"
        ),

        conclusion_title,
        conclusion_message,

        conclusion_style(
            banner_colour,
            banner_background
        ),

        intervention_action,
        intervention_quantity,
        intervention_date
    )