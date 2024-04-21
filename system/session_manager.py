from .retrocation.metrics import AMetric

"""
SessionManager fonctionne avec following
"""
class SessionManager:
    
    def __init__(self, following):
        self.following = following
        self.max_step = 50
        self.step = 50
        self.n_session = 0
        self.metrics = AMetric()
    
    def update_step(self, n = 50):
        self.step = n
        
    def get_session_metrics(self):
        return self.metrics.calculate()
        
    def report(self):
        agent = self.following.agent_data
        trade_data = agent.trade_data
        portfolio_data = agent.portfolio_data
        #display(portfolio_data.iloc[-1][["date", "capital", "cum_rets", "drawdown"]])
        
    def update_risk_session_params(self):
        return
    
    
    def actuator(self):
        if self.step == 0:
            self.report()
            m = self.get_session_metrics()
            print(m)
            self.update_risk_session_params()
            self.update_step()
            self.metrics.reset()
            print(f"__ End Session {self.n_session} ____________")
            return True, self.n_session
            
        if self.step == self.max_step :
            self.n_session += 1
            print(f"__ Start Session {self.n_session}____________")
        
            
        self.step -= 1
        return False, self.n_session
    