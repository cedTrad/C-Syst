from .base import Base

import pandas as pd
from decimal import Decimal

class Filter(Base):
    
    def __init__(self, symbol):
        super().__init__()
        self.symbol = symbol
        
    def get_mark_price(self):
        params = {"symbol": self.symbol}
        return self.binance_request('/fapi/v1/premiumIndex', params)
    
    def process_filters(self):
        response = self.get_filters()
        symbol_info = next((item for item in response['symbols'] if item['symbol'] == self.symbol), None)
        if symbol_info:
            filters = {f['filterType']: f for f in symbol_info['filters']}
            return filters
        return None
    
    
    def validate_order(self, quantity, side, price=None):
        filters = self.process_filters()
        if not filters:
            return {'code': -1, 'msg': 'No filters found for the symbol'}
        
        msg = {}
        sugg = {}
        
        # LOT_SIZE
        lot_size = filters.get('LOT_SIZE')
        if lot_size and quantity:
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
            mark_price = self.get_mark_price(self.symbol)['markPrice']
            
            if (side == "BUY") and (price > float(mark_price )*float(multiplierUp)):
                msg["percentPrice"] = f"BUY : Invalid"
            if (side == "SELL") and (price < float(mark_price) * float(multiplierDown)):
                msg["percentPrice"] = f"SELL : Invalid"
                
        
        # MARKET_LOT_SIZE
        market_lot_size = filters.get('MARKET_LOT_SIZE')
        if market_lot_size and quantity:
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
    



class Liquidity(Base):
    
    def __init__(self, symbol):
        super().__init__()
        self.symbol = symbol
        
        
    def get_order_book(self, limit=100):
        params = {
            'symbol': self.symbol,
            'limit': limit
        }
        return self.binance_request('/fapi/v1/depth', params)

    def get_ticker(self):
        params = {
            'symbol': self.symbol
        }
        return self.binance_request('/fapi/v1/ticker/24hr', params)
    
    
    def analyze_liquidity(self):
        order_book = self.get_order_book()
        ticker = self.get_ticker()
        
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
        return {
            'symbol': self.symbol,
            'spread': spread,
            'volume': volume,
            'total_bids': total_bids,
            'total_asks': total_asks,
            'is_liquid': is_liquid,
            'rules': rules
        }