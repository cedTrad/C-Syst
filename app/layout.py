import pandas as pd
import dash_bootstrap_components as dbc
from dash import dcc, html

def create_layout():
    return dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Binance Trading Dashboard", className="text-center mb-4"), width=12)
        ]),
        dbc.Row([
            dbc.Col([
                html.H3("Positions Actuelles"),
                dcc.Interval(id='interval-component', interval=10*1000, n_intervals=0),
                html.Div(id='positions-div')
            ], width=6),
            dbc.Col([
                html.H3("Statistiques du PnL"),
                html.Div(id='pnl-div')
            ], width=6)
        ]),
        dbc.Row([
            dbc.Col([
                html.H3("Historique des Positions"),
                dcc.DatePickerRange(
                    id='date-picker-range',
                    start_date=pd.to_datetime('today') - pd.DateOffset(days=30),
                    end_date=pd.to_datetime('today')
                ),
                html.Button(id='submit-button', n_clicks=0, children='Afficher l\'historique'),
                html.Div(id='history-div')
            ], width=12)
        ]),
        dbc.Row([
            dbc.Col([
                html.H3("Graphiques"),
                dcc.Graph(id='history-graph')
            ], width=12)
        ]),
        dbc.Row([
            dbc.Col([
                html.H3("Actifs Détenus"),
                dcc.Interval(id='interval-positions-component', interval=10*1000, n_intervals=0),
                html.Div(id='assets-div')
            ], width=12)
        ]),
        dbc.Row([
            dbc.Col([
                html.H3("Placer un Ordre"),
                html.Div([
                    dbc.Label("Symbole"),
                    dcc.Input(id='order-symbol', type='text', value='BTCUSDT'),
                    dbc.Label("Côté"),
                    dcc.Dropdown(
                        id='order-side',
                        options=[
                            {'label': 'Achat', 'value': 'BUY'},
                            {'label': 'Vente', 'value': 'SELL'}
                        ],
                        value='BUY'
                    ),
                    dbc.Label("Type d'ordre"),
                    dcc.Dropdown(
                        id='order-type',
                        options=[
                            {'label': 'Market', 'value': 'MARKET'},
                            {'label': 'Limit', 'value': 'LIMIT'}
                        ],
                        value='MARKET'
                    ),
                    dbc.Label("Quantité"),
                    dcc.Input(id='order-quantity', type='number', value=0.001),
                    dbc.Label("Prix (pour les ordres limit)"),
                    dcc.Input(id='order-price', type='number'),
                    html.Button(id='submit-order', n_clicks=0, children='Placer l\'ordre'),
                    html.Div(id='order-result')
                ])
            ], width=12)
        ])
    ], fluid=True)
