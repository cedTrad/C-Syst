import pandas as pd
import numpy as np
import ast


class Processing:
    
    def add_trades_features(self, trades):
        trades['ret_price'] = trades['price'].pct_change()
        trades['price_cum'] = (trades['ret_price'] + 1).cumprod()
        trades['gp'] = np.where((trades['status'] == 'open') | ((trades['position'] == 0) & (trades['status'] != 'close')),
                               0, trades['pnl'].diff())
        trades['rets'] = np.where(trades["status"] == "open", 0, trades["pnl_pct"].diff())
        trades['cum_rets'] = (trades["rets"] + 1).cumprod()
        
        trades.fillna(0, inplace = True)
        
    
    def load(self, trades):
        trades = trades.copy()
        trades.drop(columns = ['key'], inplace = True, errors = 'ignore')
        trades.set_index('date', inplace = True)
        trades["status"] = trades["state"].apply(lambda x : ast.literal_eval(x)[0])
        return trades
    
    
    def split_long_short(self, trades):
        loc_long = np.where((trades["side"] == "LONG") | ((trades["side"] == None) & ( trades["status"] == "Close")))
        loc_short = np.where((trades["side"] == "SHORT") | ((trades["side"] == None) & (trades["status"] == "Close")))
        
        long_trade = trades.iloc[loc_long]
        short_trade = trades.iloc[loc_short]
        
        return long_trade, short_trade
    
    
    def split_asset(self, trades):
        datas = {}
        symbols = trades['symbol'].unique()
        for symbol in symbols:
            trade = trades[trades['symbol'] == symbol].copy()
            long_trade, short_trade = self.split_long_short(trade)
            
            datas[symbol] = {
                "all" : trade,
                "long" : long_trade,
                "short" : short_trade
            }
            
            for data_type in ["all", "long", "short"]:
                self.add_trades_features(datas[symbol][data_type])
                self.recovery_per_trade(datas[symbol][data_type])
        return datas
    
    
    def recovery_per_trade(self, trades):
        trades["loss"] = np.where(trades["pnl_pct"] <= 0, trades["pnl_pct"], 0)
        trades["recovery"] = (1 / (1 + trades["loss"])) - 1
    
    
    
    