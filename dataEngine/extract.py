import requests
import pandas as pd
import numpy as np

from datetime import datetime, timedelta

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import requests
import hmac
import hashlib
from urllib.parse import urljoin, urlencode

from dataEngine.base import Base
from dataEngine.table import CandlestickData

import utils

# Extract data from binance

#       ------ Spot


#       ------ Future
class Binance:
    
    def __init__(self, symbol, interval):
        self.symbol = symbol
        self.start = self.config_date()
        self.interval = interval
        self.base_url = "https://testnet.binancefuture.com"
        self.endpoint = "/fapi/v1/klines"
        self.set_engine()
    
    def config_date(self, date = '01/01/23 00:00:00'):
        datetime_str = date
        datetime_object = datetime.strptime(datetime_str, '%m/%d/%y %H:%M:%S') 
        return utils.datetime_to_timestamp(datetime_object) * 1000 
    
    def set_engine(self):
        engine = create_engine("sqlite:///binance_data.db")
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind = engine)
        self.session = Session()
        
    
    def klines(self, symbol, interval, start):
        params = {
            "symbol" : symbol,
            "interval" : interval,
            "startTime" : start
        }
        url = urljoin(self.base_url, self.endpoint)
        r = requests.get(url, params=params)
        code = r.status_code
        print("code : ",code)
        if code == 200:
            return r.json()
    
    
    def get_last_candle(self):
        last_candle = self.session.query(CandlestickData).order_by(CandlestickData.open_time.desc()).first()
        return last_candle
    
    
    def load(self):
        try:
            last_candle = self.get_last_candle()
            start = last_candle.open_time
        except AttributeError:
            start = self.start
        data = self.klines(self.symbol, self.interval, start)
        data.pop(0)
        for line in data:
            data = CandlestickData(line)
            self.session.add(data)
            self.session.commit()
        
        self.session.close()



#dd = Binance("BTCUSDT", "1d")
#dd.load()

# Extract data from DefiLama

class DefiLama:
    
    def __init__(self):
        self.symbol = 0
