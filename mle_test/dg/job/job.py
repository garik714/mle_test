import os
from pathlib import Path
from datetime import datetime


import polars as pl

from dagster import (
    asset,
    AssetExecutionContext,
    BackfillPolicy,
    DailyPartitionsDefinition,
    ResourceParam,
)

import dagster as dg

from exprs.windows import agg_in_w_nw_exprs
from feng.daily_w_f import DailyWindowFeatures


@asset(
    partitions_def=DailyPartitionsDefinition(start_date="2026-01-01"),
    backfill_policy=BackfillPolicy.multi_run(),
)
def deily_agg(
    context: AssetExecutionContext,
    window_f: ResourceParam[DailyWindowFeatures],
):
    serc_path = Path(os.getenv("DATA_DIR", "/home/mle/data/")) / "assets" / "deily_agg.parquet"
    context.log.info(context.partition_key)
    currnt_date = datetime.strptime(context.partition_key, "%Y-%m-%d").date()
    period_days = 7
    lf = pl.scan_parquet(serc_path)
    res = (
        window_f(
            in_df=lf,
            group_by=["uid", "val_type"],
            exprs=agg_in_w_nw_exprs(w=str(period_days)),
            current_date=currnt_date,
            period_days=period_days,
        )
        .limit(5)
        .collect()
    )
    context.log.info(res)
    return res


daily_job = dg.define_asset_job(
    name="daily_job",
    selection=[deily_agg],
)


daily_job_schedule = dg.build_schedule_from_partitioned_job(
    job=daily_job,
)


defs = dg.Definitions(
    assets=[
        deily_agg,
    ],
    jobs=[
        daily_job,
    ],
    schedules=[
        daily_job_schedule,
    ],
    resources={"window_f": DailyWindowFeatures()},
)