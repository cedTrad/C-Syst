from .viz import VizBenchmark, VizAsset, VizPortfolio, VizPnl, VizRisk
from dataEngine.data import connect_db


class Reporting:
    
    def __init__(self, env):
        self.db = env.market.db
        self.viz_asset = VizAsset()
    
    
    def get_trades_data(self, postindicator, trades_data, portfolio_data):
        self.postindicator = postindicator
        self.trades_data = trades_data
        self.portfolio_data = portfolio_data
    
    
    def benchmark(self, symbol):
        viz_benchmark = VizBenchmark(self.trades_data)
        fig = viz_benchmark.show(symbol)
        return fig
    
        
    def plot_asset(self, symbol, type_ = "all"):
        data = self.db.get_data(symbol)
        trades = self.trades_data[symbol][type_]
        
        fig = self.viz_asset.candle(trades=trades, data=data)
        return fig
    
    
    def plot_portfolio(self):
        viz_port = VizPortfolio(self.portfolio_data)
        fig = viz_port.show()
        return fig 
    
    def plot_pnl(self, symbol):
        viz_pnl = VizPnl(self.trades_data)
        fig = viz_pnl.long_short(symbol)
        return fig
        
        
        
    def plot_risk(self):
        ""
    