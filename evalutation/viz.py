import numpy as np
from plot import *


class VizBenchmark:
    
    def __init__(self, trades, portfolio_data = ""):
        self.trades = trades.copy()
        self.portfolio_data = portfolio_data.copy()
        self.portfolio_data.set_index("date", inplace = True)
    
    def per_trade(self, symbol):
        
        trade = self.trades[symbol]["all"].copy()
        trade["cum_gp"] = trade["cum_gp"] + self.portfolio_data["capital"].iloc[0]
        trade["benchmark"] = trade["price_cum"] * self.portfolio_data["capital"].iloc[0]
        
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
        fig = subplot(nb_cols = 1, nb_rows = 2)
        
        trade = self.trades[symbol]["all"].copy()
        trade["value_re"] = trade["value"] + trade["out_value"]
        
        portfolio_data = self.portfolio_data.loc[self.portfolio_data["symbol"] == symbol]
        
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
        return fig
    
    def all(self):
        ""
        

class VizAsset:
    
    def get_points(self, trades):
        loc = np.where(trades['status'] == 'Open')
        entry_points = trades.iloc[loc][['side', 'status', 'price', 'pnl']]
        
        loc = np.where(trades['status'] == 'Close')
        exit_points = trades.iloc[loc][['side', 'status', 'price', 'pnl']]
        
        return entry_points, exit_points
    
    
    def candle(self, trades, data):
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
    
    def __init__(self, portfolio_data, symbol):
        self.symbol = symbol
        self.portfolio_data = portfolio_data.copy()
    
    def show(self):
        
        self.portfolio_data.set_index("date", inplace = True)
        portfolio_data = self.portfolio_data.loc[self.portfolio_data["symbol"] == self.symbol]
        
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
    
    def __init__(self, trades_data):
        self.data = trades_data
    
    def long_short_per_step(self, symbol):
        fig = subplot(nb_cols=2, nb_rows=1)
        
        data_long = self.data[symbol]["long"]
        data_short = self.data[symbol]["short"]
        
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
        fig = subplot(nb_cols=2, nb_rows=1)
        
        data_long = self.data[symbol]["long"][self.data[symbol]["long"]["status"] == "Close"]
        data_short = self.data[symbol]["short"][self.data[symbol]["short"]["status"] == "Close"]
        
        
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

        