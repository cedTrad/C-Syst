from .viz import VizBenchmark, VizAsset, VizPortfolio, VizPnl, VizRisk
from dataEngine.data import connect_db


class Reporting:
    
    def __init__(self, env):
        self.db = env.market.db
        self.viz_asset = VizAsset()
    
    
    def get_trades_data(self, postindicator, trades_data, portfolio_data):
        self.postindicator = postindicator
        self.trades_data = trades_data.copy()
        self.portfolio_data = portfolio_data.copy()
    
    
    def benchmark(self, symbol):
        viz_benchmark = VizBenchmark(self.trades_data, self.portfolio_data)
        fig = viz_benchmark.per_trade(symbol)
        fig1 = viz_benchmark.values(symbol)
        
        return fig, fig1
    
        
    def plot_asset(self, symbol, type_ = "all"):
        data = self.db.get_data(symbol)
        trades = self.trades_data[symbol][type_]
        
        fig = self.viz_asset.candle(trades=trades, data=data)
        return fig
    
    
    def plot_portfolio(self, symbol):
        viz_port = VizPortfolio(self.portfolio_data, symbol)
        fig = viz_port.show()
        return fig 
    
    def plot_pnl(self, symbol):
        viz_pnl = VizPnl(self.trades_data)
        fig = viz_pnl.long_short_per_step(symbol)
        fig_t = viz_pnl.long_short_per_trade(symbol)
        return fig, fig_t

    
    def plot_risk(self):
        ""
    