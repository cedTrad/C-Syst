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
        self.signal_params = params
      
    def update_risk_params(self, session_params = {"floor":0.2}):
        self.session_params = session_params

    
    def signal_processing(self, batchData):
        self.signal.sets(batchData)
        self.rule = self.signal.rules.get(self.policy_name)
        if self.rule is None:
            raise Exception("Policy name incorrect")
        
        self.rule.update_params(self.signal_params)
        
        points = self.rule.run()
        signal = self.signal_policy(points)
        return signal
    
    
    def risk_policy(self, portfolio, current_status):
        current_capital = portfolio["capital"]
        available_amount = portfolio["available_value"]
        self.riskmanager.config_session_risk(self.session_params)
        self.riskmanager.actuator(current_capital)
        
        amount = available_amount
        return amount
    
    
    def perform(self, batchData, portfolio, current_asset_position, session_state):
        capital, available_amount = portfolio["capital"], portfolio["available_value"]
        
        signalAction = {}
        riskAction = {}
        
        price = batchData.iloc[-1]["close"]
        signal = self.signal_processing(batchData)
        
        sl = False
        tp = False
        
        canOpenPosition, sideIn = Transition(signal, current_asset_position, session_state).get_in()
        canClosePosition, sideOut = Transition(signal, current_asset_position, session_state).get_out()
        skip, _ = Transition(signal, current_asset_position, session_state).skip()
        canCloseSession, sessionOut = Transition(signal, current_asset_position, session_state).get_out_session()
        resize = 0
        
        if canCloseSession:
            signalAction.update({"state" : sessionOut + (sl, tp)})
        
        if canOpenPosition:
            signalAction.update({"state" : sideIn + (sl, tp)})
            leverage = 1
            amount = self.risk_policy(portfolio=portfolio, current_status="Open")
            quantity = amount / price
            riskAction.update({"amount" : amount, "quantity" : quantity, "leverage" : leverage})
        
        elif canClosePosition:
            signalAction.update({"state" : sideOut + (sl, tp)})
        
        else:
            signalAction.update({"state" : ("-", signal, sl, tp)})
            
        return signalAction, riskAction

    
  
  