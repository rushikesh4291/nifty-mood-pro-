import pandas as pd
from pathlib import Path
from .etl import merge_all
from .alerts import run, load_rules

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "out"

def main():
    df = merge_all()
    rules = load_rules()
    out = run(df, rules)
    OUT.mkdir(exist_ok=True, parents=True)
    out.to_csv(OUT / "daily_dashboard.csv", index=False)
    print("Wrote:", OUT / "daily_dashboard.csv")

if __name__ == "__main__":
    main()
