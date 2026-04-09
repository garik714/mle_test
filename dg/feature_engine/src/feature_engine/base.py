"""Abstract base class for window-based feature computation strategies.

New feature strategies (e.g. weekly, sliding, exponential) should inherit
from ``WindowFeatureStrategy`` and implement the ``compute`` method.
"""

from abc import ABC, abstractmethod
from datetime import date
from typing import Any


class WindowFeatureStrategy(ABC):
    """Base class for all window-based feature computation strategies.

    Subclasses must implement :meth:`compute` which receives a
    DataFrame-like object, grouping columns, aggregation expressions,
    a reference date and a window size, and returns the aggregated result.

    This abstraction allows the Dagster pipeline to swap strategies
    (daily context, backfill, etc.) without changing asset code.
    """

    @abstractmethod
    def compute(
        self,
        in_df: Any,
        group_by: list[str],
        exprs: list,
        current_date: date,
        period_days: int = 7,
    ) -> Any:
        """Compute windowed feature aggregations.

        Parameters
        ----------
        in_df : Any
            Source data (DataFrame or LazyFrame, framework-agnostic).
        group_by : list[str]
            Columns to group by inside each window.
        exprs : list
            Aggregation expressions.
        current_date : date
            Reference date for the computation window.
        period_days : int
            Window size in days.

        Returns
        -------
        Any
            Aggregated result in the same framework as ``in_df``.
        """
        ...
