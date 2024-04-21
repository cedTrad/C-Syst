import time
from .oms import OMS


ACTION = [
    ("Open", "LONG", "TP", "SL"), ("-", "LONG", "TP", "SL"), ("Close", "LONG", "TP", "SL"),
    ("Open", "SHORT", "TP", "SL"), ("-", "SHORT", "TP", "SL"), ("Close", "SHORT", "TP", "SL"),
    ("Resize", "LONG"), ("Resize", "SHORT"), ("-", None)
]


class FSM:
    
    def __init__(self, current_state, signal_action, risk_action, paper_mode):
        self.current_state = current_state
        
        self.signal_action = signal_action
        self.risk_action = risk_action
        self.oms = OMS(paper_mode = paper_mode)
        
        
    def actuator(self, portfolio, asset, price):
        next_asset_side = self.signal_action["state"]
        asset.update_state(state = next_asset_side)
        
        if self.signal_action["state"][:2] == ("Open", "LONG"):
            response = self.oms.order.open_long(asset, price, quantity = self.risk_action["quantity"])
            portfolio.rebalance(amount = self.risk_action["amount"])
            succes = True
            
        elif self.signal_action["state"][:2] == ("Close", "LONG"):
            response = self.oms.order.close_long(asset, price)
            succes = True
        
        # --------------------------------------------------------   ---------
        elif self.signal_action["state"][:2] == ("Open", "SHORT"):
            response = self.oms.order.open_short(asset, price = price, quantity = self.risk_action["quantity"])
            portfolio.rebalance(amount = self.risk_action["amount"])
            succes = True
        
        elif self.signal_action["state"][:2] == ("Close", "SHORT"):
            response = self.oms.order.close_short(asset, price = price)
            succes = True
        
        # --------------------------------------------------------   ---------
        elif self.signal_action["state"][:2] == ("Resize", "LONG"):
            "place_order()"
            succes = True
        
        elif self.signal_action["state"][:2] == ("Resize", "SHORT"):
            "place_order()"
            succes = True
        
        # --------------------------------------------------------   ---------
        elif self.signal_action["state"][0] == "-":
            asset.update(price = price)
            succes = True
        
        # --------------------------------------------------------   ---------
        else:
            print(self.signal_action)
            succes = False
        
        return succes
            
    
    def callback_actuator(self, asset, price, portfolio):
        i = 0
        max = 10
        while True:
            time.sleep(0.5)
            print("retry in 0.5s ... ")
            i += 1
            if i == max:
                break
            self.perform(asset=asset, price=price, portfolio=portfolio)
            
    
    def predicate(self, portfolio, min_amount = 20):
        if "Open" in self.signal_action:
            if self.risk_action.get("amount") <= min_amount:
                return False
            if self.risk_action["amount"] > portfolio.available_value:
                return False
        return True
    
    
    def perform(self, asset, price, portfolio):
        effect = self.predicate(portfolio)
        if effect:
            sucess = self.actuator(portfolio, asset, price)
            if not sucess:
                self.callback_actuator(asset=asset, price=price, portfolio=portfolio)
        return sucess



