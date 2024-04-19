from .decision.signal import Signal
from .decision.risk_manager import RiskManager
from .decision.transition import Transition


class Politic:
    
    def __init__(self, capital : float):
        self.init_capital = capital
        self.signal = Signal()
        self.riskmanager = RiskManager(capital)


    def select_rule(self, policy_name):
        self.policy_name = policy_name

    
    def signal_policy(self, signal):
        return signal

    
    def update_signal_params(self, params):
        self.params = params
  
    
    def update_risk_params(self, floor = 0.2):
        #self.risk_params = params
        self.riskmanager.config(floor=floor) # update_risk_params
        self.riskmanager.set_stop_loss()
    
    
    
    def signal_processing(self, batchData):
        self.signal.sets(batchData)
        self.rule = self.signal.rules.get(self.policy_name)
        if self.rule is None:
            raise Exception("Policy name incorrect")
        
        self.rule.update_params(self.params)
        
        points = self.rule.run()
        signal = self.signal_policy(points)
        return signal
    
    
    def get_post_metric(self, metrics):
        self.riskmanager.get_current_capital(metrics["capital"])
    
    
    def risk_policy(self, available_amount, current_status):
        self.riskmanager.config(floor=0.2) # update_risk_params
        self.riskmanager.set_stop_loss()
        risk_value, resize = self.riskmanager.update_risk()
        
        amount = available_amount
        return amount
    
    
    
    def perform(self, batchData, portfolio, current_asset_position):
        capital, available_amount = portfolio["capital"], portfolio["available_value"]
        
        self.get_post_metric(portfolio)
        
        signalAction = {}
        riskAction = {}
        
        price = batchData.iloc[-1]["close"]
        signal = self.signal_processing(batchData)
        
        sl = False
        tp = False
        
        canOpenPosition, sideIn = Transition(signal, current_asset_position).get_in()
        canClosePosition, sideOut = Transition(signal, current_asset_position).get_out()
        skip, _ = Transition(signal, current_asset_position).skip()
        resize = 0
        if canOpenPosition:
            signalAction.update({"state" : sideIn + (sl, tp)})
            leverage = 1
            amount = self.risk_policy(available_amount = available_amount, current_status="Open")
            quantity = amount / price
            riskAction.update({"amount" : amount, "quantity" : quantity, "leverage" : leverage})
        
        elif canClosePosition:
            signalAction.update({"state" : sideOut + (sl, tp)})
        
        else:
            signalAction.update({"state" : ("-", signal, sl, tp)})
            
        return signalAction, riskAction

    
  
  