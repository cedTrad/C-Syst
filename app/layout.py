from dash import dcc, html

def create_layout():
    return html.Div([
        html.H1("Application de Trading de Crypto Inspirée de Binance Futures"),
        html.Label("Sélectionner l'intervalle de temps :"),
        dcc.Dropdown(
            id='time-interval',
            options=[
                {'label': '1 Minute', 'value': '1m'},
                {'label': '5 Minutes', 'value': '5m'},
                {'label': '15 Minutes', 'value': '15m'},
                {'label': '1 Hour', 'value': '1h'},
                {'label': '1 Day', 'value': '1d'},
            ],
            value='1m',
            placeholder="Intervalle de Temps",
            style={'width': '50%'}
        ),
        html.Label("Sélectionner la fréquence de mise à jour :"),
        dcc.Dropdown(
            id='update-frequency',
            options=[
                {'label': '30 secondes', 'value': 30*1000},
                {'label': '1 minute', 'value': 60*1000},
                {'label': '5 minutes', 'value': 5*60*1000},
            ],
            value=60*1000,
            placeholder="Fréquence de mise à jour",
            style={'width': '50%'}
        ),
        html.Label("Sélectionner le type de graphique :"),
        dcc.Dropdown(
            id='chart-type',
            options=[
                {'label': 'Chandelier', 'value': 'candlestick'},
                {'label': 'Ligne', 'value': 'line'},
            ],
            value='candlestick',
            placeholder="Type de graphique",
            style={'width': '50%'}
        ),
        html.Label("Sélectionner la période historique :"),
        dcc.Dropdown(
            id='historical-period',
            options=[
                {'label': '1 Jour', 'value': '1d'},
                {'label': '1 Semaine', 'value': '7d'},
                {'label': '1 Mois', 'value': '1m'},
            ],
            value='7d',
            placeholder="Période Historique",
            style={'width': '50%'}
        ),
        html.Label("Ajouter des indicateurs techniques :"),
        dcc.Checklist(
            id='technical-indicators',
            options=[
                {'label': 'Moyenne Mobile Simple (SMA)', 'value': 'sma'},
                {'label': 'Moyenne Mobile Exponentielle (EMA)', 'value': 'ema'},
            ],
            value=['sma']
        ),
        dcc.Graph(id='live-graph', animate=True),
        dcc.Interval(
            id='graph-update',
            interval=60*1000,  # 1 minute par défaut
            n_intervals=0
        ),
        html.Div([
            html.Label("Symbole de la crypto :"),
            dcc.Input(id='crypto-symbol', value='BTCUSDT', type='text', style={'width': '20%'}),
            html.Label("Montant de l'ordre :"),
            dcc.Input(id='order-amount', value='1', type='number', style={'width': '20%'}),
            html.Label("Prix limite :"),
            dcc.Input(id='limit-price', value='0', type='number', placeholder="Prix Limite", style={'width': '20%'}),
            html.Label("Levier :"),
            dcc.Input(id='leverage', value='1', type='number', placeholder="Levier", style={'width': '20%'}),
            html.Label("Stop Loss :"),
            dcc.Input(id='stop-loss', value='0', type='number', placeholder="Stop Loss", style={'width': '20%'}),
            html.Label("Take Profit :"),
            dcc.Input(id='take-profit', value='0', type='number', placeholder="Take Profit", style={'width': '20%'}),
            html.Button('Acheter', id='buy-button', n_clicks=0, style={'backgroundColor': 'green', 'color': 'white'}),
            html.Button('Vendre', id='sell-button', n_clicks=0, style={'backgroundColor': 'red', 'color': 'white'}),
        ], style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'flex-start', 'width': '100%'}),
        html.Div(id='order-status'),
        html.H2("Positions Ouvertes"),
        html.Div(id='open-positions'),
        html.H2("Historique des Transactions"),
        html.Div(id='transaction-history'),
        html.H2("Profit et Perte"),
        html.Div(id='pnl')
    ])
