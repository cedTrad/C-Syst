

"""
SessionManager fonctionne avec following
"""
class SessionManager:
    
    def __init__(self, following):
        self.following = following
        self.max_step = 50
        self.step = 50
        
    
    def update_step(self, n = 50):
        self.step = n
        
        
    def report(self):
        self.following.get_report()
        
        
    def update_risk_session_params(self):
        return
    
    
    def actuator(self):
        if self.step == 0:
            print("********* End Session *************")
            self.report()
            self.update_risk_session_params()
            self.update_step()
            
        if self.step == self.max_step :
            print("********** Start Session **********")
            #print(f"****** step : {self.step}")
            
        self.step = self.step - 1