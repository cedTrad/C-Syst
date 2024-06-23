from .politic import Politic
from .portfolio_manager import Asset, Portfolio
from .processor import Processor
from .session_manager import SessionManager
from IPython.display import clear_output


class Event:
    """
    Représente un événement de marché avec une date et un prix.
    """
    def __init__(self, date, price):
        self.date = date
        self.price = price


class Agent:
    """
    Représente un agent de trading avec un capital, une politique et un environnement de trading.
    """
    def __init__(self, agentId, capital, env, session_step=50):
        """
        Initialise un nouvel agent de trading.

        :param agentId: Tuple contenant l'ID de l'agent et le symbole de l'actif.
        :param capital: Capital initial de l'agent.
        :param env: Environnement de trading.
        :param session_step: Nombre d'étapes par session.
        """
        self.agentId = agentId
        self.symbol = agentId[1]
        self.init_capital = capital
        self.capital = capital
        self.fitness = []

        self.env = env
        self.env.initialize_portfolio(capital)
        self.post_event = self.env.post_event
        self.gen_data = self.env.market.get_data(self.symbol)
        self.capital = self.env.capital

        self.asset = Asset(self.symbol)
        self.policy = Politic(capital=capital)
        self.processor = Processor(agentId=agentId, db=self.env.market.db, post_event=self.env.post_event)
        self.session = SessionManager(self.env, session_step)

    def get_event(self):
        """
        Génère un événement de marché basé sur les données actuelles.

        :return: Instance de l'événement.
        """
        self.batchData = next(self.gen_data)
        return Event(date=self.batchData.index[-1], price=self.batchData.iloc[-1]["close"])

    def update_policy(self, name, params, session_risk_params):
        """
        Met à jour la politique de l'agent.

        :param name: Nom de la règle de trading.
        :param params: Paramètres du signal.
        :param session_risk_params: Paramètres de risque de la session.
        """
        self.policy.select_rule(name)
        self.policy.update_signal_params(params=params)
        self.policy.update_risk_params(session_params=session_risk_params)

    def act(self, state, session_state):
        """
        Génère les actions de trading basées sur la politique actuelle.

        :param state: État actuel du portefeuille.
        :param session_state: État de la session.
        :return: Tuple contenant les actions de signal et de risque.
        """
        return self.policy.make_decision(batchData=self.batchData, portfolio=state["portfolio"],
                                   current_asset_position=self.asset.position, session_state=session_state)

    def execute(self, state, paper_mode=True):
        """
        Exécute une étape de trading.

        :param state: État actuel du portefeuille.
        :param paper_mode: Mode de simulation.
        :return: Tuple contenant les informations de l'événement, l'état suivant et les actions.
        """
        # Avant l'exécution
        event = self.get_event()
        closeSession, n_session = self.session.actuator()
        signalAction, riskAction = self.act(state, session_state=closeSession)
        if "leverage" in riskAction:
            self.asset.set_leverage(riskAction["leverage"])    
        next_state, reward = self.env.step(self.agentId[0], self.asset, event, signalAction, riskAction, n_session, paper_mode)
        
        # Après l'exécution
        if signalAction["state"][1] in ["LONG", "SHORT"]:
            tradedata = self.post_event.tradeData
            self.session.metrics.actuator(tradedata)
                
        return event, next_state, reward, signalAction, riskAction
    
    
    def run_episode(self):
        """
        Exécute une session complète de trading.
        """
        state = self.env.reset()
        i = 0
        while True:
            try:
                event, next_state, reward, signalAction, riskAction = self.execute(state)
                state = next_state
                i += 1
                
            except StopIteration:
                print(f"Session terminée après {i} itérations.")
                self.processor.run()
                break

    def view_report(self):
        """
        Affiche le rapport de performance.
        """
        self.processor.plot_equity()
        self.processor.plot_session(self.session.rets_dist)


    def learn(self):
        """
        Apprend de l'expérience de trading (méthode à implémenter).
        """
        pass

    
    def get_report(self):
        tradeData = self.post_event.tradeData.copy()
        portfolioData = self.post_event.portfolioData.copy()
        sessionData = self.post_event.sessionData.copy()
        init_capital = self.env.init_capital
        agent_capital = init_capital + tradeData.iloc[-1]["cum_gp"]
        port_capital = portfolioData.iloc[-1]["capital"]
        pnl = tradeData.iloc[-1]["cum_gp"]

        print("Initial Capital:", init_capital)
        print("Agent Capital:", agent_capital)
        print("Portfolio Capital:", port_capital)
        print("PnL:", pnl)
        print("Return : ",((agent_capital/init_capital)-1)*100,"%")
        
        min_expo = sessionData["minExposure"].min()
        max_expo = sessionData["maxExposure"].max()
        print(f"Min exposure : {min_expo}  Max exposure : {max_expo}")
        