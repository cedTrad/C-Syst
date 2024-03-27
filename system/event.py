import pandas as pd

from dataEngine.data import connect_db
from .retrocation.journal import Journal

class Event:
    
    def __init__(self, date, price):
        self.date = date
        self.price = price


class MarketEvent:
    
    def __init__(self, size = 45, start = "2023", end = "2023", interval = "1d"):
        self.size = size
        self.start = start
        self.end = end
        self.db = connect_db(name = "database", interval = interval)
    
    def gen_data(self, symbol):
        i = 0
        data = self.db.get_data(symbol, start = self.start, end = self.end)
        while True:
            batch = data.iloc[i : i + self.size]
            if len(batch) == self.size:
                yield batch
                i += 1
            else:
                break
    
    def get_data(self, symbol):
        return self.gen_data(symbol)


class PostEvent:
    
    def __init__(self):
        self.portfolioData = pd.DataFrame()
        self.metricsData = pd.DataFrame()
        self.tradesData = pd.DataFrame()
        
        
    def add_trade_line(self, agentId, date, price, asset):
        line = {'agentId' : agentId, 'date' : date, 'price' : price, 
                'quantity' : asset.quantity, 'position' : asset.position,
                'side' : asset.type, 'state' : str(asset.state),
                'in_value' : asset.in_value, 'out_value' : asset.out_value,
                'value' : asset.value, 'pnl' : asset.pnl, 'pnl_pct' : asset.pnl_pct,
                'symbol' : asset.symbol}
        add = pd.DataFrame(line , index = [date])
        self.tradesData = pd.concat([self.tradesData, add], ignore_index = True)
        
        
    def add_portfolio_line(self, agentId, date, symbol, portfolio):
        line = {'agentId' : agentId, 'date' : date, 'risk_value' : portfolio.risk_value,
                'available_value' : portfolio.available_value,
                'capital' : portfolio.capital, "symbol" : symbol}
        
        add = pd.DataFrame(line, index = [date])
        self.portfolioData = pd.concat([self.portfolioData, add], ignore_index = True)
    
    
    def add_metrics_line(self, date, line):
        add = pd.DataFrame(line, index=[date])
        self.metricsData = pd.concat([self.metricsData, add], ignore_index=True)
        
        
    def add_data(self, agentId, date, price, asset, portfolio):
        self.add_trade_line(agentId, date, price, asset)
        self.add_portfolio_line(agentId, date, asset.symbol, portfolio)
        
    def get_combined_data(self):
        data = pd.concat([self.tradesData, self.portfolioData], axis=1)
