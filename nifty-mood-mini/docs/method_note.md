# Method Note (Short)

**Data**
- OHLCV for NIFTY (^NSEI; fallback NIFTYBEES.NS) and BANKNIFTY (^NSEBANK) via yfinance (daily).
- FII/DII net cash (INR cr) manually curated in `data/fii_dii_sample.csv`.

**Features**
- RSI(14) (Wilder smoothing).
- Anchored VWAPs: month-start and week-start.
- 20D volume z-score; 20D rolling correlation with BANKNIFTY; 20D HH/LL.

**Rules → Score**
- 10 binary checks + weights (see `rules.yaml`).
- Sum → affine map to 0..100 as a simple mini version.

**Outputs**
- `out/daily_dashboard.csv` for BI.
- Keep this note + a dashboard link as evidence.
