import dash
from dash import Dash, html, dcc


# Create the dashboard
app = Dash(
    __name__,
    use_pages=True
)

server = app.server

app.title = "MIG Cement Control Tower"


# Main dashboard structure
app.layout = html.Div([

    # Sidebar
    html.Aside([

        html.Div([

            html.Div(
                "M",
                className="brand-mark"
            ),

            html.Div([
                html.H2("MIG"),
                html.P("Cement Intelligence")
            ])

        ], className="brand"),

        html.P(
            "CONTROL TOWER",
            className="nav-label"
        ),

        html.Nav([

            dcc.Link(
                "Executive Overview",
                href="/",
                className="nav-link"
            ),

            dcc.Link(
                "Demand Forecast",
                href="/forecast",
                className="nav-link"
            ),

            dcc.Link(
                "Inventory Control",
                href="/inventory",
                className="nav-link"
            ),

            dcc.Link(
                "Risk Monitor",
                href="/risk",
                className="nav-link"
            ),

            dcc.Link(
                "Reorder Recommendations",
                href="/reorder",
                className="nav-link"
            ),

            dcc.Link(
                "Site Drilldown",
                href="/site",
                className="nav-link"
            ),

            dcc.Link(
                "Scenario Simulator",
                href="/scenario",
                className="nav-link"
            )

        ]),

        html.Div([

            html.Span(
                className="status-dot"
            ),

            html.Span(
                "Forecast engine online"
            )

        ], className="system-status")

    ], className="sidebar"),


    # Main dashboard
    html.Main([

        html.Header([

            html.Div([

                html.P(
                    "MIG CEMENT OPERATIONS",
                    className="topbar-label"
                ),

                html.H1(
                    "Intelligence & Inventory Control Tower"
                )

            ]),

            html.Div(
                "LIVE FORECAST",
                className="live-badge"
            )

        ], className="topbar"),

        html.Div(
            dash.page_container,
            className="page-content"
        )

    ], className="main-panel")

], className="app-shell")


if __name__ == "__main__":
    app.run(debug=True)
