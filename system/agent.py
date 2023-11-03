import copy

from .decision.politic import Politic
from .oms import OMS
from .base import Asset


class Event:
     def __init__(self, date, price):
         self.date = date
         self.price = price
         

class Agent:
    
    def __init__(self, agentId, symbol, allocation, env, policy_name):
        self.agentId = agentId
        self.symbol = symbol
        self.allocation = allocation
        
        self.env = env
        
        self.asset = Asset(symbol)
        self.policy_name = policy_name
        
        self.fitness = []
        self.postindicator = []
        
        self.policy = Politic(capital = allocation)
        self.policy.select_rule(policy_name)
        self.gen_data = self.env.market.get_data(symbol)
        


    
    def get_event(self):
        self.data = next(self.gen_data)
        return Event(date = self.data.index[-1], price = self.data.iloc[-1]["close"])
        
    
    def act(self, state):
        signal_action, risk_action = self.policy.perform(data = self.data, portfolio = state["portfolio"],
                                                       current_asset_position = self.asset.position)
        return signal_action, risk_action
    
    
    def update(self, state):
        event = self.get_event()
        signal_action, risk_action = self.act(state)
        next_state, reward = self.env.step(self.agentId, self.asset, event, signal_action, risk_action)
        return next_state, reward, event
    
    
    def post_trade(self, event, close_trade = False):
        if close_trade:
            self.env.set_evaluation()
            indicators = self.env.postprocessor.update_indicator(self.agentId)
            indicators.update({"date" : event.date, "symbol" : self.symbol})
            self.postindicator.append(indicators)
    
    
    def update_policy_params(self, params):
        self.policy.update_signal_params(params=params)
    
    
    def run_episode(self):
        state = self.env.reset()
        i = 0
        while True:
            try:
                next_state, reward, event = self.update(state)
                state = next_state
                i += 1
            except StopIteration:
                break
                
            #if "Close" in self.asset.state:
            #    self.post_trade(event=event, close_trade=True)
    
    
    def learn(self):
        ""
        
        
    def get_report(self):
        ""

        
    def optimize(self):
        self.policy.signal
        