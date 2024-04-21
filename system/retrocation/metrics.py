import pandas as pd
import numpy as np
import scipy.stats

from dataclasses import dataclass, field
from typing import List


@dataclass
class WTO:
    nb: List[int] = field(default_factory=list)
    amount: List[float] = field(default_factory=list)
    
    def nbtrades(self):
        return len(self.nb)
    
    def winrate(self):
        return sum([x for x in self.nb if x > 0])/len(self.nb)
    
    def lossrate(self):
        return sum([x for x in self.nb if x <= 0])/len(self.nb)
    
    def totalwin(self):
        return sum([x for x in self.amount if x > 0])
    
    def totalloss(self):
        return sum([x for x in self.amount if x <= 0])
    
    def avgwin(self):
        return np.mean([x for x in self.amount if x > 0])
    
    def avgloss(self):
        return np.mean([x for x in self.amount if x <= 0])
    
    def expectancy(self):
        return self.winrate() * self.avgwin() + self.lossrate() * self.avgloss()
    
    def profitfactor(self):
        return self.totalwin() / self.totalloss() * (-1)


class AMetric:
    
    def __init__(self):
        self.nb_trades = 0
        self.wto = WTO()
        
    
    @staticmethod
    def calculate_product(r):
        return (1 + r).prod()
    
    @staticmethod
    def average(r):
        return 0 if len(r) == 0 else AMetric.calculate_product(r) ** (1 / len(r))
    
    @staticmethod
    def calculate_kurtosis(r, n=8):
        return scipy.stats.kurtosis(r) if len(r) > n else 0

    @staticmethod
    def calculate_skewness(r, n=8):
        return scipy.stats.skew(r) if len(r) > n else 0
    
    staticmethod
    def sharpe_ratio(r):
        mean = AMetric.calculate_product(r)
        std = np.std(r)
        return mean / std
    
    
    def actuator(self, tradeData):
        pnl = tradeData.iloc[-1]["pnl"]
        status = tradeData.iloc[-1]["status"]
        
        if status == "Open":
            self.nb_trades += 1
            
        elif status == "Close":
            if pnl > 0:
                self.wto.nb.append(1)
                self.wto.amount.append(pnl)
            else:
                self.wto.nb.append(-1)
                self.wto.amount.append(pnl)
            
    
    def calculate(self):
        nbTrades = self.wto.nbtrades()
        winRate = self.wto.winrate()
        lossRate = self.wto.lossrate()
        amountWin = self.wto.totalwin()
        amountLoss = self.wto.totalloss()
        expectancy = self.wto.expectancy()
        profitFactor = self.wto.profitfactor()
        
        result = {
            "nbTrades" : nbTrades,
            "winRate": winRate,
            "lossRate": lossRate,
            "amountWin": amountWin,
            "amountLoss": amountLoss,
            "expectancy": expectancy,
            "profitFactor": profitFactor
        }
        
        return result
    
    def reset(self):
        self.wto = WTO()

    
