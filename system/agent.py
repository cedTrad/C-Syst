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
        
        self.count_trade = 0
        
        self.env = env
        self.env.initialize_portfolio(capital)
        
        self.asset = Asset(self.symbol)
        
        self.fitness = []
        self.postindicator = []
        
        self.policy = Politic(capital = capital)
        
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
        next_state, reward = self.env.step(self.agentId[0], self.asset, event, signalAction, riskAction, paper_mode)
        
        return next_state, reward, event, signalAction, riskAction
    
    
    def follow(self, i):
        db = self.env.market.db
        post_event = self.env.post_event
        self.following = Following(db=db, post_event=post_event)
        self.following.execute(self.agentId)


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
                    self.follow(i)
                
                i += 1
                print(f" Agent : {self.agentId} - {self.symbol}")                
                
            except StopIteration:
                break
            
    
    def view_report(self):
        self.following.plot_equity()
           
    
    def learn(self):
        ""
        
    def optimize(self):
        self.policy.signal
        