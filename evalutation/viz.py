import numpy as np
from plot import *


class VizBenchmark:
    
    def __init__(self, trades):
        self.trades = trades
    
    def show(self, symbol):
        
        trade = self.trades[symbol]["all"]
        
        fig = create_figure()
        add_line(fig, trade, feature="price_cum", name="price")
        add_line(fig, trade, feature="cum_rets", name="strategie")
        
        return fig
    

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
        
        fig.update_layout(height = 800 , width =1000,
                          legend = dict(orientation="h",
                                        yanchor="bottom", y=1,
                                        xanchor="right", x=0.5),
                          margin = {'t':0, 'b':0, 'l':10, 'r':0}
                          )
        return fig


class VizPortfolio:
    
    def __init__(self, portfolio_data):
        self.portfolio = portfolio_data
    
    def show(self):
        
        fig = create_figure()
        
        add_line(fig, data=self.portfolio, feature="capital", name="capital")
        add_bar(fig, data=self.portfolio, feature="risk_value", name = "risk")
        add_bar(fig, data=self.portfolio, feature="available_value", name = "available")
        
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
    
    def long_short(self, symbol):
        fig = create_figure()
        
        data_long = self.data[symbol]["long"]
        data_short = self.data[symbol]["short"]
        
        add_hist(fig, data_long, feature="rets", name="long")
        add_hist(fig, data_short, feature="rets", name="short")
        
        add_vline(fig, x=0, color="black")
        
        fig.update_layout(height = 350 , width = 700,
                          legend = dict(orientation="h",
                                        yanchor="bottom", y=1,
                                        xanchor="right", x=0.5),
                          margin = {'t':0, 'b':0, 'l':10, 'r':0}
                          )
        return fig

          
class VizRisk:
    
    def __init__(self):
        self.p = 0

        