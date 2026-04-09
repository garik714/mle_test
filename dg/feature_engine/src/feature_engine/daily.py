"""Daily window feature computation strategy.

Computes feature aggregations for a single reference date by filtering
the source data to a rolling window and grouping within that window.
Framework-agnostic thanks to narwhals.
"""

from datetime import timedelta, date

import narwhals as nw
from narwhals.typing import IntoFrameT

from feature_engine.base import WindowFeatureStrategy


class DailyWindowFeatures(WindowFeatureStrategy):
    """Compute daily window features in a DataFrame-agnostic way via narwhals.

    The caller is responsible for loading the data (e.g. pl.scan_parquet)
    and passing it as a native DataFrame or LazyFrame.  The filter, group-by
    and aggregation logic is framework-agnostic thanks to narwhals.
    """

    def compute(
        self,
        in_df: IntoFrameT,
        group_by: list[str],
        exprs: list[nw.Expr],
        current_date: date,
        period_days: int = 7,
    ) -> IntoFrameT:
        """Compute windowed aggregations for a single date.

        Parameters
        ----------
        in_df : IntoFrameT
            Source data with a ``date`` column.
        group_by : list[str]
            Columns to group by inside the window.
        exprs : list[nw.Expr]
            Narwhals aggregation expressions.
        current_date : date
            Right boundary (inclusive) of the window.
        period_days : int
            Window size in days.

        Returns
        -------
        IntoFrameT
            Aggregated result for the single date window.
        """
        return self._compute_narwhals(
            in_df=in_df,
            group_by=group_by,
            exprs=exprs,
            current_date=current_date,
            period_days=period_days,
        )

    @nw.narwhalify
    def _compute_narwhals(
        self,
        in_df: IntoFrameT,
        group_by: list[str],
        exprs: list[nw.Expr],
        current_date: date,
        period_days: int = 7,
    ) -> IntoFrameT:
        return (
            in_df.filter(
                (nw.col("date") > current_date - timedelta(days=period_days))
                & (nw.col("date") <= current_date)
            )
            .group_by(group_by)
            .agg(exprs)
        )

    @nw.narwhalify
    def __call__(
        self,
        in_df: IntoFrameT,
        group_by: list[str],
        exprs: list[nw.Expr],
        current_date: date,
        period_days: int = 7,
    ) -> IntoFrameT:
        """Callable interface for Dagster resource compatibility."""
        return (
            in_df.filter(
                (nw.col("date") > current_date - timedelta(days=period_days))
                & (nw.col("date") <= current_date)
            )
            .group_by(group_by)
            .agg(exprs)
        )
