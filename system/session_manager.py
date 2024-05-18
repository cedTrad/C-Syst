from .retrocation.metrics import AMetric

"""
SessionManager fonctionne avec following
"""
class SessionManager:
    
    def __init__(self, env, following, max_step):
        self.following = following
        self.post_event = env.post_event
        self.max_step = max_step
        self.step = 50
        self.n_session = 0
        self.metrics = AMetric()
    
    def update_step(self):
        self.step = self.max_step
        
    def get_session_metrics(self):
        return self.metrics.calculate()
        
        
    def update_risk_session_params(self):
        return
    
    
    def actuator(self):
        if self.step == 0:
            session_metric = self.get_session_metrics()
            self.post_event.add_session(session_metric)
            
            print(session_metric)
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
    