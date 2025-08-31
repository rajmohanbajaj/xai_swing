import os
import pandas as pd
import numpy as np
import yfinance as yf
from ta.trend import SMAIndicator, EMAIndicator, ADXIndicator, MACD
from ta.momentum import RSIIndicator, StochasticOscillator
from ta.volatility import BollingerBands
from dataclasses import dataclass

@dataclass
class DataBundle:
    df: pd.DataFrame
    features: list

def fetch_and_engineer(ticker: str, start: str, end: str, cache_csv: str, use_pct_returns: bool=True) -> DataBundle:
    cache_path = cache_csv.format(ticker=ticker.replace("^",""))
    if os.path.exists(cache_path):
        # Read cached CSV, using first row as headers, skipping ticker and empty rows
        df = pd.read_csv(cache_path, header=0, skiprows=[1,2])
        # The first column is actually the date, so rename it
        df = df.rename(columns={"Price": "Date"})
        df["Date"] = pd.to_datetime(df["Date"])
        df = df.set_index("Date")
    else:
        df = yf.download(ticker, start=start, end=end, auto_adjust=True)
        df.index.name = "Date"
        os.makedirs(os.path.dirname(cache_path), exist_ok=True)
        df.to_csv(cache_path)

    # Basic sanity
    df = df.dropna().copy()
    
    # Handle multi-level columns from yfinance
    if isinstance(df.columns, pd.MultiIndex):
        # Flatten multi-level columns
        df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]
    
    df = df.rename(columns={"Open":"open","High":"high","Low":"low","Close":"close","Volume":"volume"})

    # Ensure we have 1D Series for technical indicators
    close_series = df["close"].astype(float)
    high_series = df["high"].astype(float)
    low_series = df["low"].astype(float)
    volume_series = df["volume"].astype(float)

    # Indicators (keep names readable) - ensure 1D Series
    df["sma10"] = SMAIndicator(close_series, window=10).sma_indicator()
    df["sma20"] = SMAIndicator(close_series, window=20).sma_indicator()
    df["sma50"] = SMAIndicator(close_series, window=50).sma_indicator()
    df["sma200"] = SMAIndicator(close_series, window=200).sma_indicator()

    df["ema20"] = EMAIndicator(close_series, window=20).ema_indicator()
    df["ema50"] = EMAIndicator(close_series, window=50).ema_indicator()

    adx = ADXIndicator(high_series, low_series, close_series, window=14)
    df["adx"] = adx.adx()

    rsi = RSIIndicator(close_series, window=14)
    df["rsi14"] = rsi.rsi()

    macd = MACD(close_series, window_slow=26, window_fast=12, window_sign=9)
    df["macd"] = macd.macd()
    df["macd_sig"] = macd.macd_signal()

    stoch = StochasticOscillator(high_series, low_series, close_series, window=14, smooth_window=3)
    df["stoch_k"] = stoch.stoch()
    df["stoch_d"] = stoch.stoch_signal()

    bb = BollingerBands(close_series, window=20, window_dev=2)
    df["bb_high"] = bb.bollinger_hband()
    df["bb_low"]  = bb.bollinger_lband()
    df["bb_bw"]   = (df["bb_high"] - df["bb_low"]) / df["close"]

    # Returns and volatility
    df["ret1"] = df["close"].pct_change()
    df["vol_roll"] = df["ret1"].rolling(20).std()

    # Drop warmup NaNs
    df = df.dropna().copy()

    # Feature list
    features = ["close","volume",
                "sma10","sma20","sma50","sma200",
                "ema20","ema50",
                "adx",
                "rsi14",
                "macd","macd_sig",
                "stoch_k","stoch_d",
                "bb_bw",
                "vol_roll","ret1"]

    # Optionally convert price to pct-change feature for scale stability
    if use_pct_returns:
        df["close_norm"] = df["close"].pct_change().fillna(0.0)
        features = ["close_norm","volume","sma10","sma20","sma50","sma200",
                    "ema20","ema50","adx","rsi14","macd","macd_sig",
                    "stoch_k","stoch_d","bb_bw","vol_roll","ret1"]

    return DataBundle(df=df, features=features)
