"""Synthetic daily aggregation data generator.

Produces a Polars DataFrame of synthetic daily metrics keyed by
(date, uid, val_type) with a random integer ``val`` column.
Used for testing and development of the feature engineering pipeline.
"""

import polars as pl
from datetime import date
import numpy as np
from functools import partial


def _random_type_ids(
    _: int, min_len: int, max_len: int
) -> list[int]:
    """Generate a random list of integer type IDs.

    Parameters
    ----------
    _ : int
        Ignored positional argument required by ``map_elements``.
    min_len : int
        Minimum number of type IDs to produce.
    max_len : int
        Maximum (exclusive) number of type IDs to produce.

    Returns
    -------
    list[int]
        Random integers in [0, 10).
    """
    return list(np.random.randint(0, 10, np.random.randint(low=min_len, high=max_len)))


def create_daily_aggregation(
    start: date,
    end: date,
    min_types_per_uid: int = 1,
    max_types_per_uid: int = 4,
    num_uids: int = 100,
) -> pl.DataFrame:
    """Create a synthetic daily aggregation DataFrame.

    Generates a cross-join of ``[start, end]`` dates × ``num_uids`` users,
    then assigns a random number of ``val_type`` entries to each row and
    samples a random ``val`` for every (date, uid, val_type) triple.

    Parameters
    ----------
    start : date
        First date (inclusive).
    end : date
        Last date (inclusive).
    min_types_per_uid : int
        Minimum number of value-type entries per user per day.
    max_types_per_uid : int
        Maximum (exclusive) number of value-type entries per user per day.
    num_uids : int
        Number of distinct user IDs.

    Returns
    -------
    pl.DataFrame
        Columns: ``date``, ``uid``, ``val_type``, ``val``.
    """
    dates = pl.DataFrame({"date": pl.date_range(start, end, interval="1d", eager=True)})
    uids = pl.DataFrame({"uid": pl.int_range(0, num_uids, eager=True)})
    daily_agg_df = dates.join(uids, how="cross")

    daily_agg_df = daily_agg_df.with_columns(
        val_type=pl.col("uid").map_elements(
            function=partial(
                _random_type_ids, min_len=min_types_per_uid, max_len=max_types_per_uid
            ),
            return_dtype=pl.List(pl.Int8),
        )
    )
    daily_agg_df = daily_agg_df.explode("val_type")
    daily_agg_df = daily_agg_df.with_columns(
        val=pl.int_range(100, 10000).sample(n=pl.len(), with_replacement=True)
    )
    return daily_agg_df