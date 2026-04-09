"""Data loading abstractions for framework-agnostic pipeline jobs.

These classes abstract away the I/O layer so that the Dagster assets do not
need to import specific dataframe libraries (like Polars or Pandas) just to
read files.
"""

from abc import ABC, abstractmethod
from typing import Any
from pathlib import Path

import polars as pl


class DataLoader(ABC):
    """Abstract interface for data loading resources."""

    @abstractmethod
    def load(self, path: Path) -> Any:
        """Load data from the specified path.

        Parameters
        ----------
        path : Path
            Path to the source data file.

        Returns
        -------
        Any
            The loaded data (e.g., LazyFrame, DataFrame, etc.), depending
            on the specific framework implementation.
        """
        ...


class PolarsDataLoader(DataLoader):
    """Data loader that uses Polars to scan parquet files."""

    def load(self, path: Path) -> pl.LazyFrame:
        """Load data into a Polars LazyFrame using scan_parquet.

        Parameters
        ----------
        path : Path
            Path to the source parquet file.

        Returns
        -------
        pl.LazyFrame
            A lazy representation of the dataset.
        """
        return pl.scan_parquet(path)
