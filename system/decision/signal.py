import pandas as pd 

from .strategies.rules import Momentum, TMM
#from .strategies.ml import Ml


class Signal:
    
    def __init__(self):
        self.op = 0
        
    def sets(self, data):
        self.st_mom = Momentum(data)
        self.st_tmm = TMM(data)
        #self.st_ml = Ml(data)
        self.params()
        
    
    def params(self):
        params = 3
        self.st_mom.update_params(params)
        params = (3, 8, 14)
        self.st_tmm.update_params(params)
    
    
    def get_points(self, bar = -1):
        s1 = self.st_mom.run(bar)
        s2 = self.st_tmm.run(bar)
        
        return s2
    

