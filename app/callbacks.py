from dash import dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from datetime import datetime
from app.binance_api import get_positions, get_history, get_pnl, place_order, get_price
from app.db_utils import log_event, get_all_events

def register_callbacks(app):
    # Callbacks pour mettre à jour les données en temps réel
    @app.callback(
        Output('positions-div', 'children'),
        [Input('interval-component', 'n_intervals')]
    )
    def update_positions(n):
        positions_data = get_positions()
        if 'positions' in positions_data:
            positions = positions_data['positions']
            df_positions = pd.DataFrame(positions)
            df_positions = df_positions[df_positions['positionAmt'].astype(float) != 0]
            return dbc.Table.from_dataframe(df_positions, striped=True, bordered=True, hover=True)
        return "Erreur lors de la récupération des données des positions."

    @app.callback(
        Output('pnl-div', 'children'),
        [Input('interval-component', 'n_intervals')]
    )
    def update_pnl(n):
        pnl_data = get_pnl()
        if 'assets' in pnl_data:
            assets = pnl_data['assets']
            df_pnl = pd.DataFrame(assets)
            df_pnl = df_pnl[df_pnl['walletBalance'].astype(float) > 0]
            return dbc.Table.from_dataframe(df_pnl, striped=True, bordered=True, hover=True)
        return "Erreur lors de la récupération des données du PnL."

    # Callback pour afficher l'historique et le graphique
    @app.callback(
        [Output('history-div', 'children'), Output('history-graph', 'figure')],
        [Input('submit-button', 'n_clicks')],
        [State('date-picker-range', 'start_date'), State('date-picker-range', 'end_date')]
    )
    def update_history(n_clicks, start_date, end_date):
        if n_clicks > 0:
            start_timestamp = int(pd.Timestamp(start_date).timestamp() * 1000)
            end_timestamp = int(pd.Timestamp(end_date).timestamp() * 1000)
            history_data = get_history(None, start_timestamp, end_timestamp)
            if history_data:
                df_history = pd.DataFrame(history_data)
                table = dbc.Table.from_dataframe(df_history, striped=True, bordered=True, hover=True)

                fig = px.line(df_history, x='time', y='price', color='symbol', title='Prix au Fil du Temps')
                return table, fig
        return "Sélectionnez une période et cliquez sur 'Afficher l'historique'", {}

    # Callback pour afficher les actifs détenus
    @app.callback(
        Output('assets-div', 'children'),
        [Input('interval-positions-component', 'n_intervals')]
    )
    def update_assets(n):
        positions_data = get_positions()
        if 'positions' in positions_data:
            positions = positions_data['positions']
            df_positions = pd.DataFrame(positions)
            df_positions = df_positions[df_positions['positionAmt'].astype(float) != 0]

            # Limiter à 3 actifs maximum
            df_positions = df_positions.head(3)

            # Obtenir les historiques des prix pour ces actifs
            figures = []
            for asset in df_positions['symbol']:
                start_timestamp = int(pd.Timestamp('today') - pd.DateOffset(days=30).timestamp() * 1000)
                end_timestamp = int(pd.Timestamp('today').timestamp() * 1000)
                history_data = get_history(asset, start_timestamp, end_timestamp)
                if history_data:
                    df_history = pd.DataFrame(history_data)
                    fig = px.line(df_history, x='time', y='price', title=f'Tendances de {asset}')
                    figures.append(dcc.Graph(figure=fig))

            return figures
        return "Erreur lors de la récupération des données des actifs."

    # Callback pour prévisualiser l'ordre
    @app.callback(
        Output('order-preview', 'children'),
        [Input('order-symbol', 'value'), Input('order-quantity', 'value'), Input('order-leverage', 'value')]
    )
    def preview_order(symbol, quantity, leverage):
        if symbol and quantity and leverage:
            price_data = get_price(symbol)
            if 'price' in price_data:
                price = float(price_data['price'])
                total = price * quantity * leverage
                return f"Prix actuel : {price} USD, Total : {total} USD (avec un levier de {leverage}x)"
        return ""

    # Callback pour placer un ordre
    @app.callback(
        [Output('order-result', 'children'), Output('order-result', 'className')],
        [Input('submit-order', 'n_clicks')],
        [State('order-symbol', 'value'),
         State('order-side', 'value'),
         State('order-type', 'value'),
         State('order-quantity', 'value'),
         State('order-leverage', 'value'),
         State('order-price', 'value')]
    )
    def place_order_callback(n_clicks, symbol, side, order_type, quantity, leverage, price):
        if n_clicks > 0:
            if not symbol or not side or not order_type or not quantity or not leverage or (order_type == 'LIMIT' and not price):
                return "Tous les champs sont obligatoires pour les ordres limit", "alert alert-danger"
            if quantity <= 0 or leverage <= 0 or (price and price <= 0):
                return "La quantité, le levier et le prix doivent être des valeurs positives", "alert alert-danger"
            
            result = place_order(symbol, side, order_type, quantity, leverage, price)
            event_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            if 'orderId' in result:
                log_event('ORDER_PLACED', event_time, symbol, side, order_type, quantity, price, 'SUCCESS')
                return f"Ordre placé avec succès : {result}", "alert alert-success"
            else:
                log_event('ORDER_FAILED', event_time, symbol, side, order_type, quantity, price, 'FAILURE')
                return f"Erreur lors du placement de l'ordre : {result}", "alert alert-danger"
        return "", ""

    # Callback pour afficher les événements
    @app.callback(
        Output('events-div', 'children'),
        [Input('interval-component', 'n_intervals')]
    )
    def display_events(n):
        events = get_all_events()
        df_events = pd.DataFrame(events, columns=['ID', 'Type', 'Time', 'Symbol', 'Side', 'Order Type', 'Quantity', 'Price', 'Result'])
        return dbc.Table.from_dataframe(df_events, striped=True, bordered=True, hover=True)

    # Callback pour afficher l'évolution du capital
    @app.callback(
        Output('capital-graph', 'figure'),
        [Input('interval-component', 'n_intervals')]
    )
    def update_capital_graph(n):
        pnl_data = get_pnl()
        if 'assets' in pnl_data:
            assets = pnl_data['assets']
            df_pnl = pd.DataFrame(assets)
            df_pnl = df_pnl[df_pnl['walletBalance'].astype(float) > 0]
            fig = px.line(df_pnl, x='asset', y='walletBalance', title='Évolution du Capital')
            return fig
        return {}