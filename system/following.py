from .report import Report
from .retrocation.processor import Processor
from .viz import Benchmark



class AgentData:
    def __init__(self, agent_id, trade_data, portfolio_data, metric_data):
        self.agent_id = agent_id
        self.trade_data = trade_data
        self.portfolio_data = portfolio_data
        self.metric_data = metric_data


class Following:
    
    def __init__(self, db, post_event):
        self.db = db
        self.processor = Processor()
        self.tradeData = post_event.tradeData
        self.portfolioData = post_event.portfolioData
        self.metricData = post_event.metricData
        
    def update_metrics(self):
        ""
    
    def process_agent_data(self, agentId):
        """
        Traite les données associées à un agent de trading donné.
        
        Args:
            agent_id (tuple): Identifiant de l'agent de trading.
        
        Returns:
            dict: Données traitées de l'agent.
        """
        self.processor.transform(self.tradeData, self.portfolioData)
        self.agent_data = AgentData(agentId, self.tradeData, self.portfolioData, self.metricData)
        
    
    def show(self):
        f_var = ["pnl", "pnl_pct", "value"]
        p_var = ["capital", "risk_value"]
        print(self.tradeData.iloc[-1][f_var])
        print(self.portfolioData.iloc[-1][p_var])
    
    
    def execute(self, agentId):
        self.process_agent_data(agentId)
        self.show()
    
    
    def plot_equity(self):
        tradeDataAgent = self.agent_data.trade_data
        portfolioDataAgent = self.agent_data.portfolio_data
        data = self.db.get_data(self.agent_data.agent_id[1])
    
        benchmark = Benchmark(tradeDataAgent, portfolioDataAgent)
        
        fig_equity = benchmark.equity()
        fig_equity.show()
        
        fig_asset = benchmark.asset(data)
        fig_asset.show()
    
    
    def get_report(self):
        ""

