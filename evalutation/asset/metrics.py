import pandas as pd
import numpy as np
import scipy.stats

class Metric:
    
    INDEX_VALUES = [
        "equityInitial", "totalTrades", "totalPnl", "winRate",
        "Expectancy", "equityFinal", "equityPeak",
        "amountWin", "amountLoss", "avgWin", "avgLoss",
        "bestTrade", "worstTrade", "profitFactor"
    ]
    
    def __init__(self):
        self.df = pd.DataFrame(index=Metric.INDEX_VALUES)

    @staticmethod
    def calculate_product(r):
        return (1 + r).prod()
    
    @staticmethod
    def average(r):
        return 0 if len(r) == 0 else Metric.calculate_product(r) ** (1 / len(r))

    @staticmethod
    def expectancy(winRate, avgWin, avgLoss):
        return winRate * avgWin + (1 - winRate) * avgLoss

    @staticmethod
    def sharpe_ratio(r):
        mean = Metric.calculate_product(r)
        std = np.std(r)
        return mean / std

    @staticmethod
    def calculate_kurtosis(r, n=8):
        return scipy.stats.kurtosis(r) if len(r) > n else 0

    @staticmethod
    def calculate_skewness(r, n=8):
        return scipy.stats.skew(r) if len(r) > n else 0
        

    def execute(self, trade):
        metrics = {}
        try:
            self.date = str(trade.index[-1])
        except IndexError:
            self.date = None

        closed_trades = trade[trade['status'] == "close"]
        nbTrades = len(closed_trades)
        winTrades = len(closed_trades[closed_trades.pnl > 0])
        lossTrades = len(closed_trades[closed_trades.pnl <= 0])

        winRate = winTrades / nbTrades if nbTrades > 0 else 0
        lossRate = lossTrades / nbTrades if nbTrades > 0 else 0

        gp_not_zero = trade[trade['gp'] != 0]
        avgGp = gp_not_zero["gp"].mean()
        amountWin = gp_not_zero[gp_not_zero['gp'] > 0]["gp"].sum()
        amountLoss = gp_not_zero[gp_not_zero['gp'] <= 0]["gp"].sum()

        avgWin = gp_not_zero[gp_not_zero['gp'] > 0]["gp"].mean()
        avgLoss = gp_not_zero[gp_not_zero['gp'] <= 0]["gp"].mean()

        profitFactor = amountWin / abs(amountLoss)

        totalPnl = trade['gp'].sum()
        expectancy = Metric.expectancy(winRate, avgWin, avgLoss)

        metrics = {
            "totalTrades": nbTrades,
            "totalPnl": totalPnl,
            "winRate": winRate,
            "lossRate": lossRate,
            "Expectancy": expectancy,
            "amountWin": amountWin,
            "amountLoss": amountLoss,
            "avgWin": avgWin,
            "avgLoss": avgLoss,
            "profitFactor": profitFactor,
        }
        return metrics





