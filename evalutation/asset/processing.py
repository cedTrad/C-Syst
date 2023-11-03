import pandas as pd
import numpy as np
import ast


class Processing:
    
    def add_trades_features(self, trades):
        trades['gp'] = np.where(trades["state"].apply(lambda x : ast.literal_eval(x)[1]), trades['pnl'].diff(), 0)
        trades["gp"] = np.where(trades["status"] == "Open", 0, trades["gp"])
        trades["cum_gp"] = trades["gp"].cumsum()
        
        trades['rets'] = np.where(trades["state"].apply(lambda x : ast.literal_eval(x)[1]), trades['pnl_pct'].diff(), 0)
        trades["rets"] = np.where(trades["status"] == "Open", 0, trades["rets"])
        
        trades['ret_price'] = trades['price'].pct_change()
        trades['price_cum'] = (trades['ret_price'] + 1).cumprod()
        #strades.fillna(0, inplace = True)
        
    
    def load(self, trades):
        trades = trades.copy()
        trades.drop(columns = ['key'], inplace = True, errors = 'ignore')
        trades.set_index('date', inplace = True)
        trades["status"] = trades["state"].apply(lambda x : ast.literal_eval(x)[0])
        return trades
    
    
    def split_asset_by_agent(self, trades):
        agentIds = trades['agentId'].unique()
        datas = {}
        for agentId in agentIds:
            trades = trades[trades['agentId'] == agentId].copy()
            self.add_trades_features(trades)
            self.recovery_per_trade(trades)
            datas[agentId] = trades
        return datas
    
    
    def recovery_per_trade(self, trades):
        trades["loss"] = np.where(trades["pnl_pct"] <= 0, trades["pnl_pct"], 0)
        trades["recovery"] = (1 / (1 + trades["loss"])) - 1
    
    
    
    
    
    
    
    
    def split_long_short(self, trades):
        loc_long = np.where(trades["state"].apply(lambda x : ast.literal_eval(x)[1]) == "LONG")
        loc_short = np.where(trades["state"].apply(lambda x : ast.literal_eval(x)[1]) == "SHORT")
        
        long_trade = trades.iloc[loc_long]
        short_trade = trades.iloc[loc_short]
        
        return long_trade, short_trade
    
    
    def split_asset(self, trades):
        datas = {}
        agentIds = trades['agentId'].unique()
        for agentId in agentIds:
            trade = trades[trades['agentId'] == agentId].copy()
            long_trade, short_trade = self.split_long_short(trade)
            
            datas[agentId] = {
                "all" : trade,
                "long" : long_trade,
                "short" : short_trade
            }
            
            for data_type in ["all", "long", "short"]:
                self.add_trades_features(datas[agentId][data_type])
                self.recovery_per_trade(datas[agentId][data_type])
        return datas
    
    
    