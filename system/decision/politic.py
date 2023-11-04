
from .signal import Signal
from .management import Management

from .transition import Transition


class Politic:
    
    def __init__(self, capital : float):
        self.capital = capital
        self.signal = Signal()
        self.management = Management(capital)
    
    
    def select_rule(self, policy_name):
        self.policy_name = policy_name
    
        
    def signal_policy(self, signal):
        return signal
    
    
    def risk_policy(self, available_amount, current_status):
        amount = available_amount
        return amount
    
    
    def update_signal_params(self, params):
        self.params = params
    
    
    def get_signal(self, batchData):
        self.signal.sets(batchData)
        self.rule = self.signal.rules.get(self.policy_name)
        if self.rule is None:
            raise Exception("Policy name incorrect")
        
        self.rule.update_params(self.params)
        
        points = self.rule.run()
        signal = self.signal_policy(points)
        return signal
    
    
    def update_postindicator(self, indicator : dict):
        self.indicator = indicator
    
    
    def perform(self, batchData, portfolio, current_asset_position):
        capital, available_amount = portfolio["capital"], portfolio["available_value"]
        
        signal_action = {}
        risk_action = {}
        
        price = batchData.iloc[-1]["close"]
        signal = self.get_signal(batchData)
        
        sl = False
        tp = False
        
        canOpenPosition, side = Transition(signal, current_asset_position).get_in()
        canclosePosition, side = Transition(signal, current_asset_position).get_out()
        skip, _ = Transition(signal, current_asset_position).get_skip()
    
        
        if canOpenPosition:
            signal_action.update({"state" : side + (sl, tp)})
            
            leverage = 1
            amount = self.risk_policy(available_amount = available_amount, current_status="Open")
            quantity = amount / price
            risk_action.update({"amount" : amount, "quantity" : quantity, "leverage" : leverage})
        
        elif canclosePosition:
            signal_action.update({"state" : side + (sl, tp)})
        
        else:
            signal_action.update({"state" : ("-", signal, sl, tp)})
            
        return signal_action, risk_action

    
  
  