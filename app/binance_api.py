import requests
import hashlib
import hmac
import time


API_KEY = 'PyT7KZFu80pFuHiMAfKIMgWHhZkpFOmQ6J0pHAtbH2vawQZZABwjRyv21db0fIGu'
API_SECRET = 'PEF7KyDCRu6dh8TWK22Vyda8kJjoXw9v9ScWy02iPQDUSSGWeeJkvqqXrt3ozLs3'


def create_signature(query_string, secret):
    return hmac.new(secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()

def binance_request(endpoint, params):
    base_url = 'https://api.binance.com'
    query_string = '&'.join([f"{key}={value}" for key, value in params.items()])
    signature = create_signature(query_string, API_SECRET)
    url = f"{base_url}{endpoint}?{query_string}&signature={signature}"
    headers = {'X-MBX-APIKEY': API_KEY}
    response = requests.get(url, headers=headers)
    return response.json()

def binance_post_request(endpoint, params):
    base_url = 'https://api.binance.com'
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
    return binance_request('/api/v3/account', params)

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
    return binance_request('/api/v3/allOrders', params)

def get_pnl():
    timestamp = int(time.time() * 1000)
    params = {
        'timestamp': timestamp,
        'recvWindow': 5000
    }
    return binance_request('/api/v3/account', params)

def place_order(symbol, side, order_type, quantity, price=None):
    timestamp = int(time.time() * 1000)
    params = {
        'symbol': symbol,
        'side': side,
        'type': order_type,
        'quantity': quantity,
        'timestamp': timestamp,
        'recvWindow': 5000
    }
    if price:
        params['price'] = price
        params['timeInForce'] = 'GTC'  # Good Till Cancelled
    return binance_post_request('/api/v3/order', params)
