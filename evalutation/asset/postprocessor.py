from .processing import Processing    
from .metrics import Metric


class Postprocessor:
    
    def __init__(self):
        self.metric = Metric()
        self.trans = Processing()
        self.type = ["all", "long", "short"]
        #self.type = ["all"]
    
    
    def get_data(self, trades_data):
        self.trades_data = self.trans.load(trades_data)
        self.datas = self.trans.split_asset(self.trades_data)
        return self.datas
    
    
    def update_indicator(self, symbol):
        lines = {}
        data = self.datas[symbol]
        for data_type in self.type:
            trade = data[data_type].copy()
            metrics = self.metric.excecute(trade = trade)
            lines[data_type] = metrics
        return lines
    
    

