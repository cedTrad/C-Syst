import numpy as np
from plot import *
import plotly.figure_factory as ff


class VizBenchmark:
    
    def __init__(self, agentId, trades, portfolio_data = ""):
        self.agentId = agentId
        self.trades = trades.copy()
        self.portfolio_data = portfolio_data.copy()
        self.portfolio_data.set_index("date", inplace = True)
    
    def preprocess(self):
        capital = self.portfolio_data["capital"].iloc[0]
        self.trades = self.trades.loc[self.trades["agentId"] == self.agentId].copy()
        self.trades["cum_gp"] = self.trades["cum_gp"] + capital
        self.trades["benchmark"] = self.trades["price_cum"] * capital
        
        self.trades["value_re"] = self.trades["value"] + self.trades["out_value"]
        self.portfolio_data = self.portfolio_data.loc[self.portfolio_data["agentId"] == self.agentId]
        
    
    def per_trade(self, symbol):
        
        self.preprocess()
        
        trade = self.trades.copy()
        
        fig = create_figure()
        add_line(fig, trade, feature="benchmark", name="market")
        add_line(fig, trade, feature="cum_gp", name=symbol)
        
        fig.update_layout(height = 400 , width = 1000,
                          legend = dict(orientation="h",
                                        yanchor="bottom", y=1,
                                        xanchor="right", x=0.5),
                          margin = {'t':0, 'b':0, 'l':10, 'r':0}
                          )
        return fig
    
    def values(self, symbol):
        
        self.preprocess()
        
        fig = subplot(nb_cols = 1, nb_rows = 2)
        
        trade = self.trades.copy()
        portfolio_data = self.portfolio_data.copy()
        
        
        add_bar(fig, trade, feature="value_re", name=symbol, col=1, row=1)
        
        add_line(fig, data=portfolio_data, feature="capital", name="portfolio", col=1, row=2)
        add_bar(fig, data=portfolio_data, feature="risk_value", name="risk", col=1, row=2)
        add_bar(fig, data=portfolio_data, feature="available_value", name="available", col=1, row=2)
        fig.update_layout(height = 600 , width = 1200,
                          legend = dict(orientation="h",
                                        yanchor="bottom", y=1,
                                        xanchor="right", x=0.5),
                          margin = {'t':0, 'b':0, 'l':10, 'r':0}
                          )
        return fig
    
    
    def all(self):
        ""
        
        

class VizAsset:
    
    
    def __init__(self, agentId, trades):
        self.agentId = agentId
        self.trades = trades.copy()
    
    def preprocess(self):
        self.trades = self.trades.loc[self.trades["agentId"] == self.agentId].copy()
        
    
    def get_points(self, trades):
        loc = np.where(trades['status'] == 'Open')
        entry_points = trades.iloc[loc][['side', 'status', 'price', 'pnl']]
        
        loc = np.where(trades['status'] == 'Close')
        exit_points = trades.iloc[loc][['side', 'status', 'price', 'pnl']]
        
        return entry_points, exit_points
    
    
    def candle(self, data):
        self.preprocess()
        
        trades = self.trades.copy()
        
        entry_points, exit_points = self.get_points(trades)
        start = trades.index[0]
        end = trades.index[-1]
        
        data = data.loc[start : end]
        
        fig = subplots(nb_rows=3, nb_cols=1, row_heights=[0.0, 0.7, 0.3])
        
        add_second_y(fig=fig, col=1, row=2, data=trades, name='position')
        plot_candle(fig=fig, col=1, row=2, data=data, symbol='ohlc')
        signal_point(fig, col=1, row=2, x = entry_points.index, y = entry_points.price, name='in', marker=(5, 10, 'blue'))
        signal_point(fig, col=1, row=2, x = exit_points.index, y = exit_points.price, name='out', marker=(6, 10, 'black'))
        color_trades(fig=fig, col=1, row=2, entry=entry_points, exit=exit_points, opacity=0.1)
        
        add_bar(fig=fig, col=1, row=3, data=trades, feature='pnl', name='pnl')
        add_second_y(fig=fig, col=1, row=3, data=trades, name='pnl_pct')
        
        fig.update_layout(height = 800 , width = 1200,
                          legend = dict(orientation="h",
                                        yanchor="bottom", y=1,
                                        xanchor="right", x=0.5),
                          margin = {'t':0, 'b':0, 'l':10, 'r':0}
                          )
        return fig




class VizPortfolio:
    
    def __init__(self, agentId, portfolio_data):
        self.agentId = agentId
        self.portfolio_data = portfolio_data.copy()
    
    def preprocess(self):
        self.portfolio_data.set_index("date", inplace = True)
        self.portfolio_data = self.portfolio_data.loc[self.portfolio_data["agentId"] == self.agentId].copy()
    
    def show(self):
        self.preprocess()
        
        portfolio_data = self.portfolio_data
        
        fig = create_figure()
        
        add_line(fig, data=portfolio_data, feature="capital", name="capital")
        add_bar(fig, data=portfolio_data, feature="risk_value", name = "risk")
        add_bar(fig, data=portfolio_data, feature="available_value", name = "available")
        
        fig.update_layout(height = 500 , width = 1000,
                          legend = dict(orientation="h",
                                        yanchor="bottom", y=1,
                                        xanchor="right", x=0.5),
                          margin = {'t':0, 'b':0, 'l':10, 'r':0}
                          )
        return fig 
    

        

class VizPnl:
    
    def __init__(self, agentId, trades_data):
        self.agentId = agentId
        self.data = trades_data
    
    def preprocess(self, symbol, mode = "per_step"):
        self.data_long_per_step = self.data[symbol]["long"]
        self.data_long_per_step = self.data_long_per_step.loc[self.data_long_per_step["agentId"] == self.agentId]
        
        self.data_short_per_step = self.data[symbol]["short"]
        self.data_short_per_step = self.data_short_per_step.loc[self.data_short_per_step["agentId"] == self.agentId]
        
        self.data_long_per_trade = self.data[symbol]["long"][self.data[symbol]["long"]["status"] == "Close"]
        self.data_long_per_trade = self.data_long_per_trade.loc[self.data_long_per_trade["agentId"] == self.agentId]
        
        self.data_short_per_trade = self.data[symbol]["short"][self.data[symbol]["short"]["status"] == "Close"]
        self.data_short_per_trade = self.data_short_per_trade.loc[self.data_short_per_trade["agentId"] == self.agentId]
    
    
    def long_short_per_step(self, symbol):
        self.preprocess(symbol)
        fig = subplot(nb_cols=2, nb_rows=1)
        
        data_long = self.data_long_per_step.copy()
        data_short = self.data_short_per_step.copy()
        
        add_hist(fig, data_long, feature="rets", name="long", col=1, row=1)
        add_hist(fig, data_short, feature="rets", name="short", col=1, row=1)
        add_vline(fig, x=0, color="black", col=1, row=1)
        
        add_hist(fig, data_long, feature="gp", name="long-gp", col=2, row=1)
        add_hist(fig, data_short, feature="gp", name="short-gp", col=2, row=1)
        add_vline(fig, x=0, color="black", col=2, row=1)
        
        fig.update_layout(height = 400 , width = 1000,
                          legend = dict(orientation="h",
                                        yanchor="bottom", y=1,
                                        xanchor="right", x=0.5),
                          margin = {'t':0, 'b':0, 'l':10, 'r':0}
                          )
        return fig
    
    def long_short_per_trade(self, symbol):
        
        self.preprocess(symbol)
        
        fig = subplot(nb_cols=2, nb_rows=1)
        
        data_long = self.data_long_per_trade.copy()
        data_short = self.data_short_per_trade.copy()
        
        add_hist(fig, data_long, feature="pnl", name="long", col=1, row=1)
        add_hist(fig, data_short, feature="pnl", name="short", col=1, row=1)
        add_vline(fig, x=0, color="black", col=1, row=1)
        
        add_hist(fig, data_long, feature="pnl_pct", name="long-gp", col=2, row=1)
        add_hist(fig, data_short, feature="pnl_pct", name="short-gp", col=2, row=1)
        add_vline(fig, x=0, color="black", col=2, row=1)
        
        fig.update_layout(height = 400 , width = 1000,
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
    
    def __init__(self, agentIds, trades, portfolio_data):
        self.agentIds = agentIds
        self.trades = trades
        self.portfolio_data = portfolio_data
    

    def preprocess(self, symbol, side="all"):
        
        self.tradesR = self.trades[symbol][side][self.trades[symbol][side]["status"] == "Close"]
        self.tradesRs = []
        self.tradesS = []
        
        for agentId in self.agentIds:    
            self.tradesRs[agentId] = self.tradesR[self.tradesR["agentId"] == agentId]
            
            self.portfolio_data[self.portfolio_data["agentId"] == agentId]
            
            data = self.trades.loc[self.trades["agentId"] == agentId].copy()
            data["cum_gp"] = data["cum_gp"] + self.capital
            data["benchmark"] = data["price_cum"] * self.capital
            data["value_re"] = data["value"] + data["out_value"]
            
            self.tradesS[agentId] = data
            
            
    def equity(self, symbol):
        self.preprocess(symbol)
        
        fig = create_figure()
        for agentId in self.agentIds:
            trade = self.tradesS[agentId]
            
            add_line(fig, trade, feature="benchmark", name=f"market_{agentId} {symbol}")
            add_line(fig, trade, feature="cum_gp", name=f"{symbol}_{agentId}")
        
        fig.update_layout(height = 400 , width = 1000,
                          legend = dict(orientation="h",
                                        yanchor="bottom", y=1,
                                        xanchor="right", x=0.5),
                          margin = {'t':0, 'b':0, 'l':10, 'r':0}
                          )
        return fig
        
        
    def pnl(self):
        
        hist_data = []
        group_labels = self.agentIds.copy()
        for agentId in self.agentIds:
            data = self.tradesRs[agentId]["pnl"]
            hist_data.append(data)

        # Create distplot with custom bin_size
        fig = ff.create_distplot(hist_data, group_labels, bin_size=.2)
        
        return fig
            
    
        