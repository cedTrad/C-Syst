class Momentum:
    
    def __init__(self, data):
        self.data = data.copy()
        
    def update_params(self, params):
        self.params = params
        
    def preprocess(self):
        self.data['mom'] = self.data["close"].pct_change().rolling(self.params).mean()
    
    def run(self, bar):
        self.preprocess()
        
        if self.data["mom"].iloc[bar] > 0:
            return "LONG"
        elif self.data["mom"].iloc[bar] < 0:
            return "SHORT"
        else:
            return None


 

class TMM:
    
    def __init__(self, data):
        self.data = data.copy()
    
    def update_params(self, params):
        self.m1 = params[0]
        self.m2 = params[1]
        self.m3 = params[2]
    
    def preprocess(self):
        self.data["m1"] = self.data.close.rolling(self.m1).mean()
        self.data["m2"] = self.data.close.rolling(self.m2).mean()
        self.data["m3"] = self.data.close.rolling(self.m3).mean()
        
    
    def run(self, bar):
        self.preprocess()
        if self.data["m1"].iloc[bar] < self.data["m2"].iloc[bar] < self.data["m3"].iloc[bar]:
            return "LONG"
        elif self.data["m1"].iloc[bar] > self.data["m2"].iloc[bar] > self.data["m3"].iloc[bar]:
            return "SHORT"
        else:
            return None
        



