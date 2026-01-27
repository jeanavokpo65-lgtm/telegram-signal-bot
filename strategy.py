import pandas as pd
import numpy as np

# ===== INDICATEURS =====

def calculate_ema(series, period):
    return series.ewm(span=period, adjust=False).mean()


def calculate_vwap(df):
    tp = (df["high"] + df["low"] + df["close"]) / 3
    return (tp * df["volume"]).cumsum() / df["volume"].cumsum()


def calculate_atr(df, period=14):
    hl = df["high"] - df["low"]
    hc = (df["high"] - df["close"].shift()).abs()
    lc = (df["low"] - df["close"].shift()).abs()
    tr = pd.concat([hl, hc, lc], axis=1).max(axis=1)
    return tr.rolling(period).mean()


# ===== FILTRE SESSION =====

def in_session(timestamp):
    hour = timestamp.hour
    return (8 <= hour < 11) or (13 <= hour < 16)


# ===== STRATÉGIE =====

def check_signal(df):
    df = df.copy()

    df["ema20"] = calculate_ema(df["close"], 20)
    df["ema50"] = calculate_ema(df["close"], 50)
    df["vwap"] = calculate_vwap(df)
    df["atr"] = calculate_atr(df)
    df["vol_ma"] = df["volume"].rolling(20).mean()

    last = df.iloc[-1]

    close = last["close"]
    ema20 = last["ema20"]
    ema50 = last["ema50"]
    vwap = last["vwap"]
    atr = last["atr"]
    volume = last["volume"]
    vol_ma = last["vol_ma"]
    timestamp = pd.to_datetime(last["time"], utc=True)

    # filtres
    if not in_session(timestamp):
        return "NO TRADE"
    if volume <= vol_ma:
        return "NO TRADE"
    if atr <= close * 0.0015:
        return "NO TRADE"
    if abs(ema20 - ema50) / close < 0.0008:
        return "NO TRADE"

    pullback = abs(close - ema20) / close < 0.0015

    if close > ema50 and ema20 > ema50 and close >= vwap and pullback:
        return "BUY"

    if close < ema50 and ema20 < ema50 and close <= vwap and pullback:
        return "SELL"

    return "NO TRADE"


def get_tp_sl(entry, side):
    if side == "BUY":
        return entry * 1.004, entry * 0.998
    else:
        return entry * 0.996, entry * 1.002
