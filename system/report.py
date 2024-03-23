from .viz import Benchmark


class Report:
    
    def __init__(self, db, monitoring):
        self.db = db
        self.tradeData = monitoring.tradeDataAgent
        self.portfolioData = monitoring.portfolioDataAgent
        self.metricData = monitoring.metricDataAgent
        
    
    def processing(self, agentId):
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
    

