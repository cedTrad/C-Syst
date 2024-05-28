import dash_bootstrap_components as dbc
from dash import dcc, html
import pandas as pd

def create_layout():
    return dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Binance Futures Trading Dashboard", className="text-center mb-4 text-light"), width=12)
        ], className="mt-4"),
        dbc.Row([
            dbc.Col([
                html.H3([
                    html.I(className="fas fa-chart-line me-2"),
                    "Positions Actuelles"
                ], className="text-light"),
                dcc.Interval(id='interval-component', interval=10*1000, n_intervals=0),
                html.Div(id='positions-div', className="text-light")
            ], width=6),
            dbc.Col([
                html.H3([
                    html.I(className="fas fa-balance-scale me-2"),
                    "Statistiques du PnL"
                ], className="text-light"),
                html.Div(id='pnl-div', className="text-light")
            ], width=6)
        ], className="mt-4"),
        dbc.Row([
            dbc.Col([
                html.H3([
                    html.I(className="fas fa-history me-2"),
                    "Historique des Positions"
                ], className="text-light"),
                dcc.DatePickerRange(
                    id='date-picker-range',
                    start_date=pd.to_datetime('today') - pd.DateOffset(days=30),
                    end_date=pd.to_datetime('today'),
                    className="bg-dark text-light"
                ),
                html.Button(id='submit-button', n_clicks=0, children='Afficher l\'historique', className="btn btn-secondary mt-2"),
                html.Div(id='history-div', className="text-light mt-4")
            ], width=12)
        ], className="mt-4"),
        dbc.Row([
            dbc.Col([
                html.H3([
                    html.I(className="fas fa-chart-bar me-2"),
                    "Graphiques"
                ], className="text-light"),
                dcc.Graph(id='history-graph', config={'displayModeBar': False})
            ], width=12)
        ], className="mt-4"),
        dbc.Row([
            dbc.Col([
                html.H3([
                    html.I(className="fas fa-wallet me-2"),
                    "Actifs Détenus"
                ], className="text-light"),
                dcc.Interval(id='interval-positions-component', interval=10*1000, n_intervals=0),
                html.Div(id='assets-div', className="text-light")
            ], width=12)
        ], className="mt-4"),
        dbc.Row([
            dbc.Col([
                html.H3([
                    html.I(className="fas fa-hand-holding-usd me-2"),
                    "Placer un Ordre"
                ], className="text-light"),
                html.Div([
                    dbc.Label("Symbole", className="text-light"),
                    dcc.Input(id='order-symbol', type='text', value='BTCUSDT', className="bg-dark text-light"),
                    dbc.Label("Côté", className="text-light"),
                    dbc.Button("Long", id='order-long', color="success", className="me-2"),
                    dbc.Button("Short", id='order-short', color="danger"),
                    dbc.Label("Type d'ordre", className="text-light"),
                    dcc.Dropdown(
                        id='order-type',
                        options=[
                            {'label': 'Market', 'value': 'MARKET'},
                            {'label': 'Limit', 'value': 'LIMIT'}
                        ],
                        value='MARKET',
                        className="bg-dark text-light"
                    ),
                    dbc.Label("Quantité", className="text-light"),
                    dcc.Input(id='order-quantity', type='number', value=0.001, className="bg-dark text-light"),
                    dbc.Label("Prix (pour les ordres limit)", className="text-light"),
                    dcc.Input(id='order-price', type='number', className="bg-dark text-light"),
                    dbc.Label("Levier", className="text-light"),
                    dcc.Input(id='order-leverage', type='number', value=1, className="bg-dark text-light"),
                    html.Div(id='order-preview', className="text-light mt-2"),
                    html.Button(id='submit-order', n_clicks=0, children='Placer l\'ordre', className="btn btn-primary mt-2"),
                    html.Div(id='order-result', className="text-light mt-2")
                ])
            ], width=12)
        ], className="mt-4"),
        dbc.Row([
            dbc.Col([
                html.H3([
                    html.I(className="fas fa-list-alt me-2"),
                    "Événements"
                ], className="text-light"),
                html.Div(id='events-div', className="text-light")
            ], width=12)
        ], className="mt-4")
    ], fluid=True)
