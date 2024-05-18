import pandas as pd

from dataEngine.data import connect_db



class MarketEvent:
    
    def __init__(self, size, start, end, interval):
        self.size = size
        self.start = start
        self.end = end
        self.db = connect_db(name = "database", interval = interval)
    
    def gen_data(self, symbol):
        i = 0
        data = self.db.get_data(symbol, start = self.start, end = self.end)
        while True:
            batch = data.iloc[i : i + self.size]
            if len(batch) == self.size:
                yield batch
                i += 1
            else:
                break
    
    def get_data(self, symbol):
        return self.gen_data(symbol)


class PostEvent:
    
    def __init__(self):
        self.portfolioData = pd.DataFrame()
        self.metricData = pd.DataFrame()
        self.tradeData = pd.DataFrame()
        self.data = pd.DataFrame()
        self.sessionData = pd.DataFrame()
        
        
    def add_trade_line(self, agentId, date, price, asset, session_id):
        line = {'agentId' : agentId, 'date' : date, 'price' : price, 
                'quantity' : asset.quantity, 'position' : asset.position,
                'side' : asset.type, 'state' : str(asset.state),
                'in_value' : asset.in_value, 'out_value' : asset.out_value,
                'value' : asset.value, 'pnl' : asset.pnl, 'pnl_pct' : asset.pnl_pct,
                'symbol' : asset.symbol, "session" : session_id}
        add = pd.DataFrame(line , index = [date])
        self.tradeData = pd.concat([self.tradeData, add], ignore_index = True)
        
        
    def add_portfolio_line(self, agentId, date, symbol, portfolio, session_id):
        line = {'agentId' : agentId, 'date' : date,
                'risk_value' : portfolio.risk_value, 'available_value' : portfolio.available_value,
                'capital' : portfolio.capital, "symbol" : symbol, "session" : session_id}
        
        add = pd.DataFrame(line, index = [date])
        self.portfolioData = pd.concat([self.portfolioData, add], ignore_index = True)
    
    
    def add_metrics_line(self, date, line):
        add = pd.DataFrame(line, index=[date])
        self.metricData = pd.concat([self.metricData, add], ignore_index=True)
        
        
    def add_data(self, agentId, date, price, asset, portfolio, session_id):
        self.add_trade_line(agentId, date, price, asset, session_id)
        self.add_portfolio_line(agentId, date, asset.symbol, portfolio, session_id)
    
    
    def add_session(self, session):
        add = pd.DataFrame(session, index=[1])
        self.sessionData = pd.concat([self.session, add], ignore_index=True)
        
    
