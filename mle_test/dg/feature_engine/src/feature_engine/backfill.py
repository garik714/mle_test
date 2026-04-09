"""Backfill window features using group_by_dynamic for efficient batch computation."""

import polars as pl


def backfill_window_features(
    lf: pl.LazyFrame,
    group_by: list[str],
    exprs: list[pl.Expr],
    period_days: int = 7,
) -> pl.LazyFrame:
    """Compute window aggregation features for every date in the dataset.

    Unlike the daily context (which processes a single current_date),
    this function uses Polars group_by_dynamic to compute rolling-window
    aggregations across the full date range in one pass.

    Parameters
    ----------
    lf : pl.LazyFrame
        Source data with a ``date`` column.
    group_by : list[str]
        Columns to group by inside each window (e.g. ``["uid", "val_type"]``).
    exprs : list[pl.Expr]
        Aggregation expressions (e.g. from ``agg_in_w_exprs``).
    period_days : int
        Window size in days.

    Returns
    -------
    pl.LazyFrame
        DataFrame with ``date``, group-by columns, and aggregated features.
        The ``date`` column corresponds to the right (inclusive) boundary
        of each window, matching the ``current_date`` semantics used in
        the daily context.
    """
    return (
        lf.sort("date")
        .group_by_dynamic(
            "date",
            every="1d",
            period=f"{period_days}d",
            offset=f"-{period_days}d",
            group_by=group_by,
            closed="right",
            label="right",
        )
        .agg(exprs)
    )
