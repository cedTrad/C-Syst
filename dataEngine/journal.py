import pandas as pd
import numpy as np
import uuid
import json
import os


class Journal:
    
    def __init__(self, database_config = None):
        self.portfolio_data = pd.DataFrame()
        self.metrics_data = pd.DataFrame()
        self.trades_data = pd.DataFrame()
    
    
    def add_trade_line(self, agentId, date, price, asset):
        line = {'agentId' : agentId, 'date' : date, 'price' : price, 
                'quantity' : asset.quantity, 'position' : asset.position,
                'side' : asset.type, 'state' : str(asset.state),
                'in_value' : asset.in_value, 'out_value' : asset.out_value,
                'value' : asset.value, 'pnl' : asset.pnl, 'pnl_pct' : asset.pnl_pct,
                'symbol' : asset.symbol}
        add = pd.DataFrame(line , index = [date])
        self.trades_data = pd.concat([self.trades_data, add], ignore_index = True)
        
        
    def add_portfolio_line(self, agentId, date, symbol, portfolio):
        line = {'agentId' : agentId, 'date' : date, 'risk_value' : portfolio.risk_value,
                'available_value' : portfolio.available_value,
                'capital' : portfolio.capital, "symbol" : symbol}
        
        add = pd.DataFrame(line, index = [date])
        self.portfolio_data = pd.concat([self.portfolio_data, add], ignore_index = True)
    
    
    def add_metrics_line(self, date, line):
        add = pd.DataFrame(line, index=[date])
        self.metrics_data = pd.concat([self.metrics_data, add], ignore_index=True)

    
    def add_data(self, agentId, date, price, asset, portfolio):
        self.add_trade_line(agentId, date, price, asset)
        self.add_portfolio_line(agentId, date, asset.symbol, portfolio)


