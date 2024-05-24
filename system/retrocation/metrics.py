import pandas as pd
import numpy as np
import ast
import scipy.stats

from dataclasses import dataclass, field
from typing import List


@dataclass
class WTO:
    nb: List[int] = field(default_factory=list)
    amount: List[float] = field(default_factory=list)
    rets : List[float] = field(default_factory=list)
    mkt_rets : List[float] = field(default_factory=list)
    exposure : List[float] = field(default_factory=list)
    
    def nbtrades(self):
        return len(self.nb)
    
    def winrate(self):
        return sum([x for x in self.nb if x > 0])/len(self.nb)
    
    def lossrate(self):
        return sum([x for x in self.nb if x <= 0])/len(self.nb)
    
    def total_amount(self):
        return sum(self.amount)
        
    def totalwin(self):
        return sum([x for x in self.amount if x > 0])
    
    def totalloss(self):
        return sum([x for x in self.amount if x <= 0])
    
    def avgwin(self):
        return np.mean([x for x in self.amount if x > 0])
    
    def avgloss(self):
        return np.mean([x for x in self.amount if x <= 0])
    
    def distribution(self):
        r = 4
        avg, std = np.mean(self.rets), np.std(self.rets)
        q1, median, q3 = np.percentile(self.rets, 0.25), np.percentile(self.rets, 0.5), np.percentile(self.rets, 0.75)
        return [round(x*100, r) for x in [q1, avg, median, q3]]
    
    def expectancy(self):
        return self.winrate() * self.avgwin() - self.lossrate() * self.avgloss()
    
    def profitfactor(self):
        return self.totalwin() / self.totalloss() * (-1)
    
    def minexp(self):
        return min(self.exposure)
    
    def maxexp(self):
        return max(self.exposure)


class AMetric:
    
    def __init__(self):
        self.nb_trades = 0
        self.len_trade = 0
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
    
    def exposition(self):
        return
    
    def actuator(self, tradeData):
        self.date = tradeData.iloc[-1]["date"]
        
        pnl = tradeData.iloc[-1]["pnl"]
        
        pnl_pct = tradeData.iloc[-1]["pnl_pct"]
        mkt_pct = tradeData.iloc[-1]["ret_price"]
        
        self.cum_gp = tradeData.iloc[-1]["cum_gp"]
        status = tradeData.iloc[-1]["status"]
        current_position = tradeData.iloc[-1]["position"]
        
        position = tradeData["state"].apply(lambda x : ast.literal_eval(x)[1]).iloc[-1]
        if position in ["LONG", "SHORT"]:
            self.wto.mkt_rets.append(mkt_pct)
        
        if status == "Open":
            self.nb_trades += 1
            self.len_trade += 1
            
        elif status == "Close":
            self.len_trade += 1
            self.wto.exposure.append(self.len_trade)
            self.len_trade = 0
            
            self.wto.nb.append(1) if pnl > 0 else self.wto.nb.append(-1)
            
            self.wto.amount.append(pnl)
            self.wto.rets.append(pnl_pct)
            
    
    def calculate(self):
        nbTrades = self.wto.nbtrades()
        winRate = self.wto.winrate()
        lossRate = self.wto.lossrate()
        amountWin = self.wto.totalwin()
        amountLoss = self.wto.totalloss()
        totalAmount = self.wto.total_amount()
        expectancy = self.wto.expectancy()
        profitFactor = self.wto.profitfactor()
        minExposure = self.wto.minexp()
        maxExposure = self.wto.maxexp()
        distribution = self.wto.distribution()
        result = {
            "date" : self.date,
            "nbTrades" : nbTrades,
            "winRate": winRate,
            "lossRate": lossRate,
            "amountWin": amountWin,
            "amountLoss": amountLoss,
            "totalAmount" : totalAmount,
            "amount" : self.cum_gp,
            "expectancy": expectancy,
            "profitFactor": profitFactor,
            "minExposure" : minExposure,
            "maxExposure" : maxExposure,
            "q1 avg median q3 %" : distribution
        }
        
        return result
    
    def reset(self):
        self.wto = WTO()

    
