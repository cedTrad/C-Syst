from .base import Portfolio, Asset
from .fsm import FSM
from .market import Market

from evalutation.reporting import IReport

from dataEngine.journal import Journal

signalAction = ["Open", "Close", "Resize", "-", None]
riskAction = ["quantity", "leverage", "closePrice", "sl", "tp"]



class PFuture(Portfolio):    
    def __init__(self, name, capital):
        #Portfolio.__init__(self, name, capital)
        super().__init__(name, capital)
        self.long = {}
        self.short = {}
        self.long_portfolio = 0
        self.short_portfolio = 0


    

class MEnv:
    
    def __init__(self, symbol, capital, interval = "1d", start = "2023", end = "2023"):
        self.symbol = symbol
        self.capital = capital
        self.data = {}
        
        self.journal = Journal()
        self.future_portfolio = PFuture("Binance", capital)
        self.future_portfolio.add_asset(symbol)
        
        self.start = start
        self.end = end
        self.market = Market(start = start, end = end, interval = interval)
        
        
        
    
    def get_state(self):
        portfolio = {"capital" : self.future_portfolio.capital,
                    "risk_value" : self.future_portfolio.risk_value,
                    "save_value" : self.future_portfolio.save_value,
                    "available_value" : self.future_portfolio.available_value
                    }
        indicator = {"average": 0, "dist_sl" : 0, "profit_factor" : 0, 
                     "win_rate" : 0, "drawdown": 0, "recovery" : 0}
        return {"portfolio" : portfolio, "indicator" : indicator}
    
    
    def execute(self, asset, price, signalAction, riskAction, paper_mode):
        current_state = (asset.state, asset.type, asset.tp, asset.sl)
        fsm = FSM(current_state, signalAction, riskAction, paper_mode)
        fsm.perform(asset=asset, price=price, portfolio=self.future_portfolio)
        
    
    def step(self, agentId, asset, event, signalAction, riskAction, paper_mode = True):
        reward = 0
        self.execute(asset = asset, price = event.price, signalAction = signalAction,
                     riskAction = riskAction, paper_mode=paper_mode)
        self.future_portfolio.update(asset = asset)
        self.journal.add_data(agentId = agentId[0], date = event.date, price = event.price,
                              asset = asset, portfolio = self.future_portfolio)
        
        state = self.get_state()
        
        if "Close" in signalAction["state"]:
            reward = asset.pnl
        
        return state, reward
    
        
    
    def reset(self):
        self.future_portfolio.add_asset(self.symbol)
        self.future_portfolio.clear()
        
        state = self.get_state()
        return state


