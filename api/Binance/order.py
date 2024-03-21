import json
from configparser import ConfigParser
import requests
import hmac
import hashlib
from urllib.parse import urljoin, urlencode
import time


API_Key = "d727ada381ac80bb187e04ca361e0e0f6ba5f6fc22d3cbf610c17c32d936657e"
API_secret = "2f33bf9f838e705446915b60dfa4440c2303d478a7a726536bd0b264c2b1ec45"
URL = "https://testnet.binancefuture.com"

headers = {
    'X-MBX-APIKEY': API_Key
}

ORDER_PATH = "/fapi/v1/order"
ORDER_PATHS = "/fapi/v1/allOpenOrders"
LEVERAGE = "/fapi/v1/leverage"
TRADE_LIST = "/fapi/v1/userTrades"
LEVERAGE_BRACKET = "/fapi/v1/leverageBracket"


class Base:
    
    def __init__(self, symbol, recvWindow):
        self.symbol = symbol
        self.positionSide = 'BOTH'      #       ( a revoir )
        self.recvWindow = recvWindow
        
        
    def orderMarket(self, quantity ,side , orderType = 'MARKET', timeInForce = 'GTC'):
        timestamp = int(time.time() * 1000)
        params = {
            'symbol' : self.symbol,
            'side' : side,
            'positionSide': self.positionSide,
            'type' : orderType,
            'quantity' : quantity,
            'timestamp' : timestamp,
            'recvWindow' : self.recvWindow
        }
        query_string = urlencode(params)
        params['signature'] = hmac.new(API_secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
        url = urljoin(URL, ORDER_PATH)
        r = requests.post(url, headers=headers, params=params)
        return r
    
    
    def orderLimit(self, quantity, price, side, orderType = 'LIMIT', timeInForce = 'GTC'):
        timestamp = int(time.time() * 1000)
        params = {
            'symbol' : self.symbol,
            'side' : side,
            'positionSide': self.positionSide,
            'type' : orderType,
            'quantity' : quantity,
            'price' : price,
            'timeInForce' : timeInForce,
            'timestamp' : timestamp,
            'recvWindow' : self.recvWindow
        }
        query_string = urlencode(params)
        params['signature'] = hmac.new(API_secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
        url = urljoin(URL, ORDER_PATH)
        r = requests.post(url, headers=headers, params=params)
        return r
    
    
    def limitOrder(self, closePrice, side, orderType, timeInForce = 'GTC'):
        timestamp = int(time.time() * 1000)
        params = {
            'symbol' : self.symbol,
            'side' : side,
            'positionSide': self.positionSide,
            'type' : orderType,
            'stopPrice' : closePrice,
            'closePosition' : 'true',
            'timeInForce' : timeInForce,
            'timestamp' : timestamp,
            'recvWindow' : self.recvWindow
        }
        query_string = urlencode(params)
        params['signature'] = hmac.new(API_secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
        url = urljoin(URL, ORDER_PATH)
        r = requests.post(url, headers=headers, params=params)
        return r
    
    def cancelOrder(self, orderId):
        timestamp = int(time.time() * 1000)
        params = {
            'symbol' : self.symbol,
            'orderId' : orderId,
            'timestamp' : timestamp,
            'recvWindow' : self.recvWindow
        }
        query_string = urlencode(params)
        params['signature'] = hmac.new(API_secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
        url = urljoin(URL, ORDER_PATH)
        r = requests.delete(url, headers=headers, params=params)
        return r
    
    
    def closeAllOrder(self):
        timestamp = int(time.time() * 1000)
        params = {
            'symbol' : self.symbol,
            'timestamp' : timestamp,
            'recvWindow' : self.recvWindow
        }
        query_string = urlencode(params)
        params['signature'] = hmac.new(API_secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
        url = urljoin(URL, ORDER_PATHS)
        r = requests.delete(url, headers=headers, params=params)
        return 
    
    def leverage(self, leverage):
        timestamp = int(time.time() * 1000)
        params = {
            'symbol' : self.symbol,
            'leverage' : leverage,
            'timestamp' : timestamp,
            'recvWindow' : self.recvWindow
        }
        query_string = urlencode(params)
        params['signature'] = hmac.new(API_secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
        url = urljoin(URL, LEVERAGE)
        r = requests.post(url, headers=headers, params=params)
        return r
    
    def leverage_bracket(self):
        timestamp = int(time.time() * 1000)
        params = {
            'symbol' : self.symbol,
            'timestamp' : timestamp,
            'recvWindow' : self.recvWindow
        }
        query_string = urlencode(params)
        params['signature'] = hmac.new(API_secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
        url = urljoin(URL, LEVERAGE_BRACKET)
        r = requests.get(url, headers=headers, params=params)
        return r



class OrderAPIBinance(Base):
    
    def __init__(self, symbol, recvWindow = 10000):
        Base.__init__(self, symbol, recvWindow)
        
    def buy(self, quantity, orderType='MARKET'):
        orderBuy = self.orderMarket(quantity = quantity, side = "BUY", orderType = orderType)
        return orderBuy
    
    def sell(self, quantity, orderType = "MARKET"):
        orderSell = self.orderMarket(quantity, side = "SELL", orderType = orderType)
        return orderSell
    
    def stopLoss(self, closePrice, side):
        stopLoss = self.limitOrder(closePrice = closePrice, side = side, orderType = "STOP_MARKET")
        return stopLoss
    
    def takeProfit(self, closePrice, side):
        takeProfit = self.limitOrder(closePrice = closePrice, side = side, orderType = "TAKE_PROFIT_MARKET")
        return takeProfit
    
    
    def open_long(self, quantity, orderType = "MARKET"):
        order = self.buy(quantity=quantity)
        
    def close_long(self, quantity, orderType = "MARKET"):
        order = self.sell(quantity=quantity)
        
    def open_short(self, quantity, orderType = "MARKET"):
        order = self.sell(quantity=quantity)
    
    def close_short(self, quantity, orderType = "MARKET"):
        order = self.buy(quantity=quantity)
        
        
        