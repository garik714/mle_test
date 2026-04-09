"""Backfill window feature computation strategy.

Computes window aggregation features for every date in the dataset
in a single pass using Polars ``group_by_dynamic``.
"""

from datetime import date

import polars as pl

from feature_engine.base import WindowFeatureStrategy


class BackfillWindowFeatures(WindowFeatureStrategy):
    """Compute window features for all dates at once via group_by_dynamic.

    Unlike :class:`DailyWindowFeatures` (which processes a single date),
    this strategy uses Polars ``group_by_dynamic`` to compute rolling-window
    aggregations across the full date range in one efficient pass.

    .. note::
        This strategy requires Polars (not framework-agnostic) because
        ``group_by_dynamic`` is a Polars-specific optimisation.
    """

    def compute(
        self,
        in_df: pl.LazyFrame,
        group_by: list[str],
        exprs: list[pl.Expr],
        current_date: date | None = None,
        period_days: int = 7,
    ) -> pl.LazyFrame:
        """Compute windowed aggregations for every date in the source data.

        Parameters
        ----------
        in_df : pl.LazyFrame
            Source data with a ``date`` column.
        group_by : list[str]
            Columns to group by inside each window (e.g. ``["uid", "val_type"]``).
        exprs : list[pl.Expr]
            Polars aggregation expressions.
        current_date : date | None
            Ignored — backfill processes all dates. Kept for interface
            compatibility with :class:`WindowFeatureStrategy`.
        period_days : int
            Window size in days.

        Returns
        -------
        pl.LazyFrame
            DataFrame with ``date``, group-by columns, and aggregated features.
        """
        return (
            in_df.sort("date")
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


def backfill_window_features(
    lf: pl.LazyFrame,
    group_by: list[str],
    exprs: list[pl.Expr],
    period_days: int = 7,
) -> pl.LazyFrame:
    """Convenience wrapper around :class:`BackfillWindowFeatures`.

    Preserves backward compatibility with code that calls the function
    directly instead of instantiating the strategy class.
    """
    return BackfillWindowFeatures().compute(
        in_df=lf,
        group_by=group_by,
        exprs=exprs,
        period_days=period_days,
    )
