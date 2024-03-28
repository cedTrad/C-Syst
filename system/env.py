from .ffc.fsm import FSM
from .portfolio_manager import PFuture, Asset

from .event import MarketEvent, PostEvent

from evalutation.reporting import GReport, IReport

signalAction = ["Open", "Close", "Resize", "-", None]
riskAction = ["quantity", "leverage", "closePrice", "sl", "tp"]


class GEnv:
    
    def __init__(self, symbols, capital, interval = "1d", start = "2023", end = "2023"):
        self.symbols = symbols
        self.capital = capital
        self.init_capital = capital
        self.data = {}
        
        self.post_event = PostEvent()
        
        self.portfolio = PFuture("Binance", capital)
        self.start = start
        self.end = end
        
        self.market = MarketEvent(start = start, end = end, interval = interval)
        
        self.metrics = {}
        
        self.init_portfolio()
        
        
    def init_portfolio(self):
        for symbol in self.symbols:
            self.portfolio.add_asset(symbol)
    
    
    def get_state(self):
        
        market_data = {"price" : 1000}
        
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
        
    
    def step(self, agentId, asset, event, signalAction, riskAction, paper_mode = True):
        reward = 0
        self.execute(asset = asset, price = event.price,
                     signalAction = signalAction, riskAction = riskAction, paper_mode=paper_mode)
        
        self.portfolio.update(asset = asset)
        self.post_event.add_data(agentId = agentId, date = event.date, price = event.price,
                              asset = asset, portfolio = self.portfolio)
        
        state = self.get_state()
        if "Close" in signalAction["state"]:
            reward = asset.pnl
        
        return state, reward
    

    
    def reset(self):
        self.init_portfolio()
        self.portfolio.clear()
        
        state = self.get_state()
        return state




class Env:
    
    def __init__(self, symbol, capital, interval = "1d", start = "2023", end = "2023"):
        self.symbol = symbol
        self.capital = capital
        self.data = {}
        
        self.post_event = PostEvent()
        
        self.portfolio = PFuture("Binance", capital)
        self.portfolio.add_asset(symbol)
        
        self.start = start
        self.end = end
        self.market = MarketEvent(start = start, end = end, interval = interval)
        
        
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
        
    
    def step(self, agentId, asset, event, signalAction, riskAction, paper_mode = True):
        reward = 0
        self.execute(asset = asset, price = event.price, signalAction = signalAction,
                     riskAction = riskAction, paper_mode=paper_mode)
        self.portfolio.update(asset = asset)
        self.post_event.add_data(agentId = agentId, date = event.date, price = event.price,
                              asset = asset, portfolio = self.portfolio)
        state = self.get_state()
        
        if "Close" in signalAction["state"]:
            reward = asset.pnl
        
        return state, reward
    
    
    
    def get_report(self, agentId, symbol, viz = True):
        self.tradesData, self.portfolioData = self.journal.tradesData, self.journal.portfolioData
        
        self.ireport = IReport(agentId, db=self.market.db)
        self.ireport.load(self.tradesData, self.portfolioData)
        
        if viz:
            fig0, fig1 = self.ireport.benchmark(symbol)
            fig = self.ireport.plot_asset(symbol)
            
            fig0.show()
            fig1.show()
            fig.show()
        
        
    def reset(self):
        self.portfolio.add_asset(self.symbol)
        self.portfolio.clear()
        
        state = self.get_state()
        return state


