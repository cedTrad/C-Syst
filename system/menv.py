from .fsm import FSM
from .market import Market
from portfolio_manager import PFuture, Asset

from evalutation.reporting import IReport

from dataEngine.journal import Journal

signalAction = ["Open", "Close", "Resize", "-", None]
riskAction = ["quantity", "leverage", "closePrice", "sl", "tp"]



class MEnv:
    
    def __init__(self, symbol, capital, interval = "1d", start = "2023", end = "2023"):
        self.symbol = symbol
        self.capital = capital
        self.data = {}
        
        self.journal = Journal()
        self.portfolio = PFuture("Binance", capital)
        self.portfolio.add_asset(symbol)
        
        self.start = start
        self.end = end
        self.market = Market(start = start, end = end, interval = interval)
        
        
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
        self.journal.add_data(agentId = agentId[0], date = event.date, price = event.price,
                              asset = asset, portfolio = self.portfolio)
        
        state = self.get_state()
        
        if "Close" in signalAction["state"]:
            reward = asset.pnl
        
        return state, reward
    
    
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
        
    
    def reset(self):
        self.portfolio.add_asset(self.symbol)
        self.portfolio.clear()
        
        state = self.get_state()
        return state


