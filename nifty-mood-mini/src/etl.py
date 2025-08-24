import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
OUT_DIR = Path(__file__).resolve().parents[1] / "out"

def fetch_ohlcv(ticker: str, period: str = "1y", interval: str = "1d") -> pd.DataFrame:
    df = yf.Ticker(ticker).history(period=period, interval=interval, auto_adjust=False)
    if df.empty and ticker == "^NSEI":
        # Fallback to NIFTYBEES as proxy if Yahoo index fails locally
        df = yf.Ticker("NIFTYBEES.NS").history(period=period, interval=interval, auto_adjust=False)
    df = df.reset_index().rename(columns=str).rename(columns={"Date":"date"})
    df["date"] = pd.to_datetime(df["date"]).dt.date
    df = df.rename(columns={"Open":"Open", "High":"High", "Low":"Low", "Close":"Close", "Volume":"Volume"})
    return df[["date","Open","High","Low","Close","Volume"]]

def load_fii_dii() -> pd.DataFrame:
    path = DATA_DIR / "fii_dii_sample.csv"
    df = pd.read_csv(path, parse_dates=["date"])
    df["date"] = df["date"].dt.date
    return df

def merge_all() -> pd.DataFrame:
    nifty = fetch_ohlcv("^NSEI")
    banknifty = fetch_ohlcv("^NSEBANK")
    fii_dii = load_fii_dii()
    df = nifty.merge(banknifty.add_prefix("bn_"), left_on="date", right_on="bn_date", how="left")
    df = df.drop(columns=["bn_date"])
    df = df.merge(fii_dii, on="date", how="left")
    return df.sort_values("date").reset_index(drop=True)
