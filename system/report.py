from .retrocation.processor import Processor
from .viz import Benchmark


class Report:
    
    def __init__(self, db, post_event):
        self.db = db
        self.processor = Processor()
        self.tradeData = post_event.tradeData
        self.portfolioData = post_event.portfolioData
        self.metricData = post_event.metricData
        
    
    def processing(self, agentId):
        self.processor.transform(self.tradeData, self.portfolioData)
        
        symbol = self.tradeData.iloc[0]["symbol"]
        data = self.db.get_data(symbol)
        AgentId = {"Id" : agentId, "symbol" : symbol,
                    "tradeDataAgent" : self.tradeData,
                    "portfolioDataAgent" : self.portfolioData,
                    "metricDataAgent" : self.metricData,
                    "data" : data}
        
        return AgentId
        
    
    def plot_equity(self, agentId):
        
        Agent = self.processing(agentId)
        tradeDataAgent = Agent["tradeDataAgent"]
        portfolioDataAgent = Agent["portfolioDataAgent"]
        data = Agent["data"]
    
        benchmark = Benchmark(tradeDataAgent, portfolioDataAgent)
        
        fig_equ = benchmark.equity()
        fig_equ.show()
        
        fig_asset = benchmark.asset(data)
        fig_asset.show()
    

