from evalutation.asset.processing import Processing    
from evalutation.asset.metrics import Metric

from evalutation.portfolio.processing import Processing as PProcessing

class Postprocessor:
    
    def __init__(self):
        self.metric = Metric()
        self.processAsset = Processing()
        self.processPort = PProcessing()
        self.type = ["all", "long", "short"]
        #self.type = ["all"]
    
    
    def get_data(self, trades_data, portfolio_data):
        trades_data = self.processAsset.load(trades_data)
        portfolio_data = self.processPort.load(portfolio_data)
        
        self.trades = self.processAsset.split_asset(trades_data)
        self.portfolios = self.processPort.split_by_agent(portfolio_data)
    
    
    def update_indicator(self, symbol):
        lines = {}
        data = self.trades[symbol]
        for data_type in self.type:
            trade = data[data_type].copy()
            metrics = self.metric.excecute(trade = trade)
            lines[data_type] = metrics
        return lines
    
    

