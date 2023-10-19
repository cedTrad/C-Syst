import pandas as pd
import numpy as np

import scipy.stats
from scipy.stats import norm



class Metric:
    
    def __init__(self):
        self.df = pd.DataFrame(index = ["Equity Initial", "Total Trades", "Total Pnl", "Win Rate",
                                        "Expentancy", "Equity Final", "Equity Peak",
                                        "Amoung Win", "Amoung Loss", "Avg Win", "Avg Loss",
                                        "Best Trade", "Worse Trade", "Profit Factor"]
                               )
    
    def pnl(self, r):
        x = (1 + r).prod()
        return x    
    
    def average(self, r):
        if len(r) == 0:
            return 0
        else:
            x = (1+r).prod()
            return x**(1/len(r))
    
    def expectancy(self, win_rate, avg_win, avg_loss):
        return win_rate*avg_win + (1 - win_rate)*avg_loss    
    
    def sharpe_ratio(self):
        mean = (1+r).prod()
        std = np.std(r)
        return mean / std
    
    
    def kurtosis(self, r, n = 8):
        if len(r) > n:
            return scipy.stats.kurtosis(r)
        else:
            return 0

    def skewness(self, r, n = 8):
        if len(r) > n:
            return scipy.stats.skew(r)
        else:
            return 0
    
    
    def excecute(self, trade):
        metrics = {}
        try:
            self.date = str(trade.index[-1])
        except IndexError:
            self.date = None
        
        loc = np.where((trade['status'] == "close"))
        n_trades = len(loc[0])
        loc = np.where((trade['status'] == "close") & (trade.pnl > 0))
        win_trades = len(loc[0])
        loc = np.where((trade['status'] == "close") & (trade.pnl <= 0))
        loss_trades = len(loc[0])
        
        try:
            win_rate = win_trades / n_trades
        except ZeroDivisionError:
            win_rate = 0
        try:
            loss_rate = loss_trades / n_trades
        except ZeroDivisionError:
            loss_rate = 0
        
        loc = np.where(trade['gp'] != 0)
        avg_gp = trade.iloc[loc]["gp"].mean()
        amoung_win = trade.loc[trade['gp'] > 0, "gp"].sum()
        amoung_loss = trade.loc[trade['gp'] <= 0, "gp"].sum()
        
        trade_ = trade.iloc[loc]
        avg_win = trade_.loc[trade_['gp'] > 0, "gp" ].mean()
        avg_loss = trade_.loc[trade_['gp'] <= 0, "gp" ].mean()
        profit_factor = amoung_win / abs(amoung_loss)
        
        total_pnl = trade.gp.sum()
        exp = self.expectancy(win_rate = win_rate,
                                   avg_win = avg_win,
                                   avg_loss = avg_loss)
        
        keys = ["Total Trades", "Total Pnl", "Win Rate", "Expentancy",
                "Amoung Win", "Amoung Loss", "Avg Win", "Avg Loss", "Profit Factor"]
        
        values = [n_trades, total_pnl, win_rate, exp, 
                  amoung_win, amoung_loss, avg_win, avg_loss,
                  profit_factor]
        
        for key, value in zip(keys, values):
            metrics[key] = value
        
        return metrics
        
        
        
