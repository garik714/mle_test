from pathlib import Path
from datetime import timedelta, datetime, date

# TODO: rm polars dependency. For example you can use narwhals to do DataFrame agnostic assets

import polars as pl
import narwhals as nw


class DailyWindowFeatures:
    def __call__(
        self,
        in_df_path: Path,
        group_by: list[str],
        exprs: list[pl.Expr],
        current_date: date,
        period_days: int = 7,
    ) -> pl.LazyFrame:
        return (
            pl
            .scan_parquet(in_df_path)
            .filter(
                (current_date - timedelta(days=period_days) < pl.col("date"))
                & (pl.col("date") <= current_date)
            )
            .group_by(group_by)
            .agg(exprs)
        )
