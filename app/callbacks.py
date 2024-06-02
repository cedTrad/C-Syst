# callbacks.py

import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from datetime import datetime, timedelta
from app.binance_api import get_positions, get_pnl, place_order, get_price, get_ohlc_data, get_open_orders
from app.db_utils import log_event, get_all_events
from app.utils import dark_template, processing, ohlc, waterfall

def register_callbacks(app):
    # Callbacks pour mettre à jour les données en temps réel
    @app.callback(
        [Output('waterfall-graph', 'figure'), Output('positions-table', 'children'), Output('risk-indicators', 'children')],
        [Input('interval-component', 'n_intervals'), Input('order-symbol', 'value')]
    )
    def update_wallet_position(n, symbol):
        wallet_data = get_pnl()
        positions_data = get_positions()
        open_orders = get_open_orders()
        
        positions, r_risk, waterfall_fig = processing(wallet_data, positions_data, open_orders, get_price)
        
        # Tableau des Positions Actuelles
        df_positions = pd.DataFrame(positions)
        positions_table = dbc.Table.from_dataframe(df_positions, striped=True, bordered=True, hover=True)
        
        # Indicateurs de suivi et de risque
        risk_indicators = html.Div([
            html.H5("Indicateurs de Suivi et de Risque"),
            html.P(f"Leverage Ratio = {r_risk['leverage_ratio']}%"),
            html.P(f"Maintenance Margin Ratio = {r_risk['maint_margin_ratio']}%"),
            html.P(f"Risk-Reward Ratio = {r_risk['risk_reward_ratio']}%"),
        ])
            
        ohlc_fig = ohlc(positions, symbol, get_ohlc_data)
        
        return waterfall_fig, positions_table, risk_indicators
        
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

    # Callback pour afficher ou masquer le champ "Limit Price"
    @app.callback(
        Output('order-price', 'style'),
        [Input('order-type', 'value')]
    )
    def show_hide_limit_price(order_type):
        if order_type == 'LIMIT':
            return {'display': 'block'}
        return {'display': 'none'}

    # Callback pour mettre à jour le cours du symbole sélectionné
    @app.callback(
        Output('current-price', 'children'),
        [Input('order-symbol', 'value')]
    )
    def update_current_price(symbol):
        price_data = get_price(symbol)
        if 'price' in price_data:
            price = float(price_data['price'])
            return f"{price} USD"
        return "Erreur lors de la récupération du prix"

    # Callback pour afficher le graphique OHLC
    @app.callback(
        Output('ohlc-graph', 'figure'),
        [Input('order-symbol', 'value')]
    )
    def update_ohlc_graph(symbol):
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        interval = "1h"
        
        ohlc_data = get_ohlc_data(symbol, start_date, end_date, interval)
        
        if ohlc_data:
            df_ohlc = pd.DataFrame(ohlc_data)
            fig = go.Figure(data=[go.Candlestick(
                x=df_ohlc['time'],
                open=df_ohlc['open'],
                high=df_ohlc['high'],
                low=df_ohlc['low'],
                close=df_ohlc['close']
            )])
            y_range = [min(df_ohlc["low"]) * 0.99, max(df_ohlc["high"]) * 1.01]
            fig = fig.update_yaxes(range=y_range, showgrid=False)
            
            max_time = df_ohlc['time'].max() + pd.Timedelta(hours=8)
            fig.update_xaxes(range=[df_ohlc['time'].min(), max_time])
            
            fig.update_xaxes(rangeslider_visible=False, showgrid=False,
                             rangeselector=dict(
                                    buttons=list([
                                        dict(count=30, label="30min", step="minute", stepmode="backward"),
                                        dict(count=4, label="4h", step="hour", stepmode="backward"),
                                        dict(count=12, label="12h", step="hour", stepmode="backward"),
                                        dict(count=1, label="1d", step="day", stepmode="backward"),
                                        dict(count=7, label="7w", step="day", stepmode="backward")
                                    ]),
                                    font=dict(color="blue")
                                )
                             )
            
            fig.update_layout(
                height=600,
                legend=dict(orientation="h", yanchor="bottom", y=1, xanchor="right", x=0.5),
                margin={'t':0, 'b':0, 'l':10, 'r':0},
                template=dark_template, showlegend=False
            )           
            return fig
        return {}

    # Fonction de validation de l'entrée pour les ordres
    def validate_order_input(symbol, order_type, quantity, leverage, price):
        if not symbol or not order_type or not quantity or not leverage or (order_type == 'LIMIT' and not price):
            return "Tous les champs sont obligatoires pour les ordres limit", "alert alert-danger"
        if quantity <= 0 or leverage <= 0 or (price and price <= 0):
            return "La quantité, le levier et le prix doivent être des valeurs positives", "alert alert-danger"
        #if symbol and order_type and quantity and leverage and (order_type == 'MARKET' and price is None):
        #    return f"symbol : {symbol} - quantity : {quantity} - price : {price}", "OK continuons"
        return None, None

    # Fonction pour journaliser l'événement et retourner le résultat de l'ordre
    def log_and_return_order_result(result, event_time, symbol, side, order_type, quantity, price):
        if 'orderId' in result:
            log_event('ORDER_PLACED', event_time, symbol, side, order_type, quantity, price, 'SUCCESS')
            return f"Ordre placé avec succès : {result}", "alert alert-success"
        else:
            log_event('ORDER_FAILED', event_time, symbol, side, order_type, quantity, price, 'FAILURE')
            return f"Erreur lors du placement de l'ordre : {result}", "alert alert-danger"

    # Callback pour placer un ordre Long / Short
    @app.callback(
        [Output('order-result', 'children'), Output('order-result', 'className')],
        [Input('order-long', 'n_clicks'), Input('order-short', 'n_clicks')],
        [State('order-symbol', 'value'),
         State('order-type', 'value'),
         State('order-quantity', 'value'),
         State('order-leverage', 'value'),
         State('order-price', 'value')]
    )
    def place_order_callback(n_clicks_long, n_clicks_short, symbol, order_type, quantity, leverage, price):
        ctx = dash.callback_context

        if not ctx.triggered:
            return "", ""

        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if button_id == 'order-long':
            side = "BUY"
        elif button_id == 'order-short':
            side = "SELL"
        else:
            return "", ""

        error_message, error_class = validate_order_input(symbol, order_type, quantity, leverage, price)
        if error_message:
            return error_message, error_class

        result = place_order(symbol, side, order_type, quantity, leverage, price)
        event_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        return log_and_return_order_result(result, event_time, symbol, side, order_type, quantity, price)

    # Callback pour afficher les événements
    @app.callback(
        Output('events-div', 'children'),
        [Input('interval-component', 'n_intervals')]
    )
    def display_events(n):
        events = get_all_events()
        df_events = pd.DataFrame(events, columns=['ID', 'Type', 'Time', 'Symbol', 'Side', 'Order Type', 'Quantity', 'Price', 'Result'])
        return dbc.Table.from_dataframe(df_events, striped=True, bordered=True, hover=True)
