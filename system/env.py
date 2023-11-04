from .base import Portfolio, Asset
from .fsm import FSM
from .market import Market

from evalutation.reporting import Reporting
from evalutation.postprocessor import Postprocessor

from dataEngine.journal import Journal

signal_action = ["Open", "Close", "Resize", "-", None]
risk_action = ["quantity", "leverage", "closePrice", "sl", "tp"]



class PFuture(Portfolio):    
    def __init__(self, name, capital):
        Portfolio.__init__(self, name, capital)
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
        self.market = Market(start = start, end = end, interval = interval)
        
        self.init_portfolio()
        self.postprocessor = Postprocessor()
        
        
    def init_portfolio(self):
        for symbol in self.symbols:
            self.future_portfolio.add_asset(symbol)
            
    
    def config_agents(self, agentIds):
        self.agentIds = agentIds
        self.report = Reporting(agentIds, db=self.market.db)
    
    
    def get_state(self):
        portfolio = {"capital" : self.future_portfolio.capital,
                    "risk_value" : self.future_portfolio.risk_value,
                    "save_value" : self.future_portfolio.save_value,
                    "available_value" : self.future_portfolio.available_value
                    }
        indicator = {"average": 0, "dist_sl" : 0, "profit_factor" : 0, 
                     "win_rate" : 0, "drawdown": 0, "recovery" : 0}
        return {"portfolio" : portfolio, "indicator" : indicator}
    
    
    def execute(self, asset, price, signal_action, risk_action, paper_mode):
        current_state = (asset.state, asset.type, asset.tp, asset.sl)
        
        fsm = FSM(current_state, signal_action, risk_action, paper_mode)
        fsm.perform(asset=asset, price=price, portfolio=self.future_portfolio)
        
    
    def step(self, agentId, asset, event, signal_action, risk_action, paper_mode = True):
        reward = 0
        self.execute(asset = asset, price = event.price,
                     signal_action = signal_action, risk_action = risk_action, paper_mode=paper_mode)
        
        self.future_portfolio.update(asset = asset)
        self.journal.add_data(agentId = agentId, date = event.date, price = event.price,
                              asset = asset, portfolio = self.future_portfolio)
        
        state = self.get_state()
        if "Close" in signal_action["state"]:
            reward = asset.pnl
        
        return state, reward
    
    
    def process(self):
        tradesData = self.journal.tradesData
        portfolioData = self.journal.portfolioData
        self.trades, self.portfolios, self.tradesData, self.portfolioData = self.postprocessor.load(tradesData, portfolioData)
    
    
    def update_indicator(self):
        self.process()
        
    
    
    def get_report(self, agentId, symbol):
        self.process()
        
        self.report.load(self.trades, self.portfolios)
        
        fig0, fig1 = self.report.benchmark(agentId, symbol)
        fig0.show()
        
        fig = self.report.plot_asset(agentId, symbol)
        fig.show()
        
        fig1.show()
        
       #fig2 = self.report.plot_portfolio(self.agentId)
        #fig2.show()
        
    
    
    def globalReport(self):
        self.report.load(self.trades, self.portfolios)
        fig_e, fig_p = self.report.compare()
        
        fig_e.show()
        fig_p.show()
        
    
    
    def reset(self):
        self.init_portfolio()
        self.future_portfolio.clear()
        
        state = self.get_state()
        return state


