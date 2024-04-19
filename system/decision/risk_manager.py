import numpy as np

from .risk.cppi import CPPI
from .risk.profit import ProfitManager

RISK_SIGNAL = ["Close", "Resize"]

CUSHION = 0.25
CUSHION_SEUIL = np.linspace(0, CUSHION, 5)


class RiskManager:
    
    def __init__(self, capital):
        self.session_capital = capital  # Capital a l'ouverture de la session
        
        self.stop_loss_pct = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4]
        self.take_profit = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4]
        self.leverage = [1, 3, 4, 5, 6, 7, 8, 9, 10]
        
        self.cppi = CPPI(capital=capital)
        self.profitmanager = ProfitManager
    
    def get_metric(self):
        return
    
    
    def get_current_capital(self, capital):
        self.current_capital = capital
        
         
    def config_session_risk(self, params): # params = {"floor" : floor}
        self.cppi.update_params(**params)
    
    
    def update_session_capital(self, capital):
        self.session_capital = capital
    
    def update_floor_value(self, params):
        self.cppi.update_params(**params)
        floor_value = self.cppi.get_floor_value()
    
    
    def update_risk(self, params = {"m" : 3}):
        m = params["m"]
        risk_w = self.cushion * m
        risk_w = np.minimum(risk_w, 1)
        risk_w = np.maximum(risk_w, 0)
        return risk_w
    
    
    def actuator(self, capital):
        self.get_current_capital(capital)
        self.cppi.get_current_capital(capital)
        self.cushion = self.cppi.update_cushion()
        
        riskw = self.update_risk()
        
    
    
    
    
    
    