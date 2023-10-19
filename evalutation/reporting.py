from .viz import VizAsset
from dataEngine.data import connect_db

class Reporting:
    
    def __init__(self, env):
        self.db = env.market.db
        self.viz_asset = VizAsset()
    
    
    def get_trades_data(self, symbol, postindicator, trades_data):
        self.postindicator = postindicator
        self.trades_data = trades_data
        
        
    def plot_asset(self, symbol, type_ = "all"):
        data = self.db.get_data(symbol)
        trades = self.trades_data[symbol][type_]
        
        fig = self.viz_asset.candle(trades=trades, data=data)
        return fig
            
    