import pandas as pd
import numpy as np
import ast


class APostprocessing:
    
    
    def add_trade_features(self, trade):
        trade["status"] = trade["state"].apply(lambda x : ast.literal_eval(x)[0])
        
        trade['gp'] = np.where(trade["state"].apply(lambda x : ast.literal_eval(x)[1]), trade['pnl'].diff(), 0)
        trade["gp"] = np.where(trade["status"] == "Open", 0, trade["gp"])
        trade["cum_gp"] = trade["gp"].cumsum()
        
        trade['cum_price'] = (trade['ret_price'] + 1).cumprod()
        
        
    def recovery_per_trade(self, trade):
        trade["loss"] = np.where(trade["pnl_pct"] <= 0, trade["pnl_pct"], 0)
        trade["recovery"] = (1 / (1 + trade["loss"])) - 1
    
    
    def transform(self, trade):
        #trade.set_index('date', inplace = True)
        
        self.add_trade_features(trade)
        self.recovery_per_trade(trade)
        
        

    def split_long_short(self, trade):
        loc_long = np.where(trade["state"].apply(lambda x : ast.literal_eval(x)[1]) == "LONG")
        loc_short = np.where(trade["state"].apply(lambda x : ast.literal_eval(x)[1]) == "SHORT")
        
        long_trade = trade.iloc[loc_long]
        short_trade = trade.iloc[loc_short]
        
        return long_trade, short_trade
    

    


class PPostprocessing:
    
    def add_features(self, portfolio):
        portfolio["rets"] = portfolio["capital"].pct_change()
        portfolio["cum_rets"] = (portfolio["rets"] + 1).cumprod()
        self.drawdown(portfolio)
    
    def transform(self, portfolio):
        self.add_features(portfolio)
    
    
    def drawdown(self, portfolio):
        portfolio["drawdown"] = (portfolio["capital"] - portfolio["capital"].cummax()) / portfolio["capital"].cummax()
    
    
    