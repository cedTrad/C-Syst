import pandas as pd
import numpy as np
import ast


class Processing:
    
    
    def load(self, portfolioData):
        self.portfolioData = portfolioData
        #portfolioData.set_index("date", inplace = True)
        return self.portfolioData
        
        
    def split_by_agent(self):
        agentIds = self.portfolioData["agentId"].unique()
        portfolios = {}
        for agentId in agentIds:
            portfolios[agentId] = self.portfolioData[self.portfolioData["agentId"] == agentId]
        return portfolios
    
    
    def add_features(self, portfolioData):
        portfolioData["rets"] = portfolioData["capital"].pct_change()
        portfolioData["cum_rets"] = (portfolioData["rets"] + 1).cumprod()
        
    
    
        