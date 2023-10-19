class Momentum:
    
    def __init__(self, data):
        self.data = data.copy()
        
    def preprocess(self):
        self.data['mom'] = self.data["close"].pct_change().rolling(3).mean()
    
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
    
    def set_params(self, m1, m2, m3):
        self.m1 = m1
        self.m2 = m2
        self.m3 = m3
    
    def preprocess(self):
        self.data["m1"] = self.data.close.rolling(self.m1).mean()
        self.data["m2"] = self.data.close.rolling(self.m2).mean()
        self.data["m3"] = self.data.close.rolling(self.m3).mean()
        #display(self.data.iloc[-1])
    
    def run(self, bar):
        self.preprocess()
        
        if self.data["m1"].iloc[bar] < self.data["m2"].iloc[bar] < self.data["m3"].iloc[bar]:
            return "LONG"
        elif self.data["m1"].iloc[bar] > self.data["m2"].iloc[bar] > self.data["m3"].iloc[bar]:
            return "SHORT"
        else:
            return None
        



