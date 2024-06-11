import pandas as pd
import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import logging
from app.api.order import Order
from app.overviews import Overview
from app.viz import ohlc_fig

overview = Overview()


class CallBack:
    
    def __init__(self):
        self.overview = Overview()
        
    def register_callbacks(self, app):
        # Update Wallet
        @app.callback(
        [Output('waterfall-graph', 'figure'), Output('risk-indicators', 'children')],
        [Input('interval-component', 'n_intervals')]
        )
        def update_wallet(n):
            self.overview.actuator_wallet()
            risk_indicators = html.Div([
                html.H5("Indicateurs de Suivi et de Risque"),
                html.P(f"Leverage Ratio = {self.overview.risk_indicator['leverage_ratio']}%"),
                html.P(f"Maintenance Margin Ratio = {self.overview.risk_indicator['maint_margin_ratio']}%"),
                html.P(f"Risk-Reward Ratio = {self.overview.risk_indicator['risk_reward_ratio']}%"),
            ], style={"color": "#ffffff"})
            return self.overview.waterfall_fig, risk_indicators
        

        
        # Update Position
        @app.callback(
        [Output('position-table', 'children')],
        [Input('interval-component', 'n_intervals')]
        )
        def update_position(n):
            self.overview.actuator_position()
            positions_df = pd.DataFrame(self.overview.positions)
            return [
                    dash_table.DataTable(
                        id='data-table',
                        columns=[{"name": i, "id": i} for i in positions_df.columns],
                        data=positions_df.to_dict('records'),
                        style_table={'overflowX': 'auto'},
                        style_cell={
                            'minWidth': '150px', 'width': '150px', 'maxWidth': '150px',
                            'whiteSpace': 'normal',
                            'backgroundColor': '#1a1a1a',
                            'color': '#ffffff'
                        },
                        style_header={
                            'backgroundColor': '#2c3e50',
                            'color': '#ffffff'
                        },
                    )
                ]
        
        # Update OHLC Graph
        @app.callback(
            Output('ohlc-graph', 'figure'),
            [Input('order-symbol', 'value'), Input('interval-component', 'n_intervals')]
        )
        def update_ohlc(symbol, n_intervals):
            ohlc_df = overview.ohlc_data(symbol, interval="1d")
            fig = ohlc_fig(symbol, ohlc_df)
            return fig
        
        # Place an order
        @app.callback(
        [Output('order-result', 'children'), Output('order-alert', 'displayed'), Output('order-alert', 'message')],
        [Input('order-long', 'n_clicks'), Input('order-short', 'n_clicks')],
        [State('order-symbol', 'value'),
         State('order-quantity', 'value'),
         State('order-leverage', 'value'),
         State('order-stop_loss', 'value'), State('order-take_profit', 'value')]
        )
        def place_order(long, short, symbol, quantity, leverage, stop_loss, take_profit):
            ctx = dash.callback_context
            order = Order(symbol)
            if not ctx.triggered:
                return "", False, ""
            
            button_id = ctx.triggered[0]['prop_id'].split('.')[0]
            
            result = ""
            alert_message = ""
            success = False
            
            try:
                if button_id == "order-long":
                    result = order.open_long(quantity, leverage, stop_loss, take_profit)
                    alert_message = f"Long order placed for {quantity} {symbol} with leverage {leverage}. SL: {stop_loss}, TP: {take_profit}"
                elif button_id == "order-short":
                    result = order.open_short(quantity, leverage, stop_loss, take_profit)
                    alert_message = f"Short order placed for {quantity} {symbol} with leverage {leverage}. SL: {stop_loss}, TP: {take_profit}"
                
                success = True
                logging.info(alert_message)
            except Exception as e:
                result = str(e)
                alert_message = f"Failed to place order: {str(e)}"
                success = False
                logging.error(alert_message)
                
                # Enhanced error details and troubleshooting steps
                if "Invalid" in result:
                    alert_message += " Please check the order parameters and try again."
                elif "Network" in result:
                    alert_message += " Network error occurred. Please check your internet connection."
                else:
                    alert_message += " An unexpected error occurred. Please try again later."

            return result, success, alert_message
        
        # Order Previews
        @app.callback(
        Output('order-preview', 'children'),
        [Input('order-quantity', 'value'),
         Input('order-leverage', 'value'),
         Input('order-stop_loss', 'value'), Input('order-take_profit', 'value')]
        )
        def order_previews(quantity, leverage, stop_loss, take_profit):
            if quantity and leverage and stop_loss and take_profit:
                return [f"Quantity : {quantity} - Leverage : {leverage} - ST/TP : [{stop_loss}-{take_profit}]"]
        
        # Modal Callback
        @app.callback(
            Output("modal-order-info", "is_open"),
            [Input("order-long", "n_clicks"), Input("order-short", "n_clicks"), Input("close-order-info", "n_clicks")],
            [State("modal-order-info", "is_open")],
        )
        def toggle_modal(n1, n2, n3, is_open):
            if n1 or n2:
                return not is_open
            elif n3:
                return False
            return is_open
