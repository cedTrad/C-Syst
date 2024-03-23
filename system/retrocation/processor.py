from typing import Any
from .metrics import AMetric
from .postprocessing import APostprocessing, PPostprocessing


class Processor:
    
    def __init__(self, capital):
        self.processAsset = APostprocessing(capital)
        self.processPort = PPostprocessing()
    

    def transform(self, tradesData, portfolioData):
        tradesData = self.processAsset.transform(tradesData)
        portfolioData = self.processPort.transform(portfolioData)

        return tradesData, portfolioData
    
    
    def gen_data(self, tradeDataAgent):
        return AMetric(tradeDataAgent).update()
    
    
    def update_metric(self, tradeDataAgent):
        metrics = []
        metric = self.gen_data(tradeDataAgent)
        while True:
            try:
                metrics.append(
                    next(metric)
                    )
                
            except (StopIteration, IndexError):
                break
            
        return metrics
    
    
    
