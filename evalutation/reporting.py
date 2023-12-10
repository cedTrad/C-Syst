from .viz import VizBenchmark, VizAsset, VizPortfolio, VizPnl, VizRisk, GlobalViz
from .postprocessor import Postprocessor


class GReport:
    
    def __init__(self, agentIds, db):
        self.agentIds = agentIds
        self.db = db
        self.postprocessor = Postprocessor()
        
    def load(self, tradesData, portfolioData):
        self.trades, self.portfolios, _, _ = self.postprocessor.load(tradesData, portfolioData)
    
    def plot_portfolio(self, agentId):
        viz_port = VizPortfolio(agentId, self.portfolios)
        fig = viz_port.show()
        return fig 
    
    def plot_pnl(self):
        ""
    
    def compare(self):
        compare_agent = GlobalViz(self.agentIds, self.trades, self.portfolios)
        fig_e = compare_agent.equity()
        #fig_p = compare_agent.pnl()
        return fig_e
    
    


class IReport:
    
    def __init__(self, agentId, db):
        self.agentId = agentId
        self.db = db
        self.postprocessor = Postprocessor()


    def load(self, tradesData, portfolioData):
        self.trades, self.portfolios, self.tradesData, self.portfolioData = self.postprocessor.load(tradesData, portfolioData)    
            
            
    def plot_asset(self, symbol):
        data = self.db.get_data(symbol)
        viz_asset = VizAsset(self.agentId, self.trades)
        fig = viz_asset.candle(data = data)
        return fig
    
    def benchmark(self, symbol):
        viz_benchmark = VizBenchmark(agentId=self.agentId, trades=self.trades, portfolios=self.portfolios)
        fig_pt = viz_benchmark.per_trade(symbol)
        fig_v = viz_benchmark.values(symbol)
        return fig_pt, fig_v
    
        
        