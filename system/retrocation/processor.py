from typing import Any
from .postprocessing import APostprocessing, PPostprocessing


class Processor:
    
    def __init__(self):
        self.processAsset = APostprocessing()
        self.processPort = PPostprocessing()
    

    def transform(self, tradesData, portfolioData):
        self.processAsset.transform(tradesData)
        self.processPort.transform(portfolioData)
        
    
    
    
