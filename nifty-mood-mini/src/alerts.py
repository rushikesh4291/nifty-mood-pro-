import pandas as pd
import yaml
from pathlib import Path

from .indicators import rsi, anchored_vwap, zscore, rolling_corr

ROOT = Path(__file__).resolve().parents[1]

def compute_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Anchors: start of month/week
    d = pd.to_datetime(df["date"])
    month_anchor = d.dt.is_month_start
    week_anchor = d.dt.weekday == 0  # Monday

    df["avwap_month"] = anchored_vwap(df, month_anchor)
    df["avwap_week"] = anchored_vwap(df, week_anchor)

    df["rsi14"] = rsi(df["Close"], period=14)
    df["vol_z20"] = zscore(df["Volume"], window=20)

    # 20D high/low close
    df["hh_20"] = df["Close"].rolling(20).max()
    df["ll_20"] = df["Close"].rolling(20).min()

    # Correlation with BANKNIFTY close
    if "bn_Close" in df.columns:
        df["corr20_bn"] = rolling_corr(df["Close"], df["bn_Close"], window=20)
    else:
        df["corr20_bn"] = pd.NA

    # FII/DII divergence flags
    df["fii_pos_dii_neg"] = (df["fii_cash_net_cr"] > 0) & (df["dii_cash_net_cr"] < 0)
    df["fii_neg_dii_pos"] = (df["fii_cash_net_cr"] < 0) & (df["dii_cash_net_cr"] > 0)

    return df

def load_rules():
    with open(ROOT / "rules.yaml", "r") as f:
        return yaml.safe_load(f)

def evaluate_rules(df: pd.DataFrame, rules_cfg: dict) -> pd.DataFrame:
    df = df.copy()
    latest = df.iloc[-1:].copy()

    checks = {}

    checks["price_above_month_avwap"] = (latest["Close"] > latest["avwap_month"]).iloc[0]
    checks["price_above_week_avwap"] = (latest["Close"] > latest["avwap_week"]).iloc[0]
    checks["rsi_bullish"] = (latest["rsi14"] >= 55).iloc[0]
    checks["rsi_bearish"] = (latest["rsi14"] <= 45).iloc[0]
    checks["vol_surge"] = (latest["vol_z20"] >= 1.5).iloc[0]
    checks["fii_dii_divergence_pos"] = (latest["fii_pos_dii_neg"]).iloc[0]
    checks["fii_dii_divergence_neg"] = (latest["fii_neg_dii_pos"]).iloc[0]
    checks["corr_flip"] = (latest["corr20_bn"] < 0.6).iloc[0] if pd.notna(latest["corr20_bn"]).iloc[0] else False
    checks["higher_high"] = (latest["Close"] > latest["hh_20"]).iloc[0]
    checks["lower_low"] = (latest["Close"] < latest["ll_20"]).iloc[0]

    # Score
    weights = {r["id"]: r["weight"] for r in rules_cfg["rules"]}
    raw_score = sum(int(checks.get(k, False)) * weights.get(k, 0) for k in weights)

    # Normalize to 0..100
    smin, smax = rules_cfg["score_bounds"]["min"], rules_cfg["score_bounds"]["max"]
    # Crude normalization assumption: raw score range roughly -40..+40 for this set
    normalized = int((raw_score + 40) / 80 * 100)
    normalized = max(smin, min(smax, normalized))

    out = latest[["date","Close","Volume","avwap_month","avwap_week","rsi14","vol_z20","corr20_bn","fii_cash_net_cr","dii_cash_net_cr"]].copy()
    out["raw_score"] = raw_score
    out["mood_score"] = normalized

    # Booleans to columns
    for k, v in checks.items():
        out[f"rule__{k}"] = bool(v)

    return out

def run(df: pd.DataFrame, rules_cfg: dict) -> pd.DataFrame:
    feats = compute_features(df)
    return evaluate_rules(feats, rules_cfg)
