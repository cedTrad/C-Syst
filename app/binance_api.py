import requests
import time
import hashlib
import hmac
import os
import pandas as pd
from decimal import Decimal

from app.config import API_KEY, API_SECRET, BASE_URL


# Test
API_KEY = "d727ada381ac80bb187e04ca361e0e0f6ba5f6fc22d3cbf610c17c32d936657e"
API_SECRET = "2f33bf9f838e705446915b60dfa4440c2303d478a7a726536bd0b264c2b1ec45"
URL = "https://testnet.binancefuture.com"

#BASE_URL = 'https://fapi.binance.com'
BASE_URL = "https://testnet.binancefuture.com"



# --------------------------------------------   Base  -----------------------------------------------

def create_signature(query_string, secret):
    return hmac.new(secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()

def binance_request(endpoint, params):
    params['timestamp'] = int(time.time() * 1000)
    query_string = '&'.join([f"{key}={value}" for key, value in sorted(params.items())])
    signature = create_signature(query_string, API_SECRET)
    headers = {
        'X-MBX-APIKEY': API_KEY
    }
    response = requests.get(f"{BASE_URL}{endpoint}?{query_string}&signature={signature}", headers=headers)
    return response.json()

def binance_post_request(endpoint, params):
    params['timestamp'] = int(time.time() * 1000)
    query_string = '&'.join([f"{key}={value}" for key, value in sorted(params.items())])
    signature = create_signature(query_string, API_SECRET)
    headers = {
        'X-MBX-APIKEY': API_KEY
    }
    response = requests.post(f"{BASE_URL}{endpoint}?{query_string}&signature={signature}", headers=headers)
    return response.json()

# ------------------------------------------------ End Base  -------------------------------------------

# ------------------------------------------------ OHLC Data  -------------------------------------------
def get_ohlc_data(symbol, start_date, end_date, interval):
    base_url = "https://api.binance.com"
    endpoint = "/api/v3/klines"

    params = {
        "symbol": symbol,
        "interval": interval,
        "startTime": int(start_date.timestamp() * 1000),
        "endTime": int(end_date.timestamp() * 1000),
        "limit": 500
    }

    response = requests.get(base_url + endpoint, params=params)
    data = response.json()

    if response.status_code == 200:
        ohlc_data = []
        for entry in data:
            ohlc_data.append({
                "time": pd.to_datetime(entry[0], unit='ms'),
                "open": float(entry[1]),
                "high": float(entry[2]),
                "low": float(entry[3]),
                "close": float(entry[4])
            })
        return ohlc_data
    else:
        return None

# ------------------------------------------------ End OHLC Data  -------------------------------------------

# ------------------------------------------------ Account  -------------------------------------------
def get_price(symbol):
    params = {'symbol': symbol}
    return binance_request('/fapi/v1/ticker/price', params)

def get_positions():
    return binance_request('/fapi/v2/positionRisk', {})

def get_pnl():
    return binance_request('/fapi/v2/account', {})




# ------------------------------------------------ End Account  -------------------------------------------


# ---------------------------------------------------- Open Order ---------------------------------------
def get_mark_price(symbol):
    params = {"symbol": symbol}
    return binance_request('/fapi/v1/premiumIndex', params)

def get_open_orders():
    return binance_request('/fapi/v1/openOrders', {})

def get_open_orders_count(symbol):
    orders = get_open_orders()
    return sum(1 for order in orders if order['symbol'] == symbol)

def get_current_position(symbol):
    positions = get_positions()
    position = next((p for p in positions if p['symbol'] == symbol), None)
    return float(position['positionAmt']) if position else 0.0


def get_filters(symbol):
    response = binance_request('/fapi/v1/exchangeInfo', {})
    symbol_info = next((item for item in response['symbols'] if item['symbol'] == symbol), None)
    if symbol_info:
        filters = {f['filterType']: f for f in symbol_info['filters']}
        return filters
    return None

# Market DEPTH
def get_order_book(symbol, limit=100):
    params = {
        'symbol': symbol,
        'limit': limit
    }
    return binance_request('/fapi/v1/depth', params)

# VOLUME
def get_ticker(symbol):
    params = {
        'symbol': symbol
    }
    return binance_request('/fapi/v1/ticker/24hr', params)

# Analyse de la liquidite
def analyze_liquidity(symbol):
    order_book = get_order_book(symbol)
    ticker = get_ticker(symbol)
    
    #Spread
    if len(order_book['bids']) > 0 and len(order_book['asks']) > 0:
        best_bid = float(order_book['bids'][0][0])
        best_ask = float(order_book['asks'][0][0])
        spread = (best_ask - best_bid) / best_bid
    else:
        spread = 10
    
    # Volume
    volume = float(ticker['volume'])
    
    #Depth
    bids = pd.DataFrame(order_book['bids'], columns=['price', 'quantity'], dtype=float)
    asks = pd.DataFrame(order_book['asks'], columns=['price', 'quantity'], dtype=float)
    
    total_bids = bids['quantity'].sum()
    total_asks = asks['quantity'].sum()
    
    # Règles de décision
    rules = {
        'spread': spread < 0.01,  # Spread < 1%
        'volume': volume > 1000,  # Volume > 1000 unités
        'depth': total_bids > 500 and total_asks > 500  # Profondeur significative
    }
    is_liquid = all(rules.values())
    print(symbol)
    return {
        'symbol': symbol,
        'spread': spread,
        'volume': volume,
        'total_bids': total_bids,
        'total_asks': total_asks,
        'is_liquid': is_liquid,
        'rules': rules
    }

def validate_order(symbol, quantity, side, price=None):
    filters = get_filters(symbol)
    if not filters:
        return {'code': -1, 'msg': 'No filters found for the symbol'}
    
    msg = {}
    sugg = {}
    
    # LOT_SIZE
    lot_size = filters.get('LOT_SIZE')
    if lot_size:
        min_qty = lot_size['minQty']
        max_qty = lot_size['maxQty']
        step_size = lot_size['stepSize']
        
        if quantity < float(min_qty):
            msg["minQty"] = f"Invalid Qty. Must be > {min_qty}"
            sugg["qty"] = float(min_qty)
        if quantity > float(max_qty):
            msg["maxQty"] = f"Invalid Qty. Must be < {max_qty}"
            sugg["qty"] = float(max_qty)
        if (Decimal(str(quantity)) - Decimal(min_qty)) % Decimal(step_size) != 0:
            msg["stepSize"] = f"Invalid stepSize"
            r = (Decimal(str(quantity)) - Decimal(min_qty)) % Decimal(step_size)
            sugg["qty"] = float(Decimal(str(quantity)) - r)
    
    # PRICE_FILTER
    price_filter = filters.get("PRICE_FILTER")
    if price_filter and price:
        min_price = price_filter["minPrice"]
        max_price = price_filter["maxPrice"]
        tick_size = price_filter["tickize"]
        if price < float(min_price):
            msg["minPrice"] = f"Invalid Price. Must be > {min_price}"
        if price > float(max_price):
            msg["maxPrice"] = f"Invalid Price. Must be < {max_price}"
        if (Decimal(str(price)) - Decimal(min_price)) % Decimal(tick_size) != 0:
            msg["tickSize"] = f"Invalid Tick Size"
    
     # PERCENT_PRICE
    percent_price = filters.get('PERCENT_PRICE')
    if percent_price and price:
        multiplierUp = percent_price.get('multiplierUp')
        multiplierDown = percent_price.get('multiplierDown')
        multiplierUPDec = percent_price.get('multiplierDecimal')
        mark_price = get_mark_price(symbol)['markPrice']
        
        if (side == "BUY") and (price > float(mark_price )*float(multiplierUp)):
            msg["percentPrice"] = f"BUY : Invalid"
        if (side == "SELL") and (price < float(mark_price) * float(multiplierDown)):
            msg["percentPrice"] = f"SELL : Invalid"
            
    
    # MARKET_LOT_SIZE
    market_lot_size = filters.get('MARKET_LOT_SIZE')
    if market_lot_size:
        m_min_qty = market_lot_size['minQty']
        m_max_qty = market_lot_size['maxQty']
        m_step_size = market_lot_size['stepSize']
        if quantity < float(m_min_qty):
            msg["MminQty"] = f"Invalid Qty. Must be > {m_min_qty}"
            sugg["Mqty"] = float(m_min_qty)
        if quantity > float(m_max_qty):
            msg["MmaxQty"] = f"Invalid Qty. Must be < {m_max_qty}"
            sugg["Mqty"] = float(m_max_qty)
        if (Decimal(str(quantity)) - Decimal(m_min_qty)) % Decimal(m_step_size) != 0:
            msg["MstepSize"] = f"Invalid stepSize"
            r = (Decimal(str(quantity)) - Decimal(m_min_qty)) % Decimal(m_step_size)
            sugg["Mqty"] = float(Decimal(str(quantity)) - r)
            
    if msg != {}:
        print(msg)
        print(sugg)
    
    return msg, sugg
    
    
def place_order(symbol, side, order_type, quantity, price=None, stop_price=None):
    validation1 = validate_order(symbol, quantity, price)
    
    liquidity = analyze_liquidity(symbol)
    validation2 = liquidity["is_liquid"]
    
    if (validation1 == ({}, {})) and (validation2 is True):
        params = {
            'symbol': symbol,
            'side': side,
            'type': order_type,
            'quantity': quantity
        }
        if order_type == "MARKET":
            return binance_post_request('/fapi/v1/order', params)
        
        if order_type == "LIMIT":
            params['price'] = price
            params['stopPrice'] = stop_price
            
    else:
        return {"code" : 2, "msg" : liquidity}
        
# ---------------------------------------------------------  End Order ----------------------------------


