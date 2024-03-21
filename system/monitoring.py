from .retrocation.processor import Processor

class Monitoring:
    
    def __init__(self):
        self.processor = Processor()
        
    
    def transform_trade_data(self, agentId, journal):
        tradesData = journal.tradesData
        portfoliosData = journal.portfolioData
        metricsData = journal.metricsData
        
        tradeDataAgents, portfoliosDataAgents = self.processor.transform(tradesData, portfoliosData)
        
        tradeDataAgent = tradeDataAgents[agentId]
        portfoliosDataAgent = portfoliosDataAgents[agentId]
        
        return tradeDataAgent, portfoliosDataAgent
    
    
    def update_metric(self, agentId, journal):
        self.tradeDataAgent, self.portfoliosDataAgent = self.transform_trade_data(agentId, journal)
        metrics = self.processor.update_metric(self.tradeDataAgent)
        return metrics
        
        
    