import dash_bootstrap_components as dbc
from dash import dcc, html

SYMBOLS = ["BTCUSDT", "ETHUSDT"]

def create_layout():
    return dbc.Container([
        # Header
        dbc.Row([
            dbc.Col(html.H1("Binance Futures Trading Dashboard", style={"text-align": "center", "margin-top": "20px", "color": "#ffffff"}), width=12)
        ], style={"background-color": "#000000"}),
        
        # Wallet Overviews and Risk Indicators in the same row
        dbc.Row([
            dbc.Col([
                html.H3("Wallet Overviews", style={"margin-top": "20px", "color": "#3498db"}),
                dcc.Interval(id='interval-component', interval=10*1000, n_intervals=0),
                dcc.Graph(id='waterfall-graph', config={'displayModeBar': False}),
            ], width=6),
            dbc.Col([
                html.H3("Risk Indicators", style={"margin-top": "20px", "color": "#3498db"}),
                html.Div(id='risk-indicators')
            ], width=6)
        ], style={"background-color": "#1a1a1a"}),
        
        # Data Table
        dbc.Row([
            dbc.Col([
                html.H3("Data Table", style={"margin-top": "20px", "color": "#3498db"}),
                html.Div(id="position-table")
            ], width=12)
        ], style={"background-color": "#1a1a1a"}),
        
        # OHLC Graph and Order Form
        dbc.Row([
            dbc.Col([
                html.H1("Graphique", style={"margin-top": "20px", "color": "#ffffff"}),
                dcc.Graph(id='ohlc-graph')
            ], width=10),
            dbc.Col([
                html.H1("Placer un ordre", style={"margin-top": "20px", "color": "#ffffff"}),
                dbc.Row([
                    dbc.Col([
                        dbc.Label([
                            "Symbol",
                            html.Span(className="fas fa-chart-line", style={"margin-left": "10px", "color": "#3498db"})
                        ], style={"color": "#ffffff"}),
                        dcc.Dropdown(SYMBOLS, id='order-symbol', value="BTCUSDT", style={"background-color": "#1a1a1a", "color": "#ffffff"})
                    ], width=12)
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Label([
                            "Quantité/Unit",
                            html.Span(className="fas fa-sort-numeric-up", style={"margin-left": "10px", "color": "#3498db"})
                        ], style={"color": "#ffffff"}),
                        dcc.Input(id='order-quantity', type='number', style={"background-color": "#1a1a1a", "color": "#ffffff"})
                    ], width=12)
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Label([
                            "Stop Loss",
                            html.Span(className="fas fa-stop-circle", style={"margin-left": "10px", "color": "#3498db"})
                        ], style={"color": "#ffffff"}),
                        dcc.Input(id='order-stop_loss', type='number', style={"background-color": "#1a1a1a", "color": "#ffffff"})
                    ], width=12)
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Label([
                            "Take Profit",
                            html.Span(className="fas fa-coins", style={"margin-left": "10px", "color": "#3498db"})
                        ], style={"color": "#ffffff"}),
                        dcc.Input(id='order-take_profit', type='number', style={"background-color": "#1a1a1a", "color": "#ffffff"})
                    ], width=12)
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Label([
                            "Levier",
                            html.Span(className="fas fa-balance-scale", style={"margin-left": "10px", "color": "#3498db"})
                        ], style={"color": "#ffffff"}),
                        dcc.Slider(min=1, max=30, step=None, marks={i: str(i) for i in [1, 5, 10, 15, 20, 25, 30]}, id='order-leverage', tooltip={"always_visible": True, "placement": "bottom"})
                    ], width=12)
                ]),
                html.Div(id='order-preview'),
                dbc.Row([
                    dbc.Col([
                        dbc.Button([
                            "Long",
                            html.Span(className="fas fa-arrow-up", style={"margin-left": "10px"})
                        ], id='order-long', color="success", n_clicks=0, style={"margin-top": "10px", "width": "100%"})
                    ], width=6),
                    dbc.Col([
                        dbc.Button([
                            "Short",
                            html.Span(className="fas fa-arrow-down", style={"margin-left": "10px"})
                        ], id='order-short', color="danger", n_clicks=0, style={"margin-top": "10px", "width": "100%"})
                    ], width=6)
                ]),
                html.H4("Order result", style={"margin-top": "20px", "color": "#ffffff"}),
                html.Div(id='order-result')
            ], width=2)
        ], style={"background-color": "#1a1a1a"}),
        
        # Alert dialog
        dcc.ConfirmDialog(
            id='order-alert',
            message=''
        ),
        
        # Modals
        dbc.Modal(
            [
                dbc.ModalHeader("Order Information"),
                dbc.ModalBody("Detailed information about the order will be displayed here."),
                dbc.ModalFooter(
                    dbc.Button("Close", id="close-order-info", className="ml-auto")
                ),
            ],
            id="modal-order-info",
            is_open=False,
        )
    ], fluid=True, style={"background-color": "#000000"})
