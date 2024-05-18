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
        
        leverage = 1
        amount = available_amount
        return amount, leverage
    
    
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
            amount, leverage = self.risk_policy(portfolio=portfolio, current_status="Open")
            quantity = amount / price
            riskAction.update({"amount" : amount, "quantity" : quantity, "leverage" : leverage})
        
        elif canClosePosition:
            signalAction.update({"state" : sideOut + (sl, tp)})
        
        else:
            signalAction.update({"state" : ("-", signal, sl, tp)})
            
        return signalAction, riskAction

    
  
# ----- ------------------

from .decision.signal import Signal
from .decision.risk_manager import RiskManager
from .decision.transition import Transition


class Politic:
    
    def __init__(self, capital: float):
        """
        Initialize the Politic class with initial capital.
        
        Parameters:
        - capital (float): Initial capital for the risk manager.
        """
        self.init_capital = capital
        self.signal = Signal()
        self.riskmanager = RiskManager(capital)
        self.policy_name = None
        self.signal_params = {}
        self.session_params = {"floor": 0.2}

    def select_rule(self, policy_name: str):
        """
        Select the trading rule by its name.
        
        Parameters:
        - policy_name (str): The name of the policy to be used.
        """
        self.policy_name = policy_name

    def signal_policy(self, signal):
        """
        Process and return the signal as is. Can be overridden for more complex signal processing.
        
        Parameters:
        - signal: The signal to be processed.
        
        Returns:
        - The processed signal.
        """
        return signal

    def update_signal_params(self, params: dict):
        """
        Update the parameters for the signal processing.
        
        Parameters:
        - params (dict): The parameters to be updated for the signal processing.
        """
        self.signal_params = params

    def update_risk_params(self, session_params: dict = {"floor": 0.2}):
        """
        Update the parameters for the risk manager.
        
        Parameters:
        - session_params (dict): The parameters for the session risk management.
        """
        self.session_params = session_params

    def signal_processing(self, batchData):
        """
        Process the batch data to generate signals.
        
        Parameters:
        - batchData: The batch data to be processed.
        
        Returns:
        - signal: The processed signal.
        
        Raises:
        - Exception: If the policy name is incorrect.
        """
        self.signal.sets(batchData)
        self.rule = self.signal.rules.get(self.policy_name)
        if self.rule is None:
            raise Exception("Policy name incorrect")
        
        self.rule.update_params(self.signal_params)
        points = self.rule.run()
        signal = self.signal_policy(points)
        return signal

    def risk_policy(self, portfolio, current_status):
        """
        Determine the risk policy based on the portfolio and current status.
        
        Parameters:
        - portfolio: The current state of the portfolio.
        - current_status: The current status of the asset.
        
        Returns:
        - amount (float): The amount to be used for the position.
        - leverage (float): The leverage to be used.
        """
        current_capital = portfolio["capital"]
        available_amount = portfolio["available_value"]
        self.riskmanager.config_session_risk(self.session_params)
        self.riskmanager.actuator(current_capital)
        
        leverage = 1
        amount = available_amount
        return amount, leverage

    def make_decision(self, batchData, portfolio, current_asset_position, session_state):
        """
        Perform the policy action based on the given data and portfolio state.
        
        Parameters:
        - batchData: The batch data containing market information.
        - portfolio: The current state of the portfolio.
        - current_asset_position: The current position of the asset.
        - session_state: The current state of the session.
        
        Returns:
        - signalAction (dict): The action to be performed based on the signal.
        - riskAction (dict): The risk-related action to be performed.
        """
        signalAction = {}
        riskAction = {}
        
        price = batchData.iloc[-1]["close"]
        signal = self.signal_processing(batchData)
        
        sl = False
        tp = False
        
        transition = Transition(signal, current_asset_position, session_state)
        
        canOpenPosition, sideIn = transition.get_in()
        canClosePosition, sideOut = transition.get_out()
        skip, _ = transition.skip()
        canCloseSession, sessionOut = transition.get_out_session()
        
        if canCloseSession:
            signalAction["state"] = sessionOut + (sl, tp)
        
        if canOpenPosition:
            signalAction["state"] = sideIn + (sl, tp)
            amount, leverage = self.risk_policy(portfolio, current_status="Open")
            quantity = amount / price
            riskAction.update({"amount": amount, "quantity": quantity, "leverage": leverage})
        
        elif canClosePosition:
            signalAction["state"] = sideOut + (sl, tp)
        
        else:
            signalAction["state"] = ("-", signal, sl, tp)
        
        return signalAction, riskAction
