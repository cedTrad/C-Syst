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
        self.session_id = 0
        self.metrics = AMetric()        
        self.rets_dist = {}


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
            
            self.rets_dist[self.session_id] = {"trade" : self.metrics.wto.rets, "market" : self.metrics.wto.mkt_rets}
            
            self.update_step()
            self.metrics.reset()
            print(f"__ End Session {self.session_id} ____________")
            return True, self.session_id
            
        if self.step == self.max_step :
            self.session_id += 1
            
            print(f"__ Start Session {self.session_id}____________")
        
            
        self.step -= 1
        return False, self.session_id
    
