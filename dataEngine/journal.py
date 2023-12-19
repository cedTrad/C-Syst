import pandas as pd
import numpy as np
import uuid
import json
import os


class Journal:
    
    def __init__(self, database_config = None):
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
        print(f"*** LINE {line}")
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


