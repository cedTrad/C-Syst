import pandas as pd
import numpy as np


class CPPI:
    
    def __init__(self, capital):
        #self.capital = capital
        self.init_capital = capital
        
        
    def update_value(self, m, floor, drawdown = None):
        self.m = m
        self.floor = floor
        self.drawdown = drawdown
    
    
    def update(self, capital):
        self.capital = capital
    
    
    def execute(self, leverage = 1):    
        if self.drawdown is not None:
            peak = np.maximum(self.capital , peak)
            self.floor_value = (1 - self.drawdown)*peak
        else:
            self.floor_value = self.init_capital*self.floor
        # Cushion
        self.cushion = (self.capital - self.floor_value)/self.capital
        
        # Risky_weight
        self.risky_w = self.m * self.cushion
        
        # Borner risky_w, leverage
        self.risky_w = np.minimum(self.risky_w, 1)
        self.risky_w = np.maximum(self.risky_w, 0)
        self.safe_w = 1 - self.risky_w
        
        self.risky_value = self.capital * self.risky_w
        self.safe_value = self.capital * self.safe_w
        