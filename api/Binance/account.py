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


BALANCE_PATH = "/fapi/v2/balance"
ACCOUNT_PATH = "/fapi/v2/account"
POSITION_PATH = "/fapi/v2/positionRisk"
LEVERAGE_PATH = "/fapi/v1/leverage"

class Spot:
    
    def __init__(self):
        self.recvWindow = 50000


class Future:
    
    def __init__(self):
        self.recvWindow = 50000
        
    def currentPosition(self):
        timestamp = int(time.time() * 1000)
        params = {
            'timestamp' : timestamp,
            'recvWindow' : self.recvWindow
        }
        query_string = urlencode(params)
        params['signature'] = hmac.new(API_secret.encode('utf-8'),
                                    query_string.encode('utf-8'), hashlib.sha256).hexdigest()
        url = urljoin(URL, POSITION_PATH)
        r = requests.get(url, headers=headers, params=params)
        return r.json()
    
    
    def changePosition(self):
        timestamp = int(time.time() * 1000)
        params = {
            'timestamp' : timestamp,
            'dualSidePosition' : 'true',
            'recvWindow' : self.recvWindow
        }
        query_string = urlencode(params)
        params['signature'] = hmac.new(API_secret.encode('utf-8'),
                                    query_string.encode('utf-8'), hashlib.sha256).hexdigest()
        url = urljoin(URL, POSITION_PATH)
        r = requests.get(url, headers=headers, params=params)
        return r.json()
    
        
    def balance(self):
        timestamp = int(time.time() * 1000)
        params = {
            'timestamp' : timestamp,
            'recvWindow' : self.recvWindow
        }
        query_string = urlencode(params)
        params['signature'] = hmac.new(API_secret.encode('utf-8'),
                                    query_string.encode('utf-8'), hashlib.sha256).hexdigest()
        url = urljoin(URL, BALANCE_PATH)
        r = requests.get(url, headers=headers, params=params)
        return r.json()
    
    
    def info(self):
        timestamp = int(time.time() * 1000)
        params = {
            'timestamp' : timestamp,
            'recvWindow' : self.recvWindow
        }
        query_string = urlencode(params)
        params['signature'] = hmac.new(API_secret.encode('utf-8'),
                                    query_string.encode('utf-8'), hashlib.sha256).hexdigest()
        url = urljoin(URL, ACCOUNT_PATH)
        r = requests.get(url, headers=headers, params=params)
        return r.json()
    
    
    def positionInfo(self, symbol):
        timestamp = int(time.time() * 1000)
        params = {
            'symbol' : symbol,
            'timestamp' : timestamp,
            'recvWindow' : self.recvWindow  
        }
        query_string = urlencode(params)
        params['signature'] = hmac.new(API_secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
        url = urljoin(URL, POSITION_PATH)
        r = requests.get(url, headers=headers, params=params)
        return r.json()
    
    
    def leverage(self, symbol, interval): # interval : int, [1:125]
        timestamp = int(time.time() * 1000)
        params = {
            'symbol' : symbol,
            'leverage' : leverage,
            'timestamp' : timestamp,
            'recvWindow' : self.recvWindow
        }
        query_string = urlencode(params)
        params['signature'] = hmac.new(API_secret.encode('utf-8'),
                                    query_string.encode('utf-8'), hashlib.sha256).hexdigest()
        url = urljoin(URL, LEVERAGE_PATH)
        r = requests.post(url, headers=headers, params=params)
        return r.json()
    
    
    
    
    
    