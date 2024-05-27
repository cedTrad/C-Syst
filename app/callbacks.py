from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import pandas as pd
from app.data_fetcher import fetch_crypto_data, fetch_historical_data, place_order, get_open_positions, get_order_history, get_pnl
from app.database import add_order, get_orders

def calculate_sma(data, window):
    return data.rolling(window=window).mean()

def calculate_ema(data, window):
    return data.ewm(span=window, adjust=False).mean()

def register_callbacks(app):
    @app.callback(
        Output('graph-update', 'interval'),
        Input('update-frequency', 'value')
    )
    def update_interval(frequency):
        return frequency

    @app.callback(
        Output('live-graph', 'figure'),
        [Input('graph-update', 'n_intervals'),
         Input('time-interval', 'value'),
         Input('chart-type', 'value'),
         Input('historical-period', 'value'),
         Input('technical-indicators', 'value')],
        State('crypto-symbol', 'value')
    )
    def update_graph(n, interval, chart_type, period, indicators, symbol):
        data = fetch_historical_data(symbol, interval, period)
        if chart_type == 'candlestick':
            fig = go.Candlestick(
                x=data['timestamp'],
                open=data['open'],
                high=data['high'],
                low=data['low'],
                close=data['close'],
                increasing_line_color='green',
                decreasing_line_color='red'
            )
        else:
            fig = go.Scatter(
                x=data['timestamp'],
                y=data['close'],
                mode='lines',
                line=dict(color='blue')
            )

        figure_data = [fig]

        # Ajout des indicateurs techniques
        if 'sma' in indicators:
            sma = calculate_sma(data['close'], window=20)
            figure_data.append(go.Scatter(
                x=data['timestamp'],
                y=sma,
                mode='lines',
                line=dict(color='orange', dash='dash'),
                name='SMA 20'
            ))
        if 'ema' in indicators:
            ema = calculate_ema(data['close'], window=20)
            figure_data.append(go.Scatter(
                x=data['timestamp'],
                y=ema,
                mode='lines',
                line=dict(color='purple', dash='dash'),
                name='EMA 20'
            ))

        # Points d'entrée, sortie, stop loss et take profit
        order_markers = []
        orders = get_orders()
        for order in orders:
            if order.symbol == symbol:
                order_markers.append(go.Scatter(
                    x=[order.timestamp],
                    y=[order.price],
                    mode='markers+text',
                    marker=dict(color='blue' if order.type == 'buy' else 'orange', size=12),
                    text=order.type.capitalize(),
                    textposition='top center'
                ))
                if order.stop_loss > 0:
                    order_markers.append(go.Scatter(
                        x=[order.timestamp],
                        y=[order.stop_loss],
                        mode='markers+text',
                        marker=dict(color='red', size=10, symbol='x'),
                        text='Stop Loss',
                        textposition='bottom center'
                    ))
                if order.take_profit > 0:
                    order_markers.append(go.Scatter(
                        x=[order.timestamp],
                        y=[order.take_profit],
                        mode='markers+text',
                        marker=dict(color='green', size=10, symbol='triangle-up'),
                        text='Take Profit',
                        textposition='bottom center'
                    ))

        figure = {
            'data': figure_data + order_markers,
            'layout': go.Layout(
                xaxis={'title': 'Time'},
                yaxis={'title': 'Price'},
                title=f'Price of {symbol} over the last {period}',
                plot_bgcolor='black',
                paper_bgcolor='black',
                font={'color': 'white'}
            )
        }
        return figure

    @app.callback(Output('order-status', 'children'),
                  [Input('buy-button', 'n_clicks'),
                   Input('sell-button', 'n_clicks')],
                  [State('crypto-symbol', 'value'),
                   State('order-amount', 'value'),
                   State('limit-price', 'value'),
                   State('leverage', 'value'),
                   State('stop-loss', 'value'),
                   State('take-profit', 'value')])
    def handle_orders(buy_clicks, sell_clicks, symbol, amount, limit_price, leverage, stop_loss, take_profit):
        ctx = dash.callback_context
        if not ctx.triggered:
            return ''
        else:
            button_id = ctx.triggered[0]['prop_id'].split('.')[0]
            order_type = 'LIMIT' if limit_price > 0 else 'MARKET'
            side = 'BUY' if button_id == 'buy-button' else 'SELL'
            order = place_order(symbol, amount, limit_price, side, order_type, leverage)
            return f'Ordre {side} de {amount} {symbol} au prix limite de {limit_price} avec un levier de {leverage}, stop loss à {stop_loss} et take profit à {take_profit} passé avec succès.'

    @app.callback(Output('open-positions', 'children'),
                  Input('graph-update', 'n_intervals'))
    def update_open_positions(n):
        positions = get_open_positions()
        return html.Table([
            html.Thead(html.Tr([html.Th("Symbol"), html.Th("Position Amount"), html.Th("Entry Price"), html.Th("PNL")])),
            html.Tbody([
                html.Tr([html.Td(pos['symbol']), html.Td(pos['positionAmt']), html.Td(pos['entryPrice']), html.Td(pos['unrealizedProfit'])])
                for pos in positions
            ])
        ])

    @app.callback(Output('transaction-history', 'children'),
                  [Input('graph-update', 'n_intervals')],
                  State('crypto-symbol', 'value'))
    def update_transaction_history(n, symbol):
        orders = get_order_history(symbol)
        return html.Table([
            html.Thead(html.Tr([html.Th("Order ID"), html.Th("Timestamp"), html.Th("Symbol"), html.Th("Type"), html.Th("Price"), html.Th("Quantity"), html.Th("Status")])),
            html.Tbody([
                html.Tr([html.Td(order['orderId']), html.Td(pd.to_datetime(order['time'], unit='ms')), html.Td(order['symbol']), html.Td(order['side']), html.Td(order['price']), html.Td(order['origQty']), html.Td(order['status'])])
                for order in orders
            ])
        ])

    @app.callback(Output('pnl', 'children'),
                  Input('graph-update', 'n_intervals'))
    def update_pnl(n):
        pnl = get_pnl()
        return f'Total PnL: {pnl} USDT'
