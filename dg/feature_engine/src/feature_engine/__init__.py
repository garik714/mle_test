"""Feature engineering strategies for window-based computations.

Provides the ``WindowFeatureStrategy`` abstract base class and two
concrete implementations: ``DailyWindowFeatures`` (single-date,
framework-agnostic) and ``BackfillWindowFeatures`` (all-dates-at-once,
Polars-optimised).
"""

from feature_engine.base import WindowFeatureStrategy
from feature_engine.daily import DailyWindowFeatures
from feature_engine.backfill import BackfillWindowFeatures, backfill_window_features

__all__ = [
    "WindowFeatureStrategy",
    "DailyWindowFeatures",
    "BackfillWindowFeatures",
    "backfill_window_features",
]
