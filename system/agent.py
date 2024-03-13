from .politic import Politic
from .portfolio_manager import Asset, Portfolio

from .utils import Event

class Agent:
    
    def __init__(self, Id, env):
        self.Id = Id[0]
        self.symbol = Id[1]
        self.capital = env.capital
        
        self.env = env
        self.asset = Asset(self.symbol)
        
        self.fitness = []
        self.postindicator = []
        
        self.policy = Politic(capital = env.capital)
        self.gen_data = self.env.market.get_data(self.symbol)
        
    
    def get_event(self):
        self.batchData = next(self.gen_data)
        return Event(date = self.batchData.index[-1], price = self.batchData.iloc[-1]["close"])
        
    
    def act(self, state):
        signalAction, riskAction = self.policy.perform(batchData = self.batchData, portfolio = state["portfolio"],
                                                       current_asset_position = self.asset.position)
        return signalAction, riskAction
    
    
    def update(self, state, paper_mode=True):
        event = self.get_event()
        signalAction, riskAction = self.act(state)
        next_state, reward = self.env.step(self.Id, self.asset, event, signalAction, riskAction, paper_mode)
        return next_state, reward, event
    
    
    def post_trade(self, event, close_trade = False):
        if close_trade:
            self.env.set_evaluation()
            indicators = self.env.postprocessor.update_indicator(self.Id)
            indicators.update({"date" : event.date, "symbol" : self.symbol})
            self.postindicator.append(indicators)
    
    
    def update_policy(self, name, params):
        self.policy.select_rule(name)
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
                
    
    def learn(self):
        ""
        
        
    def get_report(self):
        ""

        
    def optimize(self):
        self.policy.signal
        