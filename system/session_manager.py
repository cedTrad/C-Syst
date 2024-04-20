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
    
    
    def actuator(self, tradedata):
        self.metrics.actuator(tradeData=tradedata)
        if self.step == 0:
            print("__ End Session ____________")
            self.report()
            m = self.get_session_metrics()
            print(m)
            self.update_risk_session_params()
            self.update_step()
            
        if self.step == self.max_step :
            print("__ Start Session ____________")
            self.n_session += 1
            #print(f"****** step : {self.step}")
            
        self.step -= 1
        print(f"session {self.n_session} step : {self.step}")
