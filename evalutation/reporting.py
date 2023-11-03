from .viz import VizBenchmark, VizAsset, VizPortfolio, VizPnl, VizRisk, CompareViz
from dataEngine.data import connect_db


class Reporting:
    
    def __init__(self, agentIds, db):
        self.agentIds = agentIds
        self.db = db
        
    
    def load(self, trades : dict, portfolios : dict):
        self.trades = trades
        self.portfolios = portfolios
    
    
    def benchmark(self, agentId, symbol):
        viz_benchmark = VizBenchmark(agentId, self.trades, self.portfolios)
        fig_pt = viz_benchmark.per_trade(symbol)
        fig_v = viz_benchmark.values(symbol)
        return fig_pt, fig_v
    
        
    def plot_asset(self, agentId, symbol):
        
        data = self.db.get_data(symbol)
        viz_asset = VizAsset(agentId, self.trades)
        fig = viz_asset.candle(data=data)
        return fig
    
    
    def plot_portfolio(self, agentId):
        viz_port = VizPortfolio(agentId, self.portfolios)
        fig = viz_port.show()
        return fig 
    
    
    def plot_pnl(self):
        ""

    
    def plot_risk(self):
        ""
    
    
    def compare(self):
        compare_agent = CompareViz(self.agentIds, self.trades, self.portfolios)
        fig_e = compare_agent.equity()
        fig_p = compare_agent.pnl()
        return fig_e, fig_p
    
    
        
        