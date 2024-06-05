import requests
import time
import hashlib
import hmac

from app.config import API_KEY, API_SECRET, BASE_URL


# Test
API_KEY = "d727ada381ac80bb187e04ca361e0e0f6ba5f6fc22d3cbf610c17c32d936657e"
API_SECRET = "2f33bf9f838e705446915b60dfa4440c2303d478a7a726536bd0b264c2b1ec45"
URL = "https://testnet.binancefuture.com"

#BASE_URL = 'https://fapi.binance.com'
BASE_URL = "https://testnet.binancefuture.com"


class Base:
    
    def create_signature(self, query_string, secret):
        return hmac.new(secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()

    def binance_request(self, endpoint, params):
        params['timestamp'] = int(time.time() * 1000)
        query_string = '&'.join([f"{key}={value}" for key, value in sorted(params.items())])
        signature = self.create_signature(query_string, API_SECRET)
        headers = {
            'X-MBX-APIKEY': API_KEY
        }
        response = requests.get(f"{BASE_URL}{endpoint}?{query_string}&signature={signature}", headers=headers)
        return response.json()

    def binance_post_request(self, endpoint, params):
        params['timestamp'] = int(time.time() * 1000)
        query_string = '&'.join([f"{key}={value}" for key, value in sorted(params.items())])
        signature = self.create_signature(query_string, API_SECRET)
        headers = {
            'X-MBX-APIKEY': API_KEY
        }
        response = requests.post(f"{BASE_URL}{endpoint}?{query_string}&signature={signature}", headers=headers)
        return response.json()
    
    def binance_delete_request(self, endpoint, params):
        params['timestamp'] = int(time.time() * 1000)
        query_string = '&'.join([f"{key}={value}" for key, value in sorted(params.items())])
        signature = self.create_signature(query_string, API_SECRET)
        headers = {
            'X-MBX-APIKEY': API_KEY
        }
        response = requests.delete(f"{BASE_URL}{endpoint}?{query_string}&signature={signature}", headers=headers)
        return response.json()
    
    def get_price(self, symbol):
        params = {'symbol': symbol}
        return self.binance_request('/fapi/v1/ticker/price', params)
    
    def get_mark_price(self, symbol):
        params = {"symbol": symbol}
        return self.binance_request('/fapi/v1/premiumIndex', params)
    
    def get_filters(self):
        return self.binance_request('/fapi/v1/exchangeInfo', {})
    
    def get_open_orders(self):
        return self.binance_request('/fapi/v1/openOrders', {})
    