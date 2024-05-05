from .ffc.fsm import FSM
from .portfolio_manager import PFuture
from .event import MarketEvent, PostEvent


signalAction = ["Open", "Close", "Resize", "-", None]
riskAction = ["quantity", "leverage", "closePrice", "sl", "tp"]


class GEnv:
    
    def __init__(self, symbols, interval = "1d", start = "2023", end = "2023"):
        self.symbols = symbols
        
        self.start = start
        self.end = end
        
        self.post_event = PostEvent()
        self.market = MarketEvent(size=50, start = start, end = end, interval = interval)
        
        self.metrics = {}
        
    
    def initialize_portfolio(self, capital):
        self.init_capital = capital
        self.portfolio = PFuture("Binance", capital)
        for symbol in self.symbols:
            self.portfolio.add_asset(symbol)
        
        
    def g_report(self):
        ""




class Env:
    
    def __init__(self, symbol, interval = "1d", start = "2023", end = "2023"):
        self.symbol = symbol
        self.start = start
        self.end = end
        self.post_event = PostEvent()
        self.market = MarketEvent(size=50, start = start, end = end, interval = interval)
    
    
    def initialize_portfolio(self, capital):
        self.init_capital = capital
        self.portfolio = PFuture("Binance", capital)
        self.portfolio.add_asset(self.symbol)
        self.capital = self.portfolio.capital
        
        
    def get_state(self):
        portfolio = {"capital" : self.portfolio.capital,
                    "risk_value" : self.portfolio.risk_value,
                    "save_value" : self.portfolio.save_value,
                    "available_value" : self.portfolio.available_value
                    }
        indicator = {"average": 0, "dist_sl" : 0, "profit_factor" : 0, 
                     "win_rate" : 0, "drawdown": 0, "recovery" : 0}
        return {"portfolio" : portfolio, "indicator" : indicator}
    
    
    def execute(self, asset, price, signalAction, riskAction, paper_mode):
        current_state = (asset.state, asset.type, asset.tp, asset.sl)
        fsm = FSM(current_state, signalAction, riskAction, paper_mode)
        fsm.perform(asset=asset, price=price, portfolio=self.portfolio)
        
    
    def step(self, agentId, asset, event, signalAction, riskAction, n_session, paper_mode = True):
        reward = 0
        self.execute(asset = asset, price = event.price, signalAction = signalAction,
                     riskAction = riskAction, paper_mode=paper_mode)
        self.portfolio.update(asset = asset)
        self.post_event.add_data(agentId = agentId, date = event.date, price = event.price,
                              asset = asset, portfolio = self.portfolio, n_session = n_session)
        state = self.get_state()
        
        if "Close" in signalAction["state"]:
            reward = asset.pnl
        
        return state, reward
    
        
    def reset(self):
        self.portfolio.add_asset(self.symbol)
        self.portfolio.clear()
        
        state = self.get_state()
        return state


