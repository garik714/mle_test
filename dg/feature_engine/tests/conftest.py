"""Shared test setup and fixtures for feature_engine."""

import sys
from pathlib import Path
from datetime import date

import numpy as np
import pytest

# Make local packages importable without pip install -e
_dg = Path(__file__).resolve().parents[2]
for pkg in ("expressions/src", "feature_engine/src", "synth-data/src"):
    pkg_path = str(_dg / pkg)
    if pkg_path not in sys.path:
        sys.path.insert(0, pkg_path)

from synth_data import create_daily_aggregation


@pytest.fixture()
def daily_agg_df():
    """Small reproducible synthetic dataset common to all test cases."""
    np.random.seed(42)
    return create_daily_aggregation(
        start=date(2026, 1, 1),
        end=date(2026, 1, 31),
        min_types_per_uid=2,
        max_types_per_uid=4,
        num_uids=10,
    )
