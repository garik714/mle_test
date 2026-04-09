"""Window aggregation expression builders.

Provides both Polars-native and framework-agnostic (narwhals)
expression factories for use in feature pipelines.
"""

from expressions.windows import agg_in_w_exprs, agg_in_w_nw_exprs

__all__ = ["agg_in_w_exprs", "agg_in_w_nw_exprs"]
