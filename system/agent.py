from .politic import Politic
from .portfolio_manager import Asset, Portfolio
from .monitoring import Monitoring
from .report import Report

from evalutation.postprocessor import Postprocessor

import time
from IPython.display import clear_output


class Event:
    
    def __init__(self, date, price):
        self.date = date
        self.price = price

class Agent:
    
    def __init__(self, Id, capital, env):
        self.Id = Id[0]
        self.symbol = Id[1]
        
        self.init_capital = capital
        self.capital = capital
        
        self.count_trade = 0
        
        self.env = env
        self.asset = Asset(self.symbol)
        
        self.fitness = []
        self.postindicator = []
        
        self.policy = Politic(capital = capital)
        self.mtng = Monitoring()
        
        self.gen_data = self.env.market.get_data(self.symbol)
        
    
    def get_event(self):
        self.batchData = next(self.gen_data)
        return Event(date = self.batchData.index[-1], price = self.batchData.iloc[-1]["close"])
        
    
    def act(self, state):
        signalAction, riskAction = self.policy.perform(batchData = self.batchData, portfolio = state["portfolio"],
                                                       current_asset_position = self.asset.position)
        return signalAction, riskAction
    
    
    def execute(self, state, paper_mode=True):
        event = self.get_event()
        signalAction, riskAction = self.act(state)
        next_state, reward = self.env.step(self.Id, self.asset, event, signalAction, riskAction, paper_mode)
        
        return next_state, reward, event, signalAction, riskAction
    
    
    def update_metric(self, signal = True):
        if signal[0] == "Close":
            self.count_trade += 1
            journal = self.env.journal
            metrics = self.mtng.update_metric(self.Id, journal)
    
    
    def monitoring(self, i):
        tradeData = self.env.post_event.tradeData
        f_var = ["pnl", "pnl_pct", "value"]
        tradeData.iloc[i]
        
        

    def update_policy(self, name, params):
        self.policy.select_rule(name)
        self.policy.update_signal_params(params=params)
    
    
    def run_episode(self):
        state = self.env.reset()
        i = 0
        while True:
            try:
                next_state, reward, event, signalAction, riskAction = self.execute(state)
                state = next_state
                print(signalAction)
                print("i : ",i)
                if signalAction["state"][1] == "LONG" or signalAction["state"][1] == "SHORT":
                    self.monitoring(i)
                
                i += 1
                print(f" Agent : {self.Id} - {self.symbol}")                
                
            except StopIteration:
                break
            
    
    def view_report(self):
        db = self.env.market.db
        post_event = self.env.post_event
        report = Report(db, post_event)
        report.plot_equity(self.Id)
           
    
    def learn(self):
        ""
        
    def optimize(self):
        self.policy.signal
        