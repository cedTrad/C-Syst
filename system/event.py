import pandas as pd
from dataEngine.data import connect_db


class MarketEvent:
    """
    Classe pour générer des événements de marché en fonction des données historiques.
    """

    def __init__(self, size=45, start="2023", end="2023", interval="1d"):
        """
        Initialise un événement de marché.

        :param size: Taille de la fenêtre glissante.
        :param start: Date de début des données.
        :param end: Date de fin des données.
        :param interval: Intervalle de temps pour les données.
        """
        self.size = size
        self.start = start
        self.end = end
        self.db = connect_db(name="database", interval=interval)

    def gen_data(self, symbol):
        """
        Génère des batchs de données pour un symbole donné.

        :param symbol: Symbole de l'actif.
        :return: Générateur de batchs de données.
        """
        i = 0
        data = self.db.get_data(symbol, start=self.start, end=self.end)
        while True:
            batch = data.iloc[i: i + self.size]
            if len(batch) == self.size:
                yield batch
                i += 1
            else:
                break

    def get_data(self, symbol):
        """
        Récupère les données pour un symbole donné.

        :param symbol: Symbole de l'actif.
        :return: Générateur de batchs de données.
        """
        return self.gen_data(symbol)


class PostEvent:
    """
    Classe pour gérer les événements post-marché tels que les enregistrements de trades et de portefeuilles.
    """

    def __init__(self):
        """
        Initialise un PostEvent.
        """
        self.portfolioData = pd.DataFrame()
        self.metricData = pd.DataFrame()
        self.tradeData = pd.DataFrame()
        self.sessionData = pd.DataFrame()

    def add_trade_line(self, agent_id, date, price, asset, session_id):
        """
        Ajoute une ligne de trade à la DataFrame des trades.

        :param agent_id: ID de l'agent.
        :param date: Date du trade.
        :param price: Prix du trade.
        :param asset: Objet représentant l'actif.
        :param session_id: ID de la session.
        """
        line = {
            'agentId': agent_id, 'date': date, 'price': price,
            'quantity': asset.quantity, 'position': asset.position,
            'side': asset.type, 'state': str(asset.state),
            'in_value': asset.in_value, 'out_value': asset.out_value,
            'value': asset.value, 'pnl': asset.pnl, 'pnl_pct': asset.pnl_pct,
            'symbol': asset.symbol, "session": session_id
        }
        add = pd.DataFrame([line], index=[date])
        self.tradeData = pd.concat([self.tradeData, add], ignore_index=True)

    def add_portfolio_line(self, agent_id, date, symbol, portfolio, session_id):
        """
        Ajoute une ligne de portefeuille à la DataFrame des portefeuilles.

        :param agent_id: ID de l'agent.
        :param date: Date de l'enregistrement.
        :param symbol: Symbole de l'actif.
        :param portfolio: Objet représentant le portefeuille.
        :param session_id: ID de la session.
        """
        line = {
            'agentId': agent_id, 'date': date,
            'risk_value': portfolio.risk_value, 'available_value': portfolio.available_value,
            'capital': portfolio.capital, "symbol": symbol, "session": session_id
        }
        add = pd.DataFrame([line], index=[date])
        self.portfolioData = pd.concat([self.portfolioData, add], ignore_index=True)

    def add_metrics_line(self, date, line):
        """
        Ajoute une ligne de métriques à la DataFrame des métriques.

        :param date: Date de l'enregistrement.
        :param line: Dictionnaire représentant les métriques.
        """
        add = pd.DataFrame([line], index=[date])
        self.metricData = pd.concat([self.metricData, add], ignore_index=True)

    def add_data(self, agent_id, date, price, asset, portfolio, session_id):
        """
        Ajoute des données de trade et de portefeuille.

        :param agent_id: ID de l'agent.
        :param date: Date de l'enregistrement.
        :param price: Prix du trade.
        :param asset: Objet représentant l'actif.
        :param portfolio: Objet représentant le portefeuille.
        :param session_id: ID de la session.
        """
        self.add_trade_line(agent_id, date, price, asset, session_id)
        self.add_portfolio_line(agent_id, date, asset.symbol, portfolio, session_id)

    def add_session(self, session):
        """
        Ajoute une session à la DataFrame des sessions.

        :param session: Dictionnaire représentant une session.
        """
        add = pd.DataFrame([session], index=[1])
        self.sessionData = pd.concat([self.sessionData, add], ignore_index=True)
