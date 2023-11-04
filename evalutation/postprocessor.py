from typing import Any
from evalutation.asset.processing import Processing    
from evalutation.asset.metrics import Metric

from evalutation.portfolio.processing import Processing as PProcessing


class TradesData:
    
    def __init__(self, tradesData):
        self.tradesData = tradesData
        self.nbTrades = 0
        self.winTrades = 0
        self.lossTrades = 0
    
    def genere(self):
        i = j = 0
        while True:
            j += 1
            data = self.tradesData.iloc[i : j+1]
            if self.tradesData.iloc[j]["status"] == "Close":
                i = j+1
                self.nbTrades += 1
                pnl = self.tradesData["pnl"].iloc[j]
                if pnl > 0:
                    self.winTrades += 1
                else:
                    self.lossTrades += 1
                    
                yield data

                
                
class Postprocessor:
    
    def __init__(self):
        self.metric = Metric()
        self.processAsset = Processing()
        self.processPort = PProcessing()
    
    
    def load(self, tradesData, portfolioData):
        tradesData = self.processAsset.load(tradesData)
        portfolioData = self.processPort.load(portfolioData)
        
        self.trades = self.processAsset.split_asset_by_agent()
        self.portfolios = self.processPort.split_by_agent()
        return self.trades, self.portfolios, tradesData, portfolioData
    
    
    def gen_data(self, agentId):
        return TradesData(self.trades[agentId]).update()
        #return Metric(self.trades[agentId]).update()
    
    
    def update_indicator(self, agentId):
        trades = self.trades[agentId]
        
        t = self.gen_data(agentId)
        
        indicators = self.metric.execute(trade = trades)
        return indicators
    
    
    def for_report(self, agentId):
        indicators = []
        trades = self.gen_data(agentId)
        while True:
            try:
                indicator = self.metric.execute(trade = next(trades))
                indicators.append(indicator)
            except (StopIteration, IndexError):
                break
        return indicators

