import copy

from .decision.politic import Politic
from .oms import OMS
from .base import Asset

from evalutation.asset.postprocessor import Postprocessor
from evalutation.reporting import Reporting


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
        self.trades_data = None
        self.postindicator = []
        
        self.policy = Politic(capital = allocation)
        self.policy.select_rule(policy_name)
        self.gen_data = self.env.market.get_data(symbol)
        
        self.postprocessor = Postprocessor()
        self.report = Reporting(env)
        
    
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
    
    
    def post_trade(self, event, trades_data, close_trade = False):
        self.trades_data = copy.deepcopy(self.postprocessor.get_data(trades_data))
        if close_trade:
            lines = self.postprocessor.update_indicator(self.symbol)
            lines.update({"date" : event.date, "symbol" : self.symbol})
            self.postindicator.append(lines)
    
    
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
                
            trades_data = self.env.journal.trades_data.copy()
            if "Close" in self.asset.state:
                self.post_trade(event=event, trades_data = trades_data, close_trade=True)
    
    
    def learn(self):
        ""
    
    def get_report(self):
        self.report.get_trades_data(postindicator=self.postindicator, trades_data=self.trades_data,
                                    portfolio_data=self.env.journal.portfolio_data)
        
        fig0, fig1 = self.report.benchmark(self.symbol)
        fig0.show()
        fig1.show()
        
        fig = self.report.plot_asset(symbol=self.symbol)
        fig.show()
        
        fig1, fig2 = self.report.plot_pnl(self.symbol)
        fig1.show()
        fig2.show()
        
        fig2 = self.report.plot_portfolio(self.symbol)
        fig2.show()
        
    def optimize(self):
        self.policy.signal
        