import pandas as pd 

from .strategies.rules import Momentum, TMM
#from .strategies.ml import Ml

name = ["MOMENTUM", "TRIPLEMA", "ML1"]

class SignalManager:
    
    def __init__(self, name=""):
        self.name = name
        
        
    def sets(self, data):
        self.rules = {
            "MOMENTUM" : Momentum(data),
            "TRIPLEMA" : TMM(data)
            }
    
    def policy(self):
        return    
    
    def signal_processing(self, data):
        ""
    
    
