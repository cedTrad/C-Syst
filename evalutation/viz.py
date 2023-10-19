import numpy as np
from plot import plot_candle, add_line, add_second_y, add_scatter, add_bar, subplots, signal_point, color_trades

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


class Pnl:
    
    def __init__(self):
        self.p = 0


class Portfolio:
    
    def __init__(self):
        self.p = 0
        
        
class Risk:
    
    def __init__(self):
        self.p = 0

        