from pathlib import Path

import pandas as pd
import plotly.express as px
import dash

from dash import (
    html,
    dcc
)


# Register the page
dash.register_page(
    __name__,
    path="/",
    name="Executive Overview"
)


# Locate the project folder
project_root = (
    Path(__file__)
    .resolve()
    .parents[2]
)


# Load risk and inventory results
risk_data = pd.read_csv(
    project_root
    / "outputs"
    / "risk_reorder_recommendations.csv"
)


# Load model evaluation results
model_results = pd.read_csv(
    project_root
    / "outputs"
    / "model_comparison.csv"
)


# Convert the date column
risk_data["date"] = pd.to_datetime(
    risk_data["date"]
)


# Calculate overview metrics
total_sites = (
    risk_data["site_id"]
    .nunique()
)

forecast_days = (
    risk_data["date"]
    .nunique()
)

stockout_days = (
    risk_data["risk_status"]
    == "Stockout"
).sum()

capacity_alerts = (
    risk_data["risk_status"]
    == "Overcapacity"
).sum()


# Identify the best-performing model
best_result = model_results.loc[
    model_results["MAPE (%)"].idxmin()
]

best_model = best_result["Model"]

best_mape = best_result["MAPE (%)"]


# Prepare daily demand
daily_demand = (
    risk_data
    .groupby(
        "date",
        as_index=False
    )[
        [
            "consumed_tonnes",
            "predicted_tonnes"
        ]
    ]
    .sum()
    .rename(columns={
        "consumed_tonnes": (
            "Actual Demand"
        ),
        "predicted_tonnes": (
            "Forecast Demand"
        )
    })
)


# Create demand chart
demand_figure = px.line(
    daily_demand,
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

demand_figure.update_traces(
    line=dict(
        width=3
    )
)

demand_figure.update_layout(
    height=320,
    hovermode="x unified",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(
        color="#91a2b6"
    ),
    margin=dict(
        l=10,
        r=10,
        t=30,
        b=10
    ),
    legend=dict(
        orientation="h",
        title="",
        x=0,
        y=1.12
    )
)

demand_figure.update_xaxes(
    title="",
    showgrid=False
)

demand_figure.update_yaxes(
    title="Tonnes",
    gridcolor=(
        "rgba(151,171,196,0.10)"
    )
)


# Risk category order
risk_order = [
    "Stockout",
    "Low Stock",
    "Overcapacity",
    "Normal"
]


# Risk category colours
risk_colours = {
    "Normal": "#33d1b4",
    "Low Stock": "#f5b84b",
    "Stockout": "#ff667a",
    "Overcapacity": "#9b7cff"
}


# Transparent backgrounds for risk cards
risk_backgrounds = {
    "Normal": "rgba(51,209,180,0.07)",
    "Low Stock": "rgba(245,184,75,0.07)",
    "Stockout": "rgba(255,102,122,0.07)",
    "Overcapacity": "rgba(155,124,255,0.07)"
}


# Prepare risk summary
risk_summary = (
    risk_data["risk_status"]
    .value_counts()
    .reindex(
        risk_order,
        fill_value=0
    )
    .rename_axis("Status")
    .reset_index(
        name="Site-days"
    )
)

total_site_days = len(risk_data)

risk_summary["Percentage"] = (
    risk_summary["Site-days"]
    / total_site_days
    * 100
)


# Create inventory-status donut
risk_figure = px.pie(
    risk_summary,
    names="Status",
    values="Site-days",
    hole=0.56,
    color="Status",
    category_orders={
        "Status": risk_order
    },
    color_discrete_map=risk_colours
)

risk_figure.update_traces(
    textinfo="percent",
    textposition="inside",
    textfont=dict(
        size=16,
        color="#dce6f2"
    ),
    sort=False,
    direction="clockwise",
    marker=dict(
        line=dict(
            color="#0d1c2b",
            width=3
        )
    ),
    hovertemplate=(
        "<b>%{label}</b><br>"
        "%{value:,} site-days<br>"
        "%{percent}"
        "<extra></extra>"
    )
)

risk_figure.update_layout(
    height=430,
    autosize=True,
    showlegend=False,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(
        color="#91a2b6"
    ),
    margin=dict(
        l=5,
        r=5,
        t=5,
        b=5
    ),
    uniformtext_minsize=12,
    uniformtext_mode="hide"
)

risk_figure.add_annotation(
    x=0.5,
    y=0.5,
    text=(
        f"<b>{total_site_days:,}</b>"
        "<br>SITE-DAYS"
    ),
    showarrow=False,
    align="center",
    font=dict(
        size=18,
        color="#f4f7fb"
    )
)


# Risk summary lookup
risk_count_lookup = (
    risk_summary
    .set_index("Status")[
        "Site-days"
    ]
    .to_dict()
)

risk_percentage_lookup = (
    risk_summary
    .set_index("Status")[
        "Percentage"
    ]
    .to_dict()
)


# Create a reusable risk-status item
def risk_status_item(status):

    count = int(
        risk_count_lookup.get(
            status,
            0
        )
    )

    percentage = (
        risk_percentage_lookup.get(
            status,
            0
        )
    )

    colour = risk_colours[status]

    background = (
        risk_backgrounds[status]
    )

    return html.Div([

        html.Div([

            html.Span(
                style={
                    "display": "inline-block",
                    "width": "10px",
                    "height": "10px",
                    "borderRadius": "50%",
                    "backgroundColor": colour,
                    "boxShadow": (
                        f"0 0 12px {colour}"
                    ),
                    "flexShrink": "0"
                }
            ),

            html.Div([

                html.Strong(
                    status,
                    style={
                        "display": "block",
                        "color": "#f4f7fb",
                        "fontSize": "14px"
                    }
                ),

                html.Span(
                    f"{count:,} site-days",
                    style={
                        "color": "#91a2b6",
                        "fontSize": "12px"
                    }
                )

            ])

        ], style={
            "display": "flex",
            "alignItems": "center",
            "gap": "12px"
        }),

        html.Strong(
            f"{percentage:.1f}%",
            style={
                "color": colour,
                "fontSize": "20px"
            }
        )

    ], style={
        "display": "flex",
        "alignItems": "center",
        "justifyContent": "space-between",
        "gap": "20px",
        "padding": "15px 16px",
        "border": (
            "1px solid "
            "rgba(151,171,196,0.12)"
        ),
        "borderLeft": (
            f"3px solid {colour}"
        ),
        "borderRadius": "12px",
        "background": background
    })


# Reusable KPI card
def kpi_card(
    label,
    value,
    note,
    colour
):

    return html.Div([

        html.P(
            label,
            className="kpi-label"
        ),

        html.H3(
            value
        ),

        html.P(
            note,
            className="kpi-note"
        )

    ], className=f"kpi-card {colour}")


# Page layout
layout = html.Div([

    # Executive heading
    html.Div([

        html.Div([

            html.P(
                "EXECUTIVE COMMAND VIEW",
                className="page-eyebrow"
            ),

            html.H2(
                "Operational intelligence "
                "at a glance"
            ),

            html.P(
                "Monitor demand forecasts, "
                "inventory exposure and recommended "
                "supply actions across every site.",
                className="page-description"
            )

        ]),

        html.Div([

            html.Strong(
                f"{forecast_days}-DAY"
            ),

            html.Span(
                "PLANNING HORIZON"
            )

        ], className="horizon-badge")

    ], className="overview-hero"),


    # KPI cards
    html.Div([

        kpi_card(
            "SITES MONITORED",
            f"{total_sites}",
            "Active cement operations",
            "teal"
        ),

        kpi_card(
            "BEST MODEL",
            best_model,
            f"{best_mape:.2f}% MAPE",
            "blue"
        ),

        kpi_card(
            "FORECAST HORIZON",
            f"{forecast_days} days",
            "Forward inventory outlook",
            "purple"
        ),

        kpi_card(
            "STOCKOUT ALERTS",
            f"{stockout_days}",
            "Critical site-days",
            "red"
        ),

        kpi_card(
            "CAPACITY ALERTS",
            f"{capacity_alerts}",
            "Overcapacity site-days",
            "amber"
        )

    ], className="kpi-grid"),


    # Analytics section
    html.Div([

        # Demand panel
        html.Div([

            html.P(
                "DEMAND SIGNAL",
                className="panel-eyebrow"
            ),

            html.H3(
                "Forecast versus actual demand"
            ),

            dcc.Graph(
                figure=demand_figure,
                config={
                    "displayModeBar": False,
                    "responsive": True
                },
                style={
                    "width": "100%"
                }
            )

        ], className=(
            "analytics-panel demand-panel"
        )),


        # Risk panel
        html.Div([

            html.P(
                "RISK EXPOSURE",
                className="panel-eyebrow"
            ),

            html.H3(
                "Inventory status distribution"
            ),

            html.Div([

                # Large donut
                html.Div([

                    dcc.Graph(
                        figure=risk_figure,
                        config={
                            "displayModeBar": False,
                            "responsive": True
                        },
                        style={
                            "width": "100%",
                            "height": "430px"
                        }
                    )

                ], style={
                    "width": "100%",
                    "minWidth": "0"
                }),


                # Detailed status breakdown
                html.Div([

                    html.P(
                        "STATUS BREAKDOWN",
                        className="panel-eyebrow"
                    ),

                    html.H4(
                        "Exposure by category",
                        style={
                            "margin": "0 0 8px",
                            "color": "#f4f7fb",
                            "fontSize": "18px"
                        }
                    ),

                    html.P(
                        "Distribution across all "
                        "monitored site-days.",
                        style={
                            "margin": "0 0 18px",
                            "color": "#91a2b6",
                            "fontSize": "12px"
                        }
                    ),

                    html.Div([

                        risk_status_item(
                            "Stockout"
                        ),

                        risk_status_item(
                            "Low Stock"
                        ),

                        risk_status_item(
                            "Overcapacity"
                        ),

                        risk_status_item(
                            "Normal"
                        )

                    ], style={
                        "display": "grid",
                        "gap": "10px"
                    })

                ], style={
                    "width": "100%",
                    "minWidth": "0",
                    "padding": "20px",
                    "border": (
                        "1px solid "
                        "rgba(151,171,196,0.10)"
                    ),
                    "borderRadius": "16px",
                    "background": (
                        "rgba(7,20,32,0.28)"
                    )
                })

            ], style={
                "display": "grid",
                "gridTemplateColumns": (
                    "repeat("
                    "auto-fit, "
                    "minmax(320px, 1fr)"
                    ")"
                ),
                "alignItems": "center",
                "gap": "30px",
                "width": "100%",
                "marginTop": "8px"
            })

        ], className=(
            "analytics-panel risk-panel"
        ))

    ], className="analytics-grid")

], className="overview-page")