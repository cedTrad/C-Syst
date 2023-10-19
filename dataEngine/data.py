import pandas as pd
import numpy as np
import sqlalchemy
import os

#from .ohlc import update_data, asset_binance


DEFAULT_PATH = os.path.join(os.path.expanduser("~"), "Desktop", "CedAlgo", "database")
DEFAULT_INTERVAL = "1d"

class connect_db:
    
    def __init__(self, name : str, interval = DEFAULT_INTERVAL, path = DEFAULT_PATH):
        self.name = name
        self.interval = interval
        self.PATH = os.path.join(path, name+"_"+interval+".db")
        
        self.engine = sqlalchemy.create_engine('sqlite:///'+self.PATH)
    
    def get_data(self, symbol , start = '2017', end = '2023'):
        data = pd.read_sql(symbol+"USDT", self.engine)
        data.set_index('time' , inplace=True)
        data['volume'] = pd.to_numeric(data['volume'])
        data = data[['open', 'high', 'low' , 'close' , 'volume']]
        data = data.loc[start:end].copy()
        return data
    
    
    def update(self, assets = None, interval = "1d"):
        if assets is None:
            try:
                all_assets = asset_binance()
                update_data(all_assets, interval)
            except:
                pass
        else:
            update_data(assets, interval)
    

