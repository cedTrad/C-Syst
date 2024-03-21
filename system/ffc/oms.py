from api.Binance.order import OrderAPIBinance

class PaperOrder:
    
    def __init__(self, symbol=""):
        self.symbol = symbol
    
    def place_order(self, symbol, price, quantity, side):
        quantity = abs(quantity)
        order = {
            'symbol' : symbol,
            'quantity' : quantity,
            'side' : side
        }
        if side == "BUY":
            return quantity
        elif side == "SELL":
            return (-1)*quantity

    
    def open_long(self, asset, price, quantity):
        qty = self.place_order(asset.symbol, price, quantity, side = "BUY")
        asset.type = "LONG"
        asset.position = 1
        asset.update(quantity = qty, price = price)
        #return asset
    
    def close_long(self, asset, price):
        qty = self.place_order(asset.symbol, price, quantity = asset.quantity, side = "SELL")
        asset.position = 0
        asset.update(quantity = qty, price = price)
        asset.type = "None"
        #return asset
        
    def open_short(self, asset, price, quantity):
        qty = self.place_order(asset.symbol, price, quantity, side = "SELL")
        asset.type = "SHORT"
        asset.position = -1
        asset.update(quantity = qty, price = price)
        #return asset
    
    def close_short(self, asset, price):
        qty = self.place_order(asset.symbol, price, quantity = asset.quantity, side = "BUY")
        asset.position = 0
        asset.update(quantity = qty, price = price)
        asset.type = "None"
        #return asset
    
    def resizing_order(self, asset, order):
        asset =  self.order.open_short(asset=asset, price=order["price"], quantity=order["quantity"])
        #return asset
        
    def order_limit(self, asset, order):
        asset =  self.order.open_short(asset=asset, price=order["price"], quantity=order["quantity"])
        #return asset
    
    

class OMS:
    
    def __init__(self, paper_mode = True):
        if paper_mode:
            self.order = PaperOrder()
        else:
            self.order = OrderAPIBinance
        self.long = []
        self.short = []
        
        self.market = []
        self.limit = []
    
        
    