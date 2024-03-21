from .utils.plot import subplot, subplots, add_bar, add_line, plot_candle, signal_point, create_figure, color_returns, color_trades, add_second_y

import plotly.figure_factory as ff



class Benchmark:
    
    def __init__(self, tradeDataAgent, portfolioDataAgent):
        self.tradeDataAgent = tradeDataAgent.copy()
        self.portfolioDataAgent = portfolioDataAgent.copy()
        
        self.preprocess()
        
        
    def preprocess(self):
        self.capital = self.portfolioDataAgent["capital"]
        self.tradeDataAgent["cum_gp_value"] = self.tradeDataAgent["cum_gp"] + self.capital
        self.tradeDataAgent["benchmark_value"] = self.tradeDataAgent["price_cum"] * self.capital
        self.tradeDataAgent["value_re_value"] = self.tradeDataAgent["value"] + self.tradeDataAgent["out_value"]
        
        
    def drawdown(self, value=False):
        if value:
            return self.portfolioDataAgent["capital"] - self.portfolioDataAgent["capital"].cummax()
        else:
            return (self.portfolioDataAgent["capital"] - self.portfolioDataAgent["capital"].cummax()) / self.portfolioDataAgent["capital"].cummax()
        
        
    def equity(self, value=False):
        #self.preprocess()
        
        agentId = self.tradeDataAgent.iloc[0]["agentId"]
        symbol = self.tradeDataAgent.iloc[0]["symbol"]
        
        if value:
            self.portfolioDataAgent["drawdown"] = self.drawdown(value)
            
            fig = subplot(nb_cols = 2, nb_rows = 1)
            add_line(fig, data=self.tradeDataAgent, feature="benchmark", name=f"{agentId} : market", col=1, row=1)
            add_line(fig, data=self.tradeDataAgent, feature="cum_gp", name=f"{agentId} : {symbol}", col=1, row=1)
            
            add_line(fig, data=self.portfolioDataAgent, feature="drawdown", name=f"{agentId} : market", col=2, row=1)
            
        else:
            self.portfolioDataAgent["drawdown"] = self.drawdown(value)
            
            fig = subplot(nb_cols = 1, nb_rows = 2)
            add_line(fig, data=self.tradeDataAgent, feature="benchmark_value", name=f"{agentId} : market", col=1, row=1)
            add_line(fig, data=self.tradeDataAgent, feature="cum_gp_value", name=f"{agentId} : {symbol}", col=1, row=1)
            
            add_line(fig, data=self.portfolioDataAgent, feature="drawdown", name=f"{agentId} : market", col=2, row=1)
        
        return fig
        
        
    def candle(self, fig, col, row, data, symbol):
        
        entryPoints, exitPoints = self.get_points(self.tradeDataAgent)
        
        start = self.tradeDataAgent.index[0]
        end = self.tradeDataAgent.index[-1]
        
        data = data.loc[start : end]
        
        plot_candle(fig, data=data, col=col, row=row, symbol=f"OHLC : {symbol}")
        signal_point(fig, col=col, row=row, x=entryPoints.index, y=entryPoints.price, name="int", marker=(5, 10, 'blue'))
        signal_point(fig, col=col, row=row, x=exitPoints.index, y=exitPoints.price, name="out", marker=(6, 10, 'black'))
        color_trades(fig=fig, col=col, row=row, entry=entryPoints, exit=exitPoints, opacity=0.2)
        
        
    def asset(self, data):
        
        agentId = self.tradeDataAgent.iloc[0]["agentId"]
        symbol = self.tradeDataAgent.iloc[0]["symbol"]
        self.portfolioDataAgent["drawdown"] = self.drawdown()
        
        fig = subplots(nb_rows=3, nb_cols=1, row_heights=[0.15, 0.7, 0.15])
        
        add_bar(fig=fig, col=1, row=1, data=self.tradeDataAgent, feature='pnl', name='pnl')
        add_second_y(fig=fig, col=1, row=1, data=self.tradeDataAgent, name='pnl_pct')
        
        self.candle(fig=fig, col=1, row=2, data=data, symbol=symbol)
        
        add_line(fig, data=self.portfolioDataAgent, feature="drawdown", name=f"drawdown", col=1, row=3)
        
        fig.update_layout(height = 800 , width = 1000,
                          legend = dict(orientation="h",
                                        yanchor="bottom", y=1,
                                        xanchor="right", x=0.5),
                          margin = {'t':0, 'b':0, 'l':10, 'r':0}
                          )
        
        return fig