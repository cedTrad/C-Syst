import numpy as np

class CPPI:
    
    def __init__(self, capital):
        #self.capital = capital
        self.init_capital = capital
        self.peak = capital
        
        
    def update_params(self, floor, drawdown = None):
        self.floor = floor
        self.drawdown = drawdown
        
        
    def update_capital(self, capital):
        self.current_capital = capital
        #self.risk_value = self.current_capital * self.risk_w
        
        
    def get_floor_value(self, stop_loss_pct = None):
        if self.drawdown is not None:
            self.peak = np.maximum(self.current_capital, self.peak)
            floor_value = (1 - self.drawdown) * self.peak
        else:
            floor_value = self.current_capital *self.floor
        
        self.floor_value = floor_value
        return floor_value
        
        
    def update_cushion(self):
        cushion = (self.current_capital - self.floor_value) / self.current_capital
        return cushion
    
    

    
