"""Demo script showing backfill & daily context outputs side by side."""
import sys
import os
os.environ["PYTHONIOENCODING"] = "utf-8"
sys.stdout.reconfigure(encoding="utf-8")

from pathlib import Path
from datetime import date, timedelta
import numpy as np
import polars as pl

_dg = Path("mle_test/dg")
for pkg in ("exprs/src", "feng/src", "synth-data/src"):
    sys.path.insert(0, str(_dg / pkg))

from synth_data import create_daily_agg_pf
from exprs.windows import agg_in_w_exprs, agg_in_w_nw_exprs
from feng.backfill_w_f import backfill_window_features
from feng.daily_w_f import DailyWindowFeatures

np.random.seed(42)
df = create_daily_agg_pf(
    start=date(2026, 1, 1),
    end=date(2026, 1, 10),
    min_types_per_uid=8,
    max_types_per_uid=9,
    num_uids=20,
)

print("=" * 70)
print("1) SOURCE DATA  (3 users, 10 days, synthetic)")
print("=" * 70)
print(df)

print()
print("=" * 70)
print("2) BACKFILL RESULT  (all dates at once, period=3 days)")
print("=" * 70)
bf = backfill_window_features(
    df.lazy(),
    group_by=["uid", "val_type"],
    exprs=agg_in_w_exprs(w="3"),
    period_days=3,
).collect()
print(bf.sort(["date", "uid", "val_type"]))

print()
print("=" * 70)
print("3) DAILY CONTEXT  (single date: 2026-01-05, period=3)")
print("=" * 70)
current = date(2026, 1, 5)
daily = (
    df.lazy()
    .filter(
        (pl.col("date") > current - timedelta(days=3))
        & (pl.col("date") <= current)
    )
    .group_by(["uid", "val_type"])
    .agg(agg_in_w_exprs(w="3"))
    .sort(["uid", "val_type"])
    .collect()
)
print(daily)

print()
bf_slice = bf.filter(pl.col("date") == current).drop("date").sort(["uid", "val_type"])
match = daily.equals(bf_slice)
print(f"  -> Daily vs Backfill[2026-01-05] match: {match}")

print()
print("=" * 70)
print("4) NARWHALS DailyWindowFeatures  (framework-agnostic, period=7)")
print("=" * 70)
wf = DailyWindowFeatures()
nw_result = wf(
    in_df=df.lazy(),
    group_by=["uid", "val_type"],
    exprs=agg_in_w_nw_exprs(w="7"),
    current_date=date(2026, 1, 10),
    period_days=7,
)
print(nw_result.sort(["uid", "val_type"]).collect())
print()
print("Done!")
