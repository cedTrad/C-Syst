import pandas as pd
from app.api.account import Account
from app.viz import ohlc_fig, waterfall, generate_flow_chart


class Overview:
    
    def __init__(self):
        self.account = Account()
    
    def ohlc_data(self, symbol, interval):
        ohlc = self.account.get_ohlc_data(symbol, interval)
        df = pd.DataFrame(ohlc, columns=['time', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
        df['time'] = pd.to_datetime(df['time'], unit='ms')
        df['close_time'] = pd.to_datetime(df['close_time'], unit='ms')
        for col in ['open', 'high', 'low', 'close', 'volume']:
            df[col] = df[col].astype(float)
        return df


    def actuator_position(self):
        self.positions_data = self.account.get_positions()
        self.positions = self.process_positions()
    
    def actuator_wallet(self):
        self.wallets_data = self.account.get_wallet()
        self.risk_indicator, self.waterfall_fig = self.process_wallet()
    
    def prisk(self, totalInitialMargin, totalWalletBalance, totalMaintMargin, totalUnrealizedProfit):
        leverage_ratio = round((totalInitialMargin / totalWalletBalance) * 100, 2) if totalWalletBalance != 0 else 0
        maint_margin_ratio = round((totalMaintMargin / totalWalletBalance) * 100, 2) if totalWalletBalance != 0 else 0
        risk_reward_ratio = round((totalUnrealizedProfit / totalInitialMargin) * 100, 2) if totalInitialMargin != 0 else 0
        return {"leverage_ratio" : leverage_ratio, "maint_margin_ratio" : maint_margin_ratio, "risk_reward_ratio" : risk_reward_ratio}


    def process_wallet(self):
        totalWalletBalance = float(self.wallets_data['totalWalletBalance'])
        totalInitialMargin = float(self.wallets_data['totalInitialMargin'])
        totalMaintMargin = float(self.wallets_data['totalMaintMargin'])
        totalUnrealizedProfit = float(self.wallets_data['totalUnrealizedProfit'])
        totalMarginBalance = float(self.wallets_data['totalMarginBalance'])
        availableBalance = float(self.wallets_data['availableBalance'])
        maxWithdrawAmount = float(self.wallets_data['maxWithdrawAmount'])
        totalPositionInitialMargin = float(self.wallets_data['totalPositionInitialMargin'])
        totalOrderInitialMargin = float(self.wallets_data['totalOpenOrderInitialMargin'])
        
        flow_fig = generate_flow_chart(totalWalletBalance, totalInitialMargin, availableBalance, totalUnrealizedProfit,
                            totalInitialMargin, totalOrderInitialMargin, totalPositionInitialMargin)
        
        r_risk = self.prisk(totalInitialMargin, totalWalletBalance, totalMaintMargin, totalUnrealizedProfit)
        waterfall_fig = waterfall(totalWalletBalance, totalInitialMargin, totalUnrealizedProfit, availableBalance)
        return r_risk, waterfall_fig, flow_fig
    
    
    def process_positions(self):
        positions = []
        total_portfolio_value = 0
        for pos in self.positions_data:
            if float(pos['positionAmt']) != 0:
                symbol = pos['symbol']
                current_price_data = self.account.get_price(symbol)
                current_price = float(current_price_data['price']) if 'price' in current_price_data else None
                position_amt = float(pos['positionAmt'])
                entry_price = float(pos['entryPrice'])
                unrealized_profit = float(pos['unRealizedProfit'])
                leverage = float(pos['leverage'])
                    
                # Récupérer les ordres ouverts pour le symbole actuel
                stop_loss, take_profit = None, None
                for order in self.account.get_open_orders():
                    if order['symbol'] == symbol:
                        if order['type'] == 'STOP_MARKET':
                            stop_loss = float(order['stopPrice'])
                        elif order['type'] == 'TAKE_PROFIT_MARKET':
                            take_profit = float(order['stopPrice'])

                # Calcul des nouvelles colonnes
                position_type = 'LONG' if position_amt > 0 else 'SHORT'
                roi = (unrealized_profit / (entry_price * abs(position_amt))) * leverage * 100 if entry_price != 0 else 0
                entry_amount = entry_price * abs(position_amt)
                current_value = current_price * abs(position_amt) if current_price is not None else 0
                    
                total_portfolio_value += current_value
                    
                positions.append({
                    'symbol': symbol,
                    'positionAmt': round(position_amt, 2),
                    'entryPrice': round(entry_price, 2),
                    'entryAmount': round(entry_amount, 2),
                    'unrealizedProfit': round(unrealized_profit, 2),
                    'leverage': round(leverage, 2),
                    'currentValue': round(current_value, 2),
                    'breakEvenPrice': round(entry_price, 2),  # Placeholder, update with correct calculation if available
                    'stopLoss': round(stop_loss, 2) if stop_loss is not None else None,
                    'takeProfit': round(take_profit, 2) if take_profit is not None else None,
                    'positionType': position_type,
                    'ROI (%)': round(roi, 2)
                })
        return positions