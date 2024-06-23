import os
import joblib
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline



def compute_daily_volatility(price_series, span=100):
    returns = price_series.pct_change()
    volatility = returns.ewm(span=span).std()
    return volatility



class ReturnFeature(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X['return'] = X['close'].pct_change()
        X.columns = X.columns.astype(str)
        return X

class SMACalculator(BaseEstimator, TransformerMixin):
    def __init__(self, window):
        self.window = window

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X[f'SMA_{self.window}'] = X['close'].rolling(window=self.window).mean()
        X.columns = X.columns.astype(str)
        return X

class RSICalculator(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        delta = X['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        X['RSI'] = 100 - (100 / (1 + rs))
        X.columns = X.columns.astype(str)
        return X

class MACDCalculator(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        exp1 = X['close'].ewm(span=12, adjust=False).mean()
        exp2 = X['close'].ewm(span=26, adjust=False).mean()
        X['MACD'] = exp1 - exp2
        X['Signal_line'] = X['MACD'].ewm(span=9, adjust=False).mean()
        X.columns = X.columns.astype(str)
        return X

class HighLowRangeCalculator(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X['High_Low_Range'] = X['high'] - X['low']
        X.columns = X.columns.astype(str)
        return X

class OBVCalculator(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        obv = (np.sign(X['close'].diff()) * X['volume']).fillna(0).cumsum()
        X['OBV'] = obv
        X.columns = X.columns.astype(str)
        return X

class DropNaTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X.dropna(inplace=True)
        X.columns = X.columns.astype(str)
        return X

class ScalerWrapper(BaseEstimator, TransformerMixin):
    def __init__(self, scaler):
        self.scaler = scaler

    def fit(self, X, y=None):
        self.scaler.fit(X)
        self.index = X.index
        self.columns = X.columns
        return self

    def transform(self, X):
        X_scaled = self.scaler.transform(X)
        return pd.DataFrame(X_scaled, index=self.index, columns=self.columns)


# Définir et exporter le pipeline
def get_pipeline():
    return Pipeline([
    ('return_feature', ReturnFeature()),
    ('sma_10', SMACalculator(window=10)),
    ('sma_20', SMACalculator(window=20)),
    ('rsi', RSICalculator()),
    ('macd', MACDCalculator()),
    ('high_low_range', HighLowRangeCalculator()),
    ('obv', OBVCalculator()),
    ('dropna', DropNaTransformer()),
    ('standard_scaler', ScalerWrapper(StandardScaler()))
])


path = r"C:\Users\Dell\Desktop\CedAlgo\C-Syst\system\decision\strategies"
path = os.path.join(path, "fpipeline.pkl")
def save_pipeline(filename=path):
    pipeline = get_pipeline()
    joblib.dump(pipeline, filename)


