import polars as pl
import narwhals as nw


def agg_in_w_exprs(w: str, agg_col: str = "val", suffix_by: str = "type") -> list[pl.Expr]:
    """Polars aggregation expressions for a window."""
    suffix = f"{agg_col}_by_{suffix_by}_in_{w}"
    return [
        pl.sum(agg_col).alias(f"sum_{suffix}"),
        pl.min(agg_col).alias(f"min_{suffix}"),
        pl.max(agg_col).alias(f"max_{suffix}"),
    ]


def agg_in_w_nw_exprs(w: str, agg_col: str = "val", suffix_by: str = "type") -> list[nw.Expr]:
    """Framework-agnostic (narwhals) aggregation expressions for a window."""
    suffix = f"{agg_col}_by_{suffix_by}_in_{w}"
    return [
        nw.col(agg_col).sum().alias(f"sum_{suffix}"),
        nw.col(agg_col).min().alias(f"min_{suffix}"),
        nw.col(agg_col).max().alias(f"max_{suffix}"),
    ]
