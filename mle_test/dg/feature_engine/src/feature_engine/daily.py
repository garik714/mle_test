from datetime import timedelta, date

import narwhals as nw
from narwhals.typing import IntoFrameT


class DailyWindowFeatures:
    """Compute daily window features in a DataFrame-agnostic way via narwhals.

    The caller is responsible for loading the data (e.g. pl.scan_parquet)
    and passing it as a native DataFrame or LazyFrame.  The filter, group-by
    and aggregation logic is framework-agnostic thanks to narwhals.
    """

    @nw.narwhalify
    def __call__(
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
