# NIFTY Market Mood — Mini Version (5–8 hours)

A lean, **defendable** self-project to compute a daily **Market Mood Score** for NIFTY using:
- FII/DII net cash flows (manual CSV or paste recent values)
- OHLCV for NIFTY & BANKNIFTY (via `yfinance`)
- Indicators: **RSI(14)**, **Anchored VWAP** (month & week anchors), **20D volume z-score**
- Simple correlation (20D) between NIFTY and BANKNIFTY
- **Rule-based alerts** → weighted **0–100 mood score**
- Export to `out/daily_dashboard.csv` for Power BI / Google Sheets

> **Evidence:** host a public BI report or Google Sheet + add `docs/method_note.md`.

---

## Quickstart

```bash
# 1) Create environment
python -m venv .venv && . .venv/bin/activate  # (Windows) .venv\Scripts\activate
pip install -r requirements.txt

# 2) Add/verify FII-DII data
# Edit data/fii_dii_sample.csv with the last ~30–60 trading days (date,fii_cash_net_cr,dii_cash_net_cr)

# 3) Run ETL + score
python src/mood_score.py

# 4) Open out/daily_dashboard.csv in Power BI / Google Sheets and build a mini dashboard.
```

## Files

- `data/fii_dii_sample.csv` — sample net flows (INR crore). Replace/extend with real recent data.
- `src/etl.py` — downloads OHLCV via yfinance and merges with FII/DII.
- `src/indicators.py` — RSI, anchored VWAP, rolling stats, correlation.
- `src/alerts.py` — rule engine that produces per-rule booleans and weighted score.
- `src/mood_score.py` — pipeline entrypoint; writes `out/daily_dashboard.csv`.
- `rules.yaml` — thresholds & weights you can tune.
- `dashboards/powerbi_model_spec.md` — minimal guide to wire up the CSV in Power BI.
- `docs/method_note.md` — keep a short “how it works” note for interviews.

## Suggested Commit Flow

- chore: bootstrap repo
- feat: add indicators + rules engine
- feat: compute daily mood score CSV
- docs: add method note + dashboard spec
- refactor: tidy thresholds after 1 week of logs

## License

MIT (optional).
