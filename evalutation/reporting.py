from .viz import VizBenchmark, VizAsset, VizPortfolio, VizPnl, VizRisk, CompareViz
from dataEngine.data import connect_db


class Reporting:
    
    def __init__(self, env, agentIds, trades : dict, portfolios : dict):
        self.agentIds = agentIds
        self.trades = trades
        self.portfolios = portfolios
        self.db = env.market.db
    
    
    def get_trades_data(self, postindicator, trades_data, portfolio_data):
        self.postindicator = postindicator
        self.trades_data = trades_data.copy()
        self.portfolio_data = portfolio_data.copy()
    
    
    def benchmark(self, agentId, symbol, side = "all"):
        
        trades = self.trades_data[agentId][side]
        
        viz_benchmark = VizBenchmark(agentId, trades, self.portfolio_data)
        fig_pt = viz_benchmark.per_trade(symbol)
        fig_v = viz_benchmark.values(symbol)
        
        return fig_pt, fig_v
    
        
    def plot_asset(self, agentId, symbol, side = "all"):
        
        data = self.db.get_data(symbol)
        trades = self.trades_data[agentId][side]
        
        viz_asset = VizAsset(agentId, trades)
        fig = viz_asset.candle(data=data)
        return fig
    
    
    def plot_portfolio(self, agentId):
        viz_port = VizPortfolio(agentId, self.portfolio_data)
        fig = viz_port.show()
        return fig 
    
    
    def plot_pnl(self, agentId, symbol):
        
        viz_pnl = VizPnl(agentId, self.trades_data)
        fig = viz_pnl.long_short_per_step(symbol)
        fig_t = viz_pnl.long_short_per_trade(symbol)
        return fig, fig_t

    
    def plot_risk(self):
        ""
    
    
    def compare(self, symbol):
        compare_agent = CompareViz(self.agentIds, self.trades_data, self.portfolio_data)
        fig_e = compare_agent.equity(symbol)
        fig_p = compare_agent.pnl()
        
        