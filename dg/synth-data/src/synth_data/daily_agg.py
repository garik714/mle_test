import polars as pl
from datetime import timedelta, datetime, date
import numpy as np
from functools import partial

def rand_list(_, min_len, max_len) -> list:
    return list(np.random.randint(0, 10, np.random.randint(low=min_len, high=max_len)))

def create_daily_agg_pf(
    start: date,
    end: date,
    min_types_per_uid: int = 1,
    max_types_per_uid: int = 4,
    num_uids: int = 100,
) -> pl.DataFrame:
    date = pl.DataFrame({"date": pl.date_range(start, end, interval="1d", eager=True)})
    uid = pl.DataFrame({"uid": pl.int_range(0, num_uids, eager=True)})
    daily_agg_df = date.join(uid, how="cross")
    del date
    del uid
    # Add nested list of random integers
    daily_agg_df = daily_agg_df.with_columns(
        val_type=pl.col("uid").map_elements(
            function=partial(
                rand_list, min_len=min_types_per_uid, max_len=max_types_per_uid
            ),
            return_dtype=pl.List(pl.Int8),
        )
    )
    daily_agg_df = daily_agg_df.explode("val_type")
    daily_agg_df = daily_agg_df.with_columns(
        val=pl.int_range(100, 10000).sample(n=pl.len(), with_replacement=True)
    )
    return daily_agg_df