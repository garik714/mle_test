"""Tests for DailyWindowFeatures.compute() with narwhals expressions.

Verifies that the narwhals-based strategy produces the same results
as a raw Polars daily-context computation, confirming the framework-
agnostic layer works correctly end-to-end.
"""

import sys
from pathlib import Path
from datetime import date, timedelta

import numpy as np
import polars as pl
import pytest



from synth_data import create_daily_aggregation
from expressions.windows import agg_in_w_exprs, agg_in_w_nw_exprs
from feature_engine.daily import DailyWindowFeatures


def _polars_daily_context(
    df: pl.DataFrame, current_date: date, period_days: int
) -> pl.DataFrame:
    """Reference: compute window features using raw Polars (no narwhals)."""
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
def test_daily_compute_matches_polars_reference(daily_agg_df, current_date, period_days):
    """DailyWindowFeatures.compute() with narwhals exprs must match raw Polars."""
    strategy = DailyWindowFeatures()
    nw_exprs = agg_in_w_nw_exprs(w=str(period_days))

    result = (
        strategy.compute(
            in_df=daily_agg_df.lazy(),
            group_by=["uid", "val_type"],
            exprs=nw_exprs,
            current_date=current_date,
            period_days=period_days,
        )
        .sort(["uid", "val_type"])
        .collect()
    )

    expected = _polars_daily_context(daily_agg_df, current_date, period_days)

    assert result.shape == expected.shape, (
        f"Shape mismatch for {current_date}, period={period_days}: "
        f"narwhals={result.shape} vs polars={expected.shape}"
    )
    assert result.equals(expected), (
        f"Data mismatch for {current_date}, period={period_days}"
    )


def test_daily_compute_returns_lazyframe_for_lazy_input(daily_agg_df):
    """When given a LazyFrame, compute() should return a LazyFrame."""
    strategy = DailyWindowFeatures()
    nw_exprs = agg_in_w_nw_exprs(w="7")

    result = strategy.compute(
        in_df=daily_agg_df.lazy(),
        group_by=["uid", "val_type"],
        exprs=nw_exprs,
        current_date=date(2026, 1, 15),
        period_days=7,
    )
    assert isinstance(result, pl.LazyFrame), (
        f"Expected LazyFrame, got {type(result).__name__}"
    )


def test_daily_compute_returns_dataframe_for_eager_input(daily_agg_df):
    """When given an eager DataFrame, compute() should return a DataFrame."""
    strategy = DailyWindowFeatures()
    nw_exprs = agg_in_w_nw_exprs(w="7")

    result = strategy.compute(
        in_df=daily_agg_df,
        group_by=["uid", "val_type"],
        exprs=nw_exprs,
        current_date=date(2026, 1, 15),
        period_days=7,
    )
    assert isinstance(result, pl.DataFrame), (
        f"Expected DataFrame, got {type(result).__name__}"
    )
