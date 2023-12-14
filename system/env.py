from .base import Portfolio, Asset
from .fsm import FSM
from .market import Market

from evalutation.reporting import GReport, IReport

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


class PDefi:
    def __init__(self):
        self.name = "metamask"
    

class Env:
    
    def __init__(self, symbols, capital, interval = "1d", start = "2023", end = "2023"):
        self.symbols = symbols
        self.capital = capital
        self.init_capital = capital
        self.data = {}
        
        self.journal = Journal()
        self.future_portfolio = PFuture("Binance", capital)
        self.start = start
        self.end = end
        self.market = Market(start = start, end = end, interval = interval)
        
        self.metrics = {}
        
        self.init_portfolio()
        
        
        
    def init_portfolio(self):
        for symbol in self.symbols:
            self.future_portfolio.add_asset(symbol)
    
    
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
        self.execute(asset = asset, price = event.price,
                     signalAction = signalAction, riskAction = riskAction, paper_mode=paper_mode)
        
        self.future_portfolio.update(asset = asset)
        self.journal.add_data(agentId = agentId, date = event.date, price = event.price,
                              asset = asset, portfolio = self.future_portfolio)
        
        state = self.get_state()
        if "Close" in signalAction["state"]:
            reward = asset.pnl
        
        return state, reward
    
    
    def config_agents(self, agentIds):
        self.agentIds = agentIds
        self.greport = GReport(agentIds, db=self.market.db)
    
    
    def pos_data(self):
        self.tradesData, self.portfolioData = self.journal.tradesData, self.journal.portfolioData
        
    
    def get_viz(self, agentId, symbol):
        self.pos_data()
        self.ireport = IReport(agentId, db=self.market.db)
        
        self.ireport.load(self.tradesData, self.portfolioData)
        
        fig0, fig1 = self.ireport.benchmark(symbol)
        fig0.show()
        
        fig = self.ireport.plot_asset(symbol)
        fig.show()
        
        fig1.show()
        
    
    
    def globalReport(self):
        self.pos_data()
        self.greport.load(self.tradesData, self.portfolioData)
        fig_e = self.greport.compare()
        
        fig_e.show()
        
    
    
    def reset(self):
        self.init_portfolio()
        self.future_portfolio.clear()
        
        state = self.get_state()
        return state


