import requests
import hashlib
import hmac
import time


API_KEY = "C8Lw6mJh4CNYQXVIgdRAv64S5bQzh1RyNBQJNL3C2roe8rsxyTtN8EfB4faadhD3"
API_SECRET = "aokTvHmhUOFnhOlSNp2a7VPh1NVfkydrFHgdqRArKjuoz2AXYJTBOsNsyxhPsXs8"


def create_signature(query_string, secret):
    return hmac.new(secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()

def binance_request(endpoint, params):
    base_url = 'https://fapi.binance.com'
    query_string = '&'.join([f"{key}={value}" for key, value in params.items()])
    signature = create_signature(query_string, API_SECRET)
    url = f"{base_url}{endpoint}?{query_string}&signature={signature}"
    headers = {'X-MBX-APIKEY': API_KEY}
    response = requests.get(url, headers=headers)
    return response.json()

def binance_post_request(endpoint, params):
    base_url = 'https://fapi.binance.com'
    query_string = '&'.join([f"{key}={value}" for key, value in params.items()])
    signature = create_signature(query_string, API_SECRET)
    url = f"{base_url}{endpoint}?{query_string}&signature={signature}"
    headers = {'X-MBX-APIKEY': API_KEY}
    response = requests.post(url, headers=headers)
    return response.json()

def get_positions():
    timestamp = int(time.time() * 1000)
    params = {
        'timestamp': timestamp,
        'recvWindow': 5000
    }
    return binance_request('/fapi/v2/positionRisk', params)

def get_history(symbol=None, start_time=None, end_time=None):
    timestamp = int(time.time() * 1000)
    params = {
        'timestamp': timestamp,
        'recvWindow': 5000
    }
    if symbol:
        params['symbol'] = symbol
    if start_time:
        params['startTime'] = start_time
    if end_time:
        params['endTime'] = end_time
    return binance_request('/fapi/v1/allOrders', params)

def get_pnl():
    timestamp = int(time.time() * 1000)
    params = {
        'timestamp': timestamp,
        'recvWindow': 5000
    }
    return binance_request('/fapi/v2/account', params)

def get_price(symbol):
    timestamp = int(time.time() * 1000)
    params = {
        'symbol': symbol,
        'timestamp': timestamp,
        'recvWindow': 5000
    }
    return binance_request('/fapi/v1/ticker/price', params)

def place_order(symbol, side, order_type, quantity, leverage, price=None):
    timestamp = int(time.time() * 1000)
    params = {
        'symbol': symbol,
        'side': side,
        'type': order_type,
        'quantity': quantity,
        'leverage': leverage,
        'timestamp': timestamp,
        'recvWindow': 5000
    }
    if price:
        params['price'] = price
        params['timeInForce'] = 'GTC'  # Good Till Cancelled
    return binance_post_request('/fapi/v1/order', params)

def get_all_symbols():
    response = requests.get('https://api.binance.com/api/v3/exchangeInfo')
    data = response.json()
    symbols = [symbol['symbol'] for symbol in data['symbols']]
    return symbols
