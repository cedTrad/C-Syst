
from .signal import Signal
from .management import Management

class Politic:
    
    def __init__(self, capital):
        self.capital = capital
        self.signal = Signal()
        self.management = Management(capital)
    
    def signal_policy(self, signal):
        return signal
    
    
    def risk_policy(self, available_amount, current_status):
        amount = available_amount
        return amount
    
    
    def get_signal(self, data):
        self.signal.sets(data)
        points = self.signal.get_points()
        signal = self.signal_policy(points)
        return signal
        
        
    def get_in(self, signal, current_asset_position):
        if current_asset_position == 0 and signal is not None:
            return True
        else:
            return False

    def get_out(self, signal, current_asset_position):
        if current_asset_position == 1 and signal == "SHORT":
            return True
        elif current_asset_position == -1 and signal == "LONG":
            return True
        else:
            return False
        
        
    def perform(self, data, portfolio, current_asset_position):
        
        capital, available_amount = portfolio["capital"], portfolio["available_value"]
        
        signal_action = {}
        risk_action = {}
        
        price = data.iloc[-1]["close"]
        signal = self.get_signal(data)
        
        sl = False
        tp = False
        
        if self.get_in(signal, current_asset_position):
            signal_action.update({"state" : ("Open", signal, sl, tp)})
            
            leverage = 1
            amount = self.risk_policy(available_amount = available_amount, current_status="Open")
            quantity = amount / price
            risk_action.update({"amount" : amount, "quantity" : quantity, "leverage" : leverage})
        
        elif self.get_out(signal, current_asset_position):
            signal_action.update({"state" : ("Close", signal, sl, tp)})
        
        else:
            signal_action.update({"state" : ("-", signal, sl, tp)})
        
        return signal_action, risk_action
    
    
    