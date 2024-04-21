

class Asset:
    
    def __init__(self, symbol):
        self.symbol = symbol
        self.quantity = 0
        self.value = 0
        self.value_re = 0
        self.position = 0
        self.in_value = 0
        self.tp = 0
        self.sl = 0
        self.out_value = 0
        self.type = None
        self.status = "-"
        self.state = ()
        self.pnl = 0
        self.pnl_pct = 0
            
            
    def get_pnl(self, price):
        if self.state[1] == ("SHORT"):
            return self.in_value - abs(self.quantity * price)
        return abs(self.quantity * price) - self.in_value
    
    
    def get_value(self, price):
        return self.in_value + self.get_pnl(price)
    
    def update_state(self, state):
        self.state = state
    
    def update(self, price, quantity = 0):
        
        if self.state[0] == ("Open"):
            self.quantity += quantity
            self.in_value = abs(self.quantity * price)
            self.pnl = self.get_pnl(price)
            self.pnl_pct = self.pnl / self.in_value
            self.out_value = 0
        
        elif self.state[0] == ("Close"):
            self.out_value = self.get_value(price)
            self.pnl = self.get_pnl(price)
            self.quantity += quantity
            self.pnl_pct = self.pnl / self.in_value
            self.in_value = 0
            
        elif self.state[0] == ("-"):
            self.out_value = 0
            self.pnl = self.get_pnl(price)
            self.pnl_pct = self.pnl / self.in_value if self.in_value !=0 else 0
        
        self.value = self.get_value(price)
        self.value_re = self.value if self.state[0] == ("Close") else self.value+self.out_value
        





class Portfolio:
    
    def __init__(self, name, capital):
        self.name = name
        self.capital = capital
        self.init_capital = capital
        self.available_value = capital
        self.risk_value = 0
        self.save_value = 0
        self.assets = {}
        
    def add_asset(self, symbol):
        self.assets[symbol] = Asset(symbol)
    
    def update_asset(self, asset):
        symbol = str(asset.symbol)
        self.assets.update({symbol : asset})
        
    def rebalance(self, amount):
        self.risk_value += amount
        self.available_value -= amount
        self.capital = self.risk_value + self.available_value
    
    def update_risk(self, asset):
        values = 0
        self.update_asset(asset)
        for asset in self.assets.values():
            values += asset.value_re
        self.risk_value = values
        
    def update(self, asset):
        self.update_risk(asset)
        self.available_value += asset.out_value
        self.capital = self.risk_value + self.available_value
        
    def clear(self):
        self.capital = self.init_capital
        self.available_value = self.init_capital
        self.risk_value = 0
        self.save_value = 0
        self.assets = {}
        
        
        

class PFuture(Portfolio):
    def __init__(self, name, capital):
        #Portfolio.__init__(self, name, capital)
        super().__init__(name, capital)
        self.long = {}
        self.short = {}
        self.long_portfolio = 0
        self.short_portfolio = 0


class PDefi:
    def __init__(self):
        self.name = "metamask"