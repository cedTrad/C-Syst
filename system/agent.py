from .politic import Politic
from .portfolio_manager import Asset, Portfolio
from .following import Following
from .report import Report

from evalutation.postprocessor import Postprocessor

import time
from IPython.display import clear_output


class Event:
    
    def __init__(self, date, price):
        self.date = date
        self.price = price


class Agent:
    
    def __init__(self, agentId, capital, env):
        self.agentId = agentId      # agent = (Id, symbol)
        self.symbol = agentId[1]
        
        self.init_capital = capital
        self.capital = capital
        self.fitness = []
        
        self.env = env
        self.env.initialize_portfolio(capital)
        self.gen_data = self.env.market.get_data(self.symbol)
        self.capital = self.env.capital
        
        self.asset = Asset(self.symbol)
        self.policy = Politic(capital = capital)
        self.following = Following(db=self.env.market.db, post_event=self.env.post_event)
        
    
    def get_event(self):
        self.batchData = next(self.gen_data)
        return Event(date = self.batchData.index[-1], price = self.batchData.iloc[-1]["close"])
    
    
    def update_policy(self, name, params, session_risk_params):
        self.policy.select_rule(name)
        self.policy.update_signal_params(params=params)
        self.policy.update_risk_params(session_params=session_risk_params)
    
    
    def act(self, state):
        signalAction, riskAction = self.policy.perform(batchData = self.batchData, portfolio = state["portfolio"],
                                                       current_asset_position = self.asset.position)
        return signalAction, riskAction
    
    
    def execute(self, state, paper_mode=True):
        event = self.get_event()
        signalAction, riskAction = self.act(state)
        next_state, reward = self.env.step(self.agentId[0], self.asset, event, signalAction, riskAction, paper_mode)
        return next_state, reward, event, signalAction, riskAction
    
    
    def follow(self, i):
        self.following.execute(self.agentId)
    
    
    def run_episode(self):
        state = self.env.reset()
        i = 0
        while True:
            try:
                next_state, reward, event, signalAction, riskAction = self.execute(state)
                state = next_state
                #print(f" Agent : {self.agentId} --- i : {i}")
                if signalAction["state"][1] == "LONG" or signalAction["state"][1] == "SHORT":
                    self.follow(i)
                i += 1
            except StopIteration:
                break
            
    
    def view_report(self):
        self.following.plot_equity()
           
    
    def learn(self):
        ""
        
    def optimize(self):
        self.policy.signal
        