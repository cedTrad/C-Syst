import numpy as np
from plot import *
import plotly.figure_factory as ff


class VizBenchmark:
    
    def __init__(self, agentId, trades : dict, portfolios : dict):
        self.agentId = agentId
        self.trades = trades
        self.portfolios = portfolios
    
    
    def preprocess(self):
        portfolioData = self.portfolios[self.agentId].copy()
        capital = portfolioData["capital"].iloc[0]
        
        tradesData = self.trades[self.agentId].copy()
        tradesData["cum_gp"] = tradesData["cum_gp"] + capital
        tradesData["benchmark"] = tradesData["price_cum"] * capital
        tradesData["value_re"] = tradesData["value"] + tradesData["out_value"]
        
        return tradesData, portfolioData
        
    
    def per_trade(self, symbol : str):
        tradesData, _ = self.preprocess()
        
        fig = create_figure()
        add_line(fig, tradesData, feature="benchmark", name="market")
        add_line(fig, tradesData, feature="cum_gp", name=symbol)
        
        fig.update_layout(height = 400 , width = 1000,
                          legend = dict(orientation="h",
                                        yanchor="bottom", y=1,
                                        xanchor="right", x=0.5),
                          margin = {'t':0, 'b':0, 'l':10, 'r':0}
                          )
        return fig
    
    
    def values(self, symbol : str):
        tradesData, portfolioData = self.preprocess()
        
        fig = subplot(nb_cols = 1, nb_rows = 2)
        add_bar(fig, tradesData, feature="value_re", name=symbol, col=1, row=1)
        add_line(fig, data=portfolioData, feature="capital", name="portfolio", col=1, row=2)
        add_bar(fig, data=portfolioData, feature="risk_value", name="risk", col=1, row=2)
        add_bar(fig, data=portfolioData, feature="available_value", name="available", col=1, row=2)
        fig.update_layout(height = 600 , width = 1000,
                          legend = dict(orientation="h",
                                        yanchor="bottom", y=1,
                                        xanchor="right", x=0.5),
                          margin = {'t':0, 'b':0, 'l':10, 'r':0}
                          )
        return fig
    
    
        
        

class VizAsset:
    
    def __init__(self, agentId, trades : dict):
        self.agentId = agentId
        self.trades = trades
    
    def preprocess(self):
        return self.trades[self.agentId]
        
    def get_points(self, trades):
        loc = np.where(trades['status'] == 'Open')
        entryPoints = trades.iloc[loc][['side', 'status', 'price', 'pnl']]
        
        loc = np.where(trades['status'] == 'Close')
        exitPoints = trades.iloc[loc][['side', 'status', 'price', 'pnl']]
        
        return entryPoints, exitPoints
    
    
    def candle(self, data):
        tradesData = self.preprocess()
        entryPoints, exitPoints = self.get_points(tradesData)
        
        start = tradesData.index[0]
        end = tradesData.index[-1]
        data = data.loc[start : end]
        
        fig = subplots(nb_rows=3, nb_cols=1, row_heights=[0.0, 0.7, 0.3])
        
        add_second_y(fig=fig, col=1, row=2, data=tradesData, name='position')
        plot_candle(fig=fig, col=1, row=2, data=data, symbol='ohlc')
        signal_point(fig, col=1, row=2, x = entryPoints.index, y = entryPoints.price, name='in', marker=(5, 10, 'blue'))
        signal_point(fig, col=1, row=2, x = exitPoints.index, y = exitPoints.price, name='out', marker=(6, 10, 'black'))
        color_trades(fig=fig, col=1, row=2, entry=entryPoints, exit=exitPoints, opacity=0.1)
        
        add_bar(fig=fig, col=1, row=3, data=tradesData, feature='pnl', name='pnl')
        add_second_y(fig=fig, col=1, row=3, data=tradesData, name='pnl_pct')
        
        fig.update_layout(height = 800 , width = 1000,
                          legend = dict(orientation="h",
                                        yanchor="bottom", y=1,
                                        xanchor="right", x=0.5),
                          margin = {'t':0, 'b':0, 'l':10, 'r':0}
                          )
        return fig



          
class VizRisk:
    
    def __init__(self):
        self.p = 0



class CompareViz:
    
    def __init__(self, agentIds, trades : dict, portfolios : dict):
        self.agentIds = agentIds
        self.trades = trades
        self.portfolios = portfolios
    

    def preprocess(self):
        
        self.tradesRs = {}
        self.tradesS = {}
        
        for agentId in self.agentIds:
            tradesR = self.trades[agentId].copy()
            self.tradesRs[agentId] = tradesR[tradesR["status"] == "Close"]
            
            capital = self.portfolios[agentId]["capital"].iloc[0]
            
            trades = self.trades[agentId].copy()
            trades["cum_gp"] = trades["cum_gp"] + capital
            trades["benchmark"] = trades["price_cum"] * capital
            self.tradesS[agentId] = trades
            
            
    def equity(self):
        self.preprocess()
        
        fig = create_figure()
        for agentId in self.agentIds:
            trade = self.tradesS[agentId]
            symbol = trade["symbol"].iloc[0]
            
            add_line(fig, trade, feature="benchmark", name=f"market_{agentId} {symbol}")
            add_line(fig, trade, feature="cum_gp", name=f"{symbol}_{agentId}")
        
        fig.update_layout(height = 400 , width = 1000,
                          margin = {'t':0, 'b':0, 'l': 0, 'r':10}
                          )
        return fig
        
        
    def pnl(self):
        
        hist_data = []
        group_labels = self.agentIds
        for agentId in self.agentIds:
            data = self.tradesRs[agentId]["pnl"]
            hist_data.append(data)

        # Create distplot with custom bin_size
        fig = ff.create_distplot(hist_data, group_labels, bin_size=.2)
        
        fig.update_layout(height = 400 , width = 1000,
                          margin = {'t':0, 'b':0, 'l': 0, 'r':10}
                          )
        
        return fig
  
  
            

class VizPortfolio:
    
    def __init__(self, agentId, portfolios : dict):
        self.agentId = agentId
        self.portfolios = portfolios
            
    def preprocess(self):
        portfolioData = self.portfolios[self.agentId]
        return portfolioData
    
    def show(self):
        portfolioData = self.preprocess()
        
        fig = create_figure()
        
        add_line(fig, data=portfolioData, feature="capital", name="capital")
        add_bar(fig, data=portfolioData, feature="risk_value", name = "risk")
        add_bar(fig, data=portfolioData, feature="available_value", name = "available")
        
        fig.update_layout(height = 500 , width = 1000,
                          legend = dict(orientation="h",
                                        yanchor="bottom", y=1,
                                        xanchor="right", x=0.5),
                          margin = {'t':0, 'b':0, 'l':10, 'r':0}
                          )
        return fig 
    
   
      
      
        

class VizPnl:
    
    def __init__(self, agentId, trades : dict):
        self.agentId = agentId
        self.trades = trades
    
    def preprocess(self, mode = "per_step"):
        self.trades_long_per_step = self.trades[self.agentId]["long"]
        self.trades_long_per_step = self.trades_long_per_step.loc[self.trades_long_per_step["agentId"] == self.agentId]
        
        self.trades_short_per_step = self.trades[self.agentId]["short"]
        self.trades_short_per_step = self.trades_short_per_step.loc[self.trades_short_per_step["agentId"] == self.agentId]
        
        self.trades_long_per_trade = self.trades[self.agentId]["long"][self.trades[self.agentId]["long"]["status"] == "Close"]
        self.trades_long_per_trade = self.trades_long_per_trade.loc[self.trades_long_per_trade["agentId"] == self.agentId]
        
        self.trades_short_per_trade = self.trades[self.agentId]["short"][self.trades[self.agentId]["short"]["status"] == "Close"]
        self.trades_short_per_trade = self.trades_short_per_trade.loc[self.trades_short_per_trade["agentId"] == self.agentId]
    
    
    def long_short_per_step(self):
        self.preprocess()
        fig = subplot(nb_cols=2, nb_rows=1)
        
        trades_long = self.trades_long_per_step.copy()
        trades_short = self.trades_short_per_step.copy()
        
        add_hist(fig, trades_long, feature="rets", name="long", col=1, row=1)
        add_hist(fig, trades_short, feature="rets", name="short", col=1, row=1)
        add_vline(fig, x=0, color="black", col=1, row=1)
        
        add_hist(fig, trades_long, feature="gp", name="long-gp", col=2, row=1)
        add_hist(fig, trades_short, feature="gp", name="short-gp", col=2, row=1)
        add_vline(fig, x=0, color="black", col=2, row=1)
        
        fig.update_layout(height = 400 , width = 1000,
                          legend = dict(orientation="h",
                                        yanchor="bottom", y=1,
                                        xanchor="right", x=0.5),
                          margin = {'t':0, 'b':0, 'l':10, 'r':0}
                          )
        return fig
    
    
    def long_short_per_trade(self):
        
        self.preprocess()
        
        fig = subplot(nb_cols=2, nb_rows=1)
        
        trades_long = self.trades_long_per_trade.copy()
        trades_short = self.trades_short_per_trade.copy()
        
        add_hist(fig, trades_long, feature="pnl", name="long", col=1, row=1)
        add_hist(fig, trades_short, feature="pnl", name="short", col=1, row=1)
        add_vline(fig, x=0, color="black", col=1, row=1)
        
        add_hist(fig, trades_long, feature="pnl_pct", name="long-gp", col=2, row=1)
        add_hist(fig, trades_short, feature="pnl_pct", name="short-gp", col=2, row=1)
        add_vline(fig, x=0, color="black", col=2, row=1)
        
        fig.update_layout(height = 400 , width = 1000,
                          legend = dict(orientation="h",
                                        yanchor="bottom", y=1,
                                        xanchor="right", x=0.5),
                          margin = {'t':0, 'b':0, 'l':10, 'r':0}
                          )
        return fig

