# layout.py

import pandas as pd
import dash_bootstrap_components as dbc
from dash import dcc, html
from app.utils import SYMBOLS

def create_navbar():
    return dbc.Navbar(
        dbc.Container(
            [
                dbc.NavbarBrand("Binance Futures Trading Dashboard", href="/", className="text-white"),
                dbc.Nav(
                    [
                        dbc.NavItem(dbc.NavLink("Global", href="/global", className="text-white")),
                        dbc.NavItem(dbc.NavLink("Place Order", href="/place-order", className="text-white")),
                    ],
                    className="ml-auto",
                    navbar=True,
                ),
            ],
            fluid=True,
        ),
        color="dark",
        dark=True,
        sticky="top",
    )

def create_layout():
    return dbc.Container([
        create_navbar(),
        dbc.Row([
            dbc.Col(html.H1("Binance Futures Trading Dashboard", className="text-center mb-4 text-white"), width=12)
        ], className="mt-4"),
        
        # ------------------------------------------
        dbc.Row([
            dbc.Col([
                html.H3([
                    html.I(className="fas fa-chart-line me-2"),
                    "Wallet Overviews"
                ], className="text-white"),
                dcc.Interval(id='interval-component', interval=10*1000, n_intervals=0),
                dcc.Graph(id='waterfall-graph', config={'displayModeBar': False}),
            ], width=6),
            dbc.Col(html.Div(id='risk-indicators'), width=6)
        ], className="mt-4"),
        
        dbc.Row([
            dbc.Col([
                html.H3([
                    html.I(className="fas fa-chart-line me-2"),
                    "Positions Actuelles"
                ], className="text-white"),
                html.Div(id='positions-table', className="text-white")
            ], width=12)
        ], className="mt-4"),
        
        # ------------------------------------------

        dbc.Row([
            dbc.Col([
                html.H3([
                    html.I(className="fas fa-wallet me-2"),
                    "OHLC"
                ], className="text-white"),
                dcc.Graph(id='ohlc-graph', config={'displayModeBar': False})
            ], width=10),  # 70% width
            dbc.Col([
                html.H3([
                    html.I(className="fas fa-hand-holding-usd me-2"),
                    "Placer un Ordre"
                ], className="text-white"),
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Symbole", className="text-white"),
                        dcc.Dropdown(SYMBOLS, id='order-symbol', value='BTCUSDT', className="bg-dark text-white")
                    ], width=12)
                ], className="mb-2"),
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Type d'ordre", className="text-white"),
                        dcc.RadioItems(
                            id='order-type',
                            options=[
                                {'label': 'Market', 'value': 'MARKET'},
                                {'label': 'Limit', 'value': 'LIMIT'}
                            ],
                            value='MARKET',
                            className="bg-dark text-white")
                    ], width=12)
                ], className="mb-2"),
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Quantité/Unit", className="text-white"),
                        dcc.Input(id='order-quantity', type='number', className="bg-dark text-white")
                    ], width=12)
                ], className="mb-2"),
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Limit Price", className="text-white"),
                        dcc.Input(id='order-price', type='number', className="bg-dark text-white")
                    ], width=12)
                ], className="mb-2"),
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Cours Actuel", className="text-white"),
                        html.Div(id='current-price', className="text-white mt-2")
                    ], width=12)
                ], className="mb-2"),
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Stop Loss", className="text-white"),
                        dcc.Input(id='order-SL', type='number', className="bg-dark text-white")
                    ], width=6),
                    dbc.Col([
                        dbc.Label("Take Profit", className="text-white"),
                        dcc.Input(id='order-TP', type='number', className="bg-dark text-white")
                    ], width=6)
                ], className="mb-2"),
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Levier", className="text-white"),
                        dcc.Slider(1, 20, 4, id='order-leverage', className='bg-dark text-white')
                    ], width=12)
                ], className="mb-2"),
                html.Div(id='order-preview', className="text-white mt-2"),
                dbc.Row([
                    dbc.Col([
                        dbc.Button("Long", id='order-long', color="success", n_clicks=0, className="me-2")
                    ], width=6),
                    dbc.Col([
                        dbc.Button("Short", id='order-short', color="danger", n_clicks=0, className="me-2")
                    ], width=6)
                ]),
                html.Div(id='order-result', className="text-white mt-2")
            ], width=2)  # 30% width
        ], className="mt-4"),
        dbc.Row([
            dbc.Col([
                html.H3([
                    html.I(className="fas fa-list-alt me-2"),
                    "Événements"
                ], className="text-white"),
                html.Div(id='events-div', className="text-white")
            ], width=12)
        ], className="mt-4")
    ], fluid=True)
