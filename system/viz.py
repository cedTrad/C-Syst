import numpy as np

from .utils.plot import subplot, subplots, add_bar, add_line, plot_candle, signal_point, create_figure, color_returns, color_trades, add_second_y

import plotly.figure_factory as ff



class Benchmark:
    
    def __init__(self, tradeDataAgent, portfolioDataAgent):
        self.tradeDataAgent = tradeDataAgent.copy()
        self.portfolioDataAgent = portfolioDataAgent.copy()
        
        self.preprocess()
        
        
    def preprocess(self):
        self.tradeDataAgent.set_index('date', inplace = True)
        self.portfolioDataAgent.set_index('date', inplace = True)
        
        self.capital = self.portfolioDataAgent["capital"]
        self.tradeDataAgent["benchmark"] = self.tradeDataAgent["cum_price"]
        
        
    def equity(self, agentId):
        print(agentId)
        fig = subplot(nb_cols = 1, nb_rows = 2, row_heights=[0.7, 0.3])
        add_line(fig, data=self.tradeDataAgent, feature="benchmark", name=f"market", col=1, row=1)
        
        add_bar(fig=fig, data=self.tradeDataAgent, feature='pnl_pct', name=f"pnl pct", col=1, row=1)
        add_line(fig, data=self.portfolioDataAgent, feature="cum_rets", name=f" cum rets", col=1, row=1)
        #add_line(fig, data=self.tradeDataAgent, feature="cum_rets", name=f" cum rets asset {agentId}", col=1, row=1)
        
        add_line(fig, data=self.portfolioDataAgent, feature="drawdown", name=f"drawdown", col=1, row=2)
        
        fig.update_layout(height = 300 , width = 1200,
                          legend = dict(orientation="h",
                                        yanchor="bottom", y=1,
                                        xanchor="right", x=0.5),
                          margin = {'t':0, 'b':0, 'l':10, 'r':0}
                          )
        
        return fig
        
    
    def get_points(self):
        loc = np.where(self.tradeDataAgent["status"] == "Open")
        entryPoints = self.tradeDataAgent.iloc[loc][['side', 'status', 'price', 'pnl']]
        
        loc = np.where(self.tradeDataAgent["status"] == "Close")
        exitPoints = self.tradeDataAgent.iloc[loc][['side', 'status', 'price', 'pnl']]
        
        return entryPoints, exitPoints
        
    def candle(self, fig, col, row, data, symbol):
        
        entryPoints, exitPoints = self.get_points()
        
        start = self.tradeDataAgent.index[0]
        end = self.tradeDataAgent.index[-1]
        
        data = data.loc[start : end]
        
        plot_candle(fig, data=data, col=col, row=row, symbol=f"OHLC : {symbol}")
        signal_point(fig, col=col, row=row, x=entryPoints.index, y=entryPoints.price, name="int", marker=(5, 10, 'blue'))
        signal_point(fig, col=col, row=row, x=exitPoints.index, y=exitPoints.price, name="out", marker=(6, 10, 'black'))
        color_trades(fig=fig, col=col, row=row, entry=entryPoints, exit=exitPoints, opacity=0.2)
        
        
    def asset(self, data, agentId):
        symbol = agentId[1]
        
        fig = subplots(nb_rows=3, nb_cols=1, row_heights=[0.15, 0.7, 0.15])
        
        add_bar(fig=fig, col=1, row=1, data=self.tradeDataAgent, feature='pnl', name='pnl')
        add_line(fig=fig, col=1, row=1, data=self.tradeDataAgent, feature="pnl_pct", name='pnl_pct')
        #add_second_y(fig=fig, col=1, row=1, data=self.tradeDataAgent, name='pnl_pct')
        
        self.candle(fig=fig, col=1, row=2, data=data, symbol=symbol)
        add_second_y(fig=fig, col=1, row=2, data=self.tradeDataAgent, name="session")
        add_line(fig, data=self.portfolioDataAgent, feature="cum_rets", name=f"cum rets", col=1, row=3)
        
        fig.update_layout(height = 800 , width = 1200,
                          legend = dict(orientation="h",
                                        yanchor="bottom", y=1,
                                        xanchor="right", x=0.5),
                          margin = {'t':0, 'b':0, 'l':10, 'r':0}
                          )
        
        return fig