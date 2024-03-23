import pandas as pd
import numpy as np
import ast


class APostprocessing:
    
    def __init__(self, capital):
        self.capital = capital
    
    def add_trades_features(self, trades):
        trades['gp'] = np.where(trades["state"].apply(lambda x : ast.literal_eval(x)[1]), trades['pnl'].diff(), 0)
        trades["gp"] = np.where(trades["status"] == "Open", 0, trades["gp"])
        trades["cum_gp"] = trades["gp"].cumsum()
        
        trades['rets'] = trades["cum_gp"] / self.capital
        trades["cum_rets"] = (trades["rets"] + 1).cumprod()
        
        trades['ret_price'] = trades['price'].pct_change()
        trades['cum_price'] = (trades['ret_price'] + 1).cumprod()
        
    
    def transform(self, tradesData):
        self.tradesData = tradesData.copy()
        self.tradesData.drop(columns = ['key'], inplace = True, errors = 'ignore')
        self.tradesData.set_index('date', inplace = True)
        self.tradesData["status"] = self.tradesData["state"].apply(lambda x : ast.literal_eval(x)[0])
        
        trades = self.split_asset_by_agent()
        return trades
        
    
    def split_asset_by_agent(self):
        agentIds = self.tradesData['agentId'].unique()
        trades = {}
        for agentId in agentIds:
            trade = self.tradesData[self.tradesData['agentId'] == agentId].copy()
            self.add_trades_features(trade)
            self.recovery_per_trade(trade)
            trades[agentId] = trade
        return trades
    
    
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
    
    


class PPostprocessing:
    
    def transform(self, portfolioData):
        self.portfolioData = portfolioData
        portfolioData.set_index("date", inplace = True)
        
        portfolios = self.split_by_agent()
        return portfolios
    
        
    def split_by_agent(self):
        agentIds = self.portfolioData["agentId"].unique()
        portfolios = {}
        for agentId in agentIds:
            portfolio = self.portfolioData[self.portfolioData["agentId"] == agentId]
            self.add_features(portfolio)
            portfolios[agentId] = portfolio
        return portfolios
    
    
    def drawdown(self, portfolio):
        portfolio["drawdown"] = (portfolio["capital"] - portfolio["capital"].cummax()) / portfolio["capital"].cummax()
    
    
    def add_features(self, portfolioData):
        portfolioData["rets"] = portfolioData["capital"].pct_change()
        portfolioData["cum_rets"] = (portfolioData["rets"] + 1).cumprod()
        self.drawdown(portfolioData)
    