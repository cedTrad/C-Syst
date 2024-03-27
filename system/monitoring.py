from .retrocation.processor import Processor

class Monitoring:
    
    def __init__(self, capital):
        self.processor = Processor(capital)
        
        
    
    def transform_trade_data(self, agentId, journal):
        self.tradesData = journal.tradesData.copy()
        self.portfoliosData = journal.portfolioData.copy()
        metricsData = journal.metricsData.copy()
        
        tradeDataAgents, portfoliosDataAgents = self.processor.transform(self.tradesData, self.portfoliosData)
        metricDataAgent = metricsData.copy()
        
        tradeDataAgent = tradeDataAgents[agentId]
        portfolioDataAgent = portfoliosDataAgents[agentId]
        
        return tradeDataAgent, portfolioDataAgent, metricDataAgent
    
    
    def update_metric(self, agentId, journal):
        self.tradeDataAgent, self.portfolioDataAgent, self.metricDataAgent = self.transform_trade_data(agentId, journal)
        metrics = self.processor.update_metric(self.tradeDataAgent)
        
        return metrics
        
        
    