from typing import Any
from evalutation.asset.processing import Processing    
from evalutation.asset.metrics import Metric

from evalutation.portfolio.processing import Processing as PProcessing
        
                
class Postprocessor:
    
    def __init__(self):
        self.processAsset = Processing()
        self.processPort = PProcessing()
    
    
    def load(self, tradesData, portfolioData):
        tradesData = self.processAsset.load(tradesData)
        portfolioData = self.processPort.load(portfolioData)
        
        self.trades = self.processAsset.split_asset_by_agent()
        self.portfolios = self.processPort.split_by_agent()
        return self.trades, self.portfolios, tradesData, portfolioData
    
    
    def gen_data(self, agentId):
        return Metric(self.trades[agentId]).update()
    
    
    def update_metric(self, agentId):
        metrics = []
        metric = self.gen_data(agentId)
        while True:
            try:
                metrics.append(
                    next(metric)
                    )
                
            except (StopIteration, IndexError):
                break
            
        return metrics
    
    
    
