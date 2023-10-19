from .risk.cppi import CPPI
from .risk.sizing import Sizing

class Management:
    
    def __init__(self, capital):
        self.init_capital = capital
        
        self.sizing = Sizing(capital = capital)
        self.cppi = CPPI(capital=capital)
    
    
    def config_cppi(self, m, floor):
        self.cppi.update_value(m, floor)
    
    
    def sizing(self, politic):
        return
    
        
    def run(self, capital):
        self.cppi.update(capital)
        self.cppi.execute()
        
        self.floor_value = self.cppi.floor_value
        self.risky_w = self.cppi.risky_w
        self.safe_w = self.cppi.safe_w
        self.cushion = self.cppi.cushion
        
        self.value_to_risk = capital * self.cppi.risky_w
        self.value_to_safe = capital * self.cppi.safe_w
        