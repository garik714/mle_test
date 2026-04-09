"""Tests for the IO/DataLoader abstractions."""

from pathlib import Path
import polars as pl
import pytest

from feature_engine.io import PolarsDataLoader


def test_polars_loader_returns_lazyframe(tmp_path: Path):
    """PolarsDataLoader should read a parquet file and return a LazyFrame."""
    import sys
    # Adding src paths for imports
    _dg = Path(__file__).resolve().parents[2]
    if str(_dg / "src") not in sys.path:
        sys.path.insert(0, str(_dg / "src"))

    # Create dummy parquet file
    test_file = tmp_path / "dummy.parquet"
    dummy_df = pl.DataFrame({"a": [1, 2, 3]})
    dummy_df.write_parquet(test_file)

    loader = PolarsDataLoader()
    result = loader.load(test_file)

    # Asset that the correct framework type (LazyFrame) is returned
    assert isinstance(result, pl.LazyFrame)
    
    # Assert data is correct
    assert result.collect().equals(dummy_df)
