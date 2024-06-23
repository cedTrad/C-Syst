from .ffc.fsm import FSM
from .portfolio_manager import PFuture
from .event import MarketEvent, PostEvent


signal_actions = ["Open", "Close", "Resize", "-", None]
risk_actions = ["quantity", "leverage", "closePrice", "sl", "tp"]


class GEnv:
    """
    Classe représentant un environnement global pour plusieurs symboles.
    """

    def __init__(self, symbols, interval, start, end):
        """
        Initialise l'environnement global.

        :param symbols: Liste des symboles à traiter.
        :param interval: Intervalle de temps pour les données.
        :param start: Date de début des données.
        :param end: Date de fin des données.
        """
        self.symbols = symbols
        self.start = start
        self.end = end
        self.post_event = PostEvent()
        self.market = MarketEvent(size=30, start=start, end=end, interval=interval)
        self.metrics = {}

    def initialize_portfolio(self, capital):
        """
        Initialise le portefeuille avec un capital initial.

        :param capital: Capital initial du portefeuille.
        """
        self.init_capital = capital
        self.portfolio = PFuture("Binance", capital)
        for symbol in self.symbols:
            self.portfolio.add_asset(symbol)

    def g_report(self):
        """
        Génère un rapport global.
        """
        # Implémenter le code de génération de rapport ici
        pass


class Env:
    """
    Classe représentant un environnement pour un seul symbole.
    """

    def __init__(self, symbol, interval="1d", start="2023", end="2023"):
        """
        Initialise l'environnement.

        :param symbol: Symbole à traiter.
        :param interval: Intervalle de temps pour les données.
        :param start: Date de début des données.
        :param end: Date de fin des données.
        """
        self.symbol = symbol
        self.start = start
        self.end = end
        self.post_event = PostEvent()
        self.market = MarketEvent(size=50, start=start, end=end, interval=interval)

    def initialize_portfolio(self, capital):
        """
        Initialise le portefeuille avec un capital initial.

        :param capital: Capital initial du portefeuille.
        """
        self.init_capital = capital
        self.portfolio = PFuture("Binance", capital)
        self.portfolio.add_asset(self.symbol)
        self.capital = self.portfolio.capital

    def get_state(self):
        """
        Récupère l'état actuel du portefeuille et des indicateurs.

        :return: Dictionnaire représentant l'état du portefeuille et des indicateurs.
        """
        portfolio = {
            "capital": self.portfolio.capital,
            "risk_value": self.portfolio.risk_value,
            "save_value": self.portfolio.save_value,
            "available_value": self.portfolio.available_value
        }
        indicator = {
            "average": 0, "dist_sl": 0, "profit_factor": 0,
            "win_rate": 0, "drawdown": 0, "recovery": 0
        }
        return {"portfolio": portfolio, "indicator": indicator}

    def execute(self, asset, price, signal_action, risk_action, paper_mode):
        """
        Exécute une action sur un actif donné.

        :param asset: Objet représentant l'actif.
        :param price: Prix actuel de l'actif.
        :param signal_action: Action de signal à effectuer.
        :param risk_action: Action de gestion des risques à effectuer.
        :param paper_mode: Mode de simulation (True pour paper trading).
        """
        current_state = (asset.state, asset.type, asset.tp, asset.sl)
        fsm = FSM(current_state, signal_action, risk_action, paper_mode)
        fsm.perform(asset=asset, price=price, portfolio=self.portfolio)

    def step(self, agent_id, asset, event, signal_action, risk_action, session_id, paper_mode=True):
        """
        Effectue une étape de trading.

        :param agent_id: ID de l'agent.
        :param asset: Objet représentant l'actif.
        :param event: Événement de marché actuel.
        :param signal_action: Action de signal à effectuer.
        :param risk_action: Action de gestion des risques à effectuer.
        :param session_id: ID de la session.
        :param paper_mode: Mode de simulation (True pour paper trading).
        :return: État actuel et récompense.
        """
        reward = 0
        self.execute(asset=asset, price=event.price, signal_action=signal_action, risk_action=risk_action, paper_mode=paper_mode)
        self.portfolio.update(asset=asset)
        self.post_event.add_data(agent_id=agent_id, date=event.date, price=event.price, asset=asset, portfolio=self.portfolio, session_id=session_id)
        state = self.get_state()

        if "Close" in signal_action["state"]:
            reward = asset.pnl

        return state, reward

    def reset(self):
        """
        Réinitialise le portefeuille et l'état.

        :return: État initial.
        """
        self.portfolio.add_asset(self.symbol)
        self.portfolio.clear()
        return self.get_state()
