import pandas as pd
import numpy as np
import ast


class Processing:
    
    
    def load(self, portfolio_data):
        portfolio_data.set_index("date", inplace = True)
    
    
    def add_features(self, portfolio_data):
        portfolio_data["rets"] = portfolio_data["capital"].pct_change()
        portfolio_data["cum_rets"] = (portfolio_data["rets"] + 1).cumprod()
        
        
        