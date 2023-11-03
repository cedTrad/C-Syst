from evalutation.asset.processing import Processing    
from evalutation.asset.metrics import Metric

from evalutation.portfolio.processing import Processing as PProcessing


class Postprocessor:
    
    def __init__(self):
        self.metric = Metric()
        self.processAsset = Processing()
        self.processPort = PProcessing()
    
    
    def get_data(self, tradesData, portfolioData):
        trades_data = self.processAsset.load(tradesData)
        self.processPort.load(portfolioData)
        
        self.trades = self.processAsset.split_asset_by_agent(trades_data)
        self.portfolios = self.processPort.split_by_agent()
        return self.trades, self.portfolios
    
    
    def update_indicator(self, agentId):
        trades = self.trades[agentId]
        indicators = self.metric.excecute(trade = trades)
        return indicators
    
    

