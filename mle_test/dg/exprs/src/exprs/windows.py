import polars as pl
import narwhals as nw

def agg_in_w_exprs(w: str, agg_col: str = "val", suffix_by: str = "type") -> list[pl.Expr]:
    suffix = f"{agg_col}_by_{suffix_by}_in_{w}"
    return [
        pl.sum(agg_col).alias(f"sum_{suffix}"),
        pl.min(agg_col).alias(f"min_{suffix}"),
        pl.max(agg_col).alias(f"max_{suffix}"),
    ]