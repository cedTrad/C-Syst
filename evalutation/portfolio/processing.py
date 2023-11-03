import pandas as pd
import numpy as np
import ast


class Processing:
    
    
    def load(self, portfolio_data):
        self.portfolio_data = portfolio_data
        #portfolio_data.set_index("date", inplace = True)
        
        
    def split_by_agent(self):
        agentIds = self.portfolio_data["agentId"].unique()
        portfolios = {}
        for agentId in agentIds:
            portfolios[agentId] = self.portfolio_data[self.portfolio_data["agentId"] == agentId]
        return portfolios
    
    
    def add_features(self, portfolio_data):
        portfolio_data["rets"] = portfolio_data["capital"].pct_change()
        portfolio_data["cum_rets"] = (portfolio_data["rets"] + 1).cumprod()
        
    
    
        