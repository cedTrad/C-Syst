import pandas as pd
import numpy as np
import ta
from arch import arch_model


def sma(data, window):
    sma = ta.trend.SMAIndicator(close = data.close, window = window)
    return sma.sma_indicator()


def ema(data, period = 4):
    ema = ta.trend.EMAIndicator(data.close, period)
    return ema.ema_indicator()


def lag_returns(data, lag):
    X = data.close.pct_change(lag)
    X.name = f"ret_{lag}"
    return X


def rsi(data, period):
    RSI = ta.momentum.RSIIndicator(data.close, period)
    return RSI.rsi()

    
def stochastic_oscillator(data, k_period, d_period):
    S_O = ta.momentum.StochasticOscillator(high = data.high, low = data.low,
                                     close = data.close,
                                     window = k_period,
                                     smooth_window = d_period)
    K = S_O.stoch()
    D = S_O.stoch_signal()
    return pd.concat([K, D], axis = 1)



def aroon(data, period):
    """
    Return : Aroon_up, Aroon_down
    """
    Aroon_indicator = ta.trend.AroonIndicator(close = data.close, window=period)
    Aroon_up = Aroon_indicator.aroon_up()
    Aroon_down = Aroon_indicator.aroon_down()
    return pd.concat([Aroon_up, Aroon_down], axis = 1)



def n_day_up(data, period):
    data = data.copy()
    data['return'] = data['close'].pct_change()
    return data['return'].rolling(period).apply(lambda x : np.sum(np.where(x>0, 1, 0))*100/period)


# ATR
def atr(data, window): 
    Atr = ta.volatility.AverageTrueRange(high = data.high, low = data.low,
                                         close = data.close, window = window)
    return Atr.average_true_range()


# Bande de bollingers
def bande_bollingers(data, window, wind_dev):
    B_B = ta.volatility.BollingerBands(close = data.close, window = window, 
                                       window_dev = wind_dev)
    B_B.bollinger_hband_indicator()
    """ return 1 or 0 : 1 if close is higher than bollinger_hband, else it return 0 """    
    B_B.bollinger_lband_indicator()
    """ return 1 or 0 : 1 if close is lower than bollinger_lband, else it return 0 """
    
    B_B.bollinger_pband()
    B_B.bollinger_wband()
    return pd.concat([B_B.bollinger_hband(), B_B.bollinger_lband(), B_B.bollinger_mavg()], axis = 1)




# ADX
def adx(data, window):
    """ 
    Return : ADX.adx , ADX.adx_up, ADX.adx_down
    """
    ADX = ta.trend.ADXIndicator(high = data.high, low = data.low,
                                close = data.close, window =  window)
    
    return pd.concat([ADX.adx(), ADX.adx_neg(), ADX.adx_pos()], axis = 1)



# SAR
def sar(data, step = 0.2, max_step = 0.2):
    """ 
    Return : SAR.psar, : SAR.psar_up, : SAR.psar_down 
    """
    SAR = ta.trend.PSARIndicator(high = data.high, low = data.low, close = data.close,
                                 step = step, max_step = max_step)
    SAR.psar()
    SAR.psar_down()              # down trend value
    SAR.psar_down_indicator()    # down trend value indicator

    SAR.psar_up()       # up trend value
    SAR.psar_up_indicator() # up trend value indicator
    
    return pd.concat([SAR.psar(), SAR.psar_up_indicator(), SAR.psar_down_indicator()], axis = 1)



def macd(data, slow , fast, signal):
    MACD = ta.trend.MACD(close = data.close , window_slow = slow, window_fast = fast,
                         window_sign = signal)
    return pd.concat([MACD.macd() , MACD.macd_diff(), MACD.macd_signal()], axis = 1)
    


def GARCH(ret : pd.Series):
    ret = ret.dropna()
    model = arch_model(ret, mean = "Zero", vol = "GARCH", p=1, q=1)
    res = model.fit(update_freq = 5)
    return res.conditional_volatility
    
