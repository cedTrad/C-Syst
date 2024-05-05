from dataEngine.data import connect_db

class Market:
    
    def __init__(self, size, start, end , interval):
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
    

