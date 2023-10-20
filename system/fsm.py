from .oms import OMS


STATE = [
    ("Open", "LONG", "TP", "SL"), ("-", "LONG", "TP", "SL"), ("Close", "LONG", "TP", "SL"),
    ("Open", "SHORT", "TP", "SL"), ("-", "SHORT", "TP", "SL"), ("Close", "SHORT", "TP", "SL"),
    ("Resize", "LONG"), ("Resize", "SHORT"), ("-", None)
]


class FSM:
    
    def __init__(self, current_state, next_state, signal_action, risk_action, test_state):
        self.current_state = current_state
        self.next_state = next_state
        self.signal_action = signal_action
        self.risk_action = risk_action
        self.oms = OMS(test = test_state)
        
        
    def actuator(self, portfolio, asset, price):
        if self.signal_action["state"][:2] == ("Open", "LONG"):
            response = self.oms.order.open_long(asset, price, quantity = self.risk_action["quantity"])
            portfolio.rebalance(amount = self.risk_action["amount"])
            
        elif self.signal_action["state"][:2] == ("Close", "LONG"):
            response = self.oms.order.close_long(asset, price)
        
        elif self.signal_action["state"][:2] == ("Open", "SHORT"):
            response = self.oms.order.open_short(asset, price = price, quantity = self.risk_action["quantity"])
            portfolio.rebalance(amount = self.risk_action["amount"])
        
        elif self.signal_action["state"][:2] == ("Close", "SHORT"):
            response = self.oms.order.close_short(asset, price = price)
        
        elif self.signal_action["state"][:2] == ("Resize", "LONG"):
            "place_order()"
        
        elif self.signal_action["state"][:2] == ("Resize", "SHORT"):
            "place_order()"
        
        elif self.signal_action["state"][0] == "-":
            asset.update(price = price, state = self.signal_action["state"])
            
    
    
    def callback_actuator(self):
        ""
    
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
                self.callback_actuator()
        return sucess



