import requests
import pandas as pd
import hashlib
import hmac
import time
from cachetools import cached, TTLCache
from app.config import API_KEY, API_SECRET

# Cache de 10 minutes
cache = TTLCache(maxsize=100, ttl=600)

BASE_URL = "https://api.binance.com"
FUTURES_URL = "https://fapi.binance.com"

def fetch_crypto_data(symbol):
    url = f'{BASE_URL}/api/v3/ticker/price?symbol={symbol}'
    response = requests.get(url)
    data = response.json()
    return float(data['price'])

@cached(cache)
def fetch_historical_data(symbol, interval, period='7d'):
    # Calcul de la limite en fonction de la période sélectionnée
    period_limits = {'1d': 24*60, '7d': 7*24*60, '1m': 30*24*60}
    limit = period_limits.get(period, 100)
    
    url = f'{BASE_URL}/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}'
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df['open'] = df['open'].astype(float)
    df['high'] = df['high'].astype(float)
    df['low'] = df['low'].astype(float)
    df['close'] = df['close'].astype(float)
    return df

def sign_request(params):
    query_string = '&'.join([f"{key}={params[key]}" for key in sorted(params)])
    signature = hmac.new(API_SECRET.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
    return signature

def place_order(symbol, quantity, price, side, order_type, leverage=1):
    timestamp = int(time.time() * 1000)
    params = {
        "symbol": symbol,
        "side": side,
        "type": order_type,
        "quantity": quantity,
        "price": price if order_type == "LIMIT" else None,
        "timeInForce": "GTC" if order_type == "LIMIT" else None,
        "leverage": leverage,
        "timestamp": timestamp
    }
    params = {k: v for k, v in params.items() if v is not None}
    params["signature"] = sign_request(params)
    
    headers = {"X-MBX-APIKEY": API_KEY}
    response = requests.post(f"{FUTURES_URL}/fapi/v1/order", headers=headers, params=params)
    return response.json()

def get_open_positions():
    timestamp = int(time.time() * 1000)
    params = {
        "timestamp": timestamp
    }
    params["signature"] = sign_request(params)
    
    headers = {"X-MBX-APIKEY": API_KEY}
    response = requests.get(f"{FUTURES_URL}/fapi/v2/positionRisk", headers=headers, params=params)
    return response.json()

def get_order_history(symbol):
    timestamp = int(time.time() * 1000)
    params = {
        "symbol": symbol,
        "timestamp": timestamp
    }
    params["signature"] = sign_request(params)
    
    headers = {"X-MBX-APIKEY": API_KEY}
    response = requests.get(f"{FUTURES_URL}/fapi/v1/allOrders", headers=headers, params=params)
    return response.json()

def get_pnl():
    timestamp = int(time.time() * 1000)
    params = {
        "timestamp": timestamp
    }
    params["signature"] = sign_request(params)
    
    headers = {"X-MBX-APIKEY": API_KEY}
    response = requests.get(f"{FUTURES_URL}/fapi/v2/account", headers=headers, params=params)
    account_info = response.json()
    return account_info['totalUnrealizedProfit']
