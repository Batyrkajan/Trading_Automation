import yfinance as yf
import pandas_ta as ta
import pandas as pd

def get_realtime_data(ticker):
    """Fetches real-time data for a given ticker."""
    data = yf.download(ticker, period="1d", interval="1m")
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = ['_'.join(col).strip() for col in data.columns.values]
    data.columns = data.columns.str.lower()
    return data

def calculate_indicators(data):
    """Calculates technical indicators using pandas-ta."""
    data.ta.rsi(append=True)
    data.ta.macd(append=True)
    data.ta.adx(append=True)
    data.ta.atr(append=True)
    data.ta.bbands(append=True)
    data.ta.cci(append=True)
    data.ta.ichimoku(append=True)
    data.ta.sma(length=20, append=True)
    data.ta.sma(length=50, append=True)
    data.ta.sma(length=200, append=True)
    data.ta.ema(length=20, append=True)
    data.ta.ema(length=50, append=True)
    data.ta.ema(length=200, append=True)
    data.ta.obv(append=True)
    data.ta.psar(append=True)
    data.ta.stoch(append=True)
    return data
