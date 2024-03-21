from .viz import Benchmark


class Report:
    
    def __init__(self, data, tradeData, portfolioData):
        self.data = data
        self.benchmark = Benchmark(tradeData, portfolioData)
        
    def plot_equity(self, value=True):
        fig_equ = self.benchmark.equity(value)
        fig_equ.show()
        
        fig_asset = self.benchmark.asset(self.data)
        fig_asset.show()
        