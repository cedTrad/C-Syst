from .politic import Politic
from .portfolio_manager import Asset, Portfolio
from .monitoring import Monitoring
from .report import Report

from .event import Event

from evalutation.postprocessor import Postprocessor

import time
from IPython.display import clear_output

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
        self.mtng = Monitoring()
        
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
        return next_state, reward, event, signalAction
    
    
    def monitoring(self, signal = True):
        if signal[0] == "Close":
            journal = self.env.journal
            metrics = self.mtng.update_metric(self.Id, journal)
    
    
    def update_policy(self, name, params):
        self.policy.select_rule(name)
        self.policy.update_signal_params(params=params)
    
    
    def run_episode(self):
        state = self.env.reset()
        i = 0
        while True:
            try:
                next_state, reward, event, signal = self.update(state)
                state = next_state
                i += 1
                
                print(f" Agent : {self.Id}")
                print(f" i {i}")
                self.monitoring(signal["state"])
                
            except StopIteration:
                break
            
    
    def view_report(self):
        db = self.env.market.db
        report = Report(db, self.mtng)
        report.plot_equity_i(self.Id)
           
    
    def learn(self):
        ""
        
    def optimize(self):
        self.policy.signal
        