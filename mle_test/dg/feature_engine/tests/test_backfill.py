"""Tests that backfill results match daily-context results for each date."""

import sys
from pathlib import Path
from datetime import date, timedelta

import numpy as np
import polars as pl
import pytest

# Make local packages importable without pip install -e
_dg = Path(__file__).resolve().parents[2]
for pkg in ("expressions/src", "feature_engine/src", "synth-data/src"):
    sys.path.insert(0, str(_dg / pkg))

from synth_data import create_daily_agg_pf
from expressions.windows import agg_in_w_exprs
from feature_engine.backfill import backfill_window_features


@pytest.fixture()
def daily_agg_df():
    """Small reproducible synthetic dataset."""
    np.random.seed(42)
    return create_daily_agg_pf(
        start=date(2026, 1, 1),
        end=date(2026, 1, 31),
        min_types_per_uid=2,
        max_types_per_uid=4,
        num_uids=10,
    )


def _daily_context(
    df: pl.DataFrame, current_date: date, period_days: int
) -> pl.DataFrame:
    """Compute window features for a single date (daily context reference)."""
    exprs = agg_in_w_exprs(w=str(period_days))
    return (
        df.lazy()
        .filter(
            (pl.col("date") > current_date - timedelta(days=period_days))
            & (pl.col("date") <= current_date)
        )
        .group_by(["uid", "val_type"])
        .agg(exprs)
        .sort(["uid", "val_type"])
        .collect()
    )


@pytest.mark.parametrize("period_days", [3, 7])
@pytest.mark.parametrize(
    "current_date",
    [date(2026, 1, 10), date(2026, 1, 15), date(2026, 1, 20), date(2026, 1, 31)],
)
def test_backfill_matches_daily(daily_agg_df, current_date, period_days):
    """Backfill row for a given date must equal the daily-context computation."""
    exprs = agg_in_w_exprs(w=str(period_days))

    backfill_result = backfill_window_features(
        lf=daily_agg_df.lazy(),
        group_by=["uid", "val_type"],
        exprs=exprs,
        period_days=period_days,
    ).collect()

    daily_result = _daily_context(daily_agg_df, current_date, period_days)

    backfill_for_date = (
        backfill_result
        .filter(pl.col("date") == current_date)
        .drop("date")
        .sort(["uid", "val_type"])
    )

    assert daily_result.shape == backfill_for_date.shape, (
        f"Shape mismatch for {current_date}, period={period_days}: "
        f"daily={daily_result.shape} vs backfill={backfill_for_date.shape}"
    )
    assert daily_result.equals(backfill_for_date), (
        f"Data mismatch for {current_date}, period={period_days}"
    )


def test_backfill_covers_all_dates(daily_agg_df):
    """Backfill output should have an entry for every source date."""
    period_days = 7
    exprs = agg_in_w_exprs(w=str(period_days))

    backfill = backfill_window_features(
        lf=daily_agg_df.lazy(),
        group_by=["uid", "val_type"],
        exprs=exprs,
        period_days=period_days,
    ).collect()

    source_dates = set(daily_agg_df["date"].unique().to_list())
    backfill_dates = set(backfill["date"].unique().to_list())

    missing = source_dates - backfill_dates
    assert not missing, f"Backfill is missing dates: {sorted(missing)}"
