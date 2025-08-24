# Power BI wiring (mini)

1) Get Data → Text/CSV → `out/daily_dashboard.csv`
2) Format `date` as Date; set data category "Uncategorized".
3) Cards:
   - Mood Score (mood_score)
   - Close (Close) and RSI (rsi14)
4) KPI/Rules table: show all `rule__*` columns (True/False).
5) Trend lines:
   - Line chart: Close vs Date + avwap_month + avwap_week
   - Line chart: RSI vs Date with band (45–55)
6) Refresh: set manual refresh daily pre‑open (07:30 IST) for this mini project.
