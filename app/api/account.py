from .base import Base


class Account(Base):
    
    def __init__(self):
        super().__init__()
    
    def get_positions(self):
        return self.binance_request('/fapi/v2/positionRisk', {})

    def get_wallet(self):
        return self.binance_request('/fapi/v2/account', {})
    
    def get_open_orders(self):
        return self.binance_request('/fapi/v1/openOrders', {})
    
    def get_ohlc_data(self, symbol, interval='1m', limit=100):
        params = {
            'symbol': symbol,
            'interval': interval,
            'limit': limit
        }
        return self.binance_request('/fapi/v1/klines', params)
    