
from .signal import Signal
from .management import Management

from .transition import Transition


class Politic:
    
    def __init__(self, capital):
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
    
    def get_signal(self, data):
        self.signal.sets(data)
        self.rule = self.signal.rules.get(self.policy_name)
        if self.rule is None:
            raise Exception("Policy name incorrect")
        
        self.rule.update_params(self.params)
        
        points = self.rule.run()
        signal = self.signal_policy(points)
        return signal
        
        
    def perform(self, data, portfolio, current_asset_position):
        capital, available_amount = portfolio["capital"], portfolio["available_value"]
        
        signal_action = {}
        risk_action = {}
        
        price = data.iloc[-1]["close"]
        signal = self.get_signal(data)
        
        sl = False
        tp = False
        
        open_state = Transition(signal, current_asset_position).get_in()
        close_state = Transition(signal, current_asset_position).get_out()
        skip = Transition(signal, current_asset_position).get_skip()
    
        
        if open_state is not False:
            signal_action.update({"state" : ("Open", signal, sl, tp)})
            
            leverage = 1
            amount = self.risk_policy(available_amount = available_amount, current_status="Open")
            quantity = amount / price
            risk_action.update({"amount" : amount, "quantity" : quantity, "leverage" : leverage})
        
        elif close_state is not False:
            signal_action.update({"state" : (close_state) + (sl, tp)})
        
        else:
            signal_action.update({"state" : ("-", signal, sl, tp)})
            
        return signal_action, risk_action
    
    