from .politic import Politic
from .portfolio_manager import Asset, Portfolio
from .following import Following

from .session_manager import SessionManager

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
        self.post_event = self.env.post_event
        self.gen_data = self.env.market.get_data(self.symbol)
        self.capital = self.env.capital
        
        self.asset = Asset(self.symbol)
        self.policy = Politic(capital = capital)
        self.following = Following(db=self.env.market.db, post_event=self.env.post_event)
        self.session = SessionManager(self.following)
    
    
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
        return event, next_state, reward, event, signalAction, riskAction
    
    
    def follow(self, event, signal):
        if signal["state"][1] == "LONG" or signal["state"][1] == "SHORT":
            self.following.execute(self.agentId)
            tradeData = self.following.tradeData
            self.session.actuator(tradeData)
            self.post_event.add_session(event.date, self.agentId[0], self.session.n_session)
        else:
            self.post_event.add_session(event.date, self.agentId[0], "-")
    
    
    def run_episode(self):
        state = self.env.reset()
        i = 0
        while True:
            try:
                event, next_state, reward, event, signalAction, riskAction = self.execute(state)
                state = next_state
                self.follow(event=event, signal=signalAction)
                i += 1
            except StopIteration:
                break
            
    
    def view_report(self):
        self.following.plot_equity()
           
    
    def learn(self):
        ""
        
    def optimize(self):
        self.policy.signal
        