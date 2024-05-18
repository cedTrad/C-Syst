import pandas as pd 

from .strategies.rules import Momentum, Momentum2, TMM
#from .strategies.ml import Ml

name = ["MOMENTUM", "TRIPLEMA", "ML1"]

class Signal:
    
    def __init__(self, name=""):
        self.name = name
        
        
    def sets(self, data):
        self.rules = {
            "MOMENTUM" : Momentum2(data),
            "TRIPLEMA" : TMM(data)
            }
    
    
    def processing(self):
        return
    
