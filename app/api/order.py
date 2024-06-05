from .base import Base
from .validation import Filter, Liquidity

class Order(Base):
    
    def __init__(self, symbol):
        super().__init__()
        self.symbol = symbol
        self.qty = 0
        self.filter = Filter(symbol)
        self.liquidity = Liquidity(symbol)
        
    def update_leverage(self, leverage):
        params = {
            'symbol' : self.symbol,
            'leverage' : leverage
        }
        return self.binance_post_request('/fapi/v1/leverage', params)
        
    def place_order(self, side, order_type, quantity=None, price=None, stop_price=None):
        validation1 = self.filter.validate_order(quantity, side, price)
        
        liquidity = self.liquidity.analyze_liquidity()
        validation2 = liquidity["is_liquid"]
        
        if (validation1 == ({}, {})) and (validation2 is True):
            params = {
                'symbol': self.symbol,
                'side': side,
                'type': order_type
            }
            if order_type == "MARKET":
                params['quantity'] = quantity
                return self.binance_post_request('/fapi/v1/order', params)
            
            if order_type == "LIMIT":
                params['quantity'] = quantity
                params['price'] = price
                return self.binance_post_request('/fapi/v1/order', params)
                
        else:
            return {"code" : 2, "msg" : liquidity}
    
    
    
    def place_stop_loss_take_profit(self, side, quantity, stop_loss_price, take_profit_price):
        mark_price = float(self.get_mark_price(self.symbol)['markPrice'])
        if stop_loss_price >= mark_price or take_profit_price <= mark_price:
            return {"code": -1, "msg": "Invalid stop loss or take profit prices"}
        
        # Place StopLossOrder
        stop_loss_side = 'SELL' if side == 'BUY' else 'BUY'
        stop_loss_order_params = {
            'symbol': self.symbol,
            'side': stop_loss_side,
            'type': 'STOP_MARKET',
            'quantity': quantity,
            'stopPrice': stop_loss_price
        }
        stop_loss_order_response = self.binance_post_request('/fapi/v1/order', stop_loss_order_params)
        if 'code' in stop_loss_order_response and stop_loss_order_response['code'] != 200:
            return {"code": stop_loss_order_response['code'], "msg": stop_loss_order_response['msg']}
        
        # Place the take profit order
        take_profit_side = 'SELL' if side == 'BUY' else 'BUY'
        take_profit_order_params = {
            'symbol': self.symbol,
            'side': take_profit_side,
            'type': 'TAKE_PROFIT_MARKET',
            'quantity': quantity,
            'stopPrice': take_profit_price
        }
        take_profit_order_response = self.binance_post_request('/fapi/v1/order', take_profit_order_params)
        if 'code' in take_profit_order_response and take_profit_order_response['code'] != 200:
            return {"code": take_profit_order_response['code'], "msg": take_profit_order_response['msg']}
        
        return stop_loss_order_response, take_profit_order_response
    
    
    def cancel_all_open_orders(self):
        params = {
            'symbol': self.symbol
        }
        response = self.binance_delete_request('/fapi/v1/allOpenOrders', params)
        return response
    
    def reduce_position(self, quantity, side):
        # Déterminer le côté opposé pour réduire la position
        reduce_side = 'SELL' if side == 'BUY' else 'BUY'
        params = {
            'symbol': self.symbol,
            'side': reduce_side,
            'type': 'MARKET',
            'quantity': quantity,
            'reduceOnly': 'true'
        }
        return self.binance_post_request('/fapi/v1/order', params)
    
    def open_long(self, quantity, leverage, stop_loss, take_profit):
        self.qty = quantity
        self.update_leverage(leverage)
        position = self.place_order(side='BUY', order_type='MARKET', quantity=quantity)
        if stop_loss and take_profit:
            protection = self.place_stop_loss_take_profit(side="BUY", quantity=quantity, stop_loss_price=stop_loss, take_profit_price=take_profit)
        msg = []
        if position['status'] == 'NEW':
            msg.append("Order Success")
        if protection[0]['status'] == 'NEW' and protection[1]['status'] == 'NEW':
            msg.append("ST and TP sucess")
        return msg
            
    
    def close_long(self):
        quantity = self.qty
        position = self.place_order(side='SELL', order_type='MARKET', quantity=quantity)
        cancel = self.cancel_all_open_orders()
        return position, cancel
    
    def open_short(self, quantity, leverage, stop_loss, take_profit):
        self.st_qty = quantity
        self.update_leverage(leverage)
        position = self.place_order(side='SELL', order_type='MARKET', quantity=quantity)
        if stop_loss and take_profit:
            protection = self.place_stop_loss_take_profit(side="SELL", quantity=quantity, stop_loss_price=stop_loss, take_profit_price=take_profit)
        msg = []
        if position['status'] == 'NEW':
            msg.append("Order Success")
        if protection[0]['status'] == 'NEW' and protection[1]['status'] == 'NEW':
            msg.append("ST and TP sucess")
        return msg
            
    
    def close_short(self):
        quantity = self.qty
        position = self.place_order(side='BUY', order_type='MARKET', quantity=quantity)
        cancel = self.cancel_all_open_orders()
        return position, cancel
        
    


