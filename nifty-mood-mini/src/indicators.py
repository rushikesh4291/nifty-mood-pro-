import pandas as pd
import numpy as np

def rsi(series: pd.Series, period: int = 14) -> pd.Series:
    delta = series.diff()
    gain = np.where(delta > 0, delta, 0.0)
    loss = np.where(delta < 0, -delta, 0.0)
    gain_ema = pd.Series(gain, index=series.index).ewm(alpha=1/period, adjust=False).mean()
    loss_ema = pd.Series(loss, index=series.index).ewm(alpha=1/period, adjust=False).mean()
    rs = gain_ema / (loss_ema.replace(0, np.nan))
    rsi = 100 - (100 / (1 + rs))
    return rsi.fillna(method="bfill").clip(0, 100)

def anchored_vwap(df: pd.DataFrame, anchor_mask: pd.Series) -> pd.Series:
    """
    Daily anchored VWAP using Close*Volume from the most recent anchor row forward.
    anchor_mask: boolean Series where True marks an anchor (e.g., month start / week start)
    """
    # Create a group id that increments at each anchor
    group_id = anchor_mask.cumsum()
    pv = df["Close"] * df["Volume"]
    vwap = pv.groupby(group_id).cumsum() / df["Volume"].groupby(group_id).cumsum()
    return vwap

def zscore(series: pd.Series, window: int = 20) -> pd.Series:
    mean = series.rolling(window).mean()
    std = series.rolling(window).std()
    return (series - mean) / std

def rolling_corr(a: pd.Series, b: pd.Series, window: int = 20) -> pd.Series:
    return a.rolling(window).corr(b)
