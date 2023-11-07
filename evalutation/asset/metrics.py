import pandas as pd
import numpy as np
import scipy.stats



class Metric:
    
    def __init__(self, tradesData):
        self.tradesData = tradesData
        self.nbTrades = 0
        self.winTrades = 0
        self.lossTrades = 0
        
        self.amoungWin = []
        self.amoungLoss = []
        
    
    @staticmethod
    def calculate_product(r):
        return (1 + r).prod()
    
    @staticmethod
    def average(r):
        return 0 if len(r) == 0 else Metric.calculate_product(r) ** (1 / len(r))
    
    @staticmethod
    def calculate_kurtosis(r, n=8):
        return scipy.stats.kurtosis(r) if len(r) > n else 0

    @staticmethod
    def calculate_skewness(r, n=8):
        return scipy.stats.skew(r) if len(r) > n else 0
    
    @staticmethod
    def expectancy(winRate, avgWin, avgLoss):
        return winRate * avgWin + (1 - winRate) * avgLoss
    
    staticmethod
    def sharpe_ratio(r):
        mean = Metric.calculate_product(r)
        std = np.std(r)
        return mean / std
    
    
    def update(self):
        i = j = 0
        while True:
            j += 1
            data = self.tradesData.iloc[i : j+1]
            if self.tradesData.iloc[j]["status"] == "Close":
                i = j+1
                date = self.tradesData.index[j]
                self.nbTrades += 1
                pnl = self.tradesData.iloc[j]["pnl"]
                
                if pnl > 0:
                    self.winTrades += 1
                    self.amoungWin.append(pnl)
                    self.amoungLoss.append(0)
                    
                else:
                    self.lossTrades += 1
                    self.amoungWin.append(0)
                    self.amoungLoss.append(pnl)
                    
                winRate = self.winTrades / self.nbTrades
                avgWin = np.mean(self.amoungWin)
                avgLoss = np.mean(self.amoungLoss)
                expectancy = Metric.expectancy(winRate = winRate , avgWin = avgWin, avgLoss = avgLoss)
                
                profitFactor = np.sum(self.amoungWin) / np.sum(self.amoungLoss)*(-1)
                
                metric = {
                    "date" : date,
                    "nbTrades" : self.nbTrades,
                    "winRate" : winRate,
                    "expectancy" : expectancy,
                    "profitFactor" : profitFactor,
                }
                yield metric
                
                