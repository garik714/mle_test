"""Generate synthetic data for the dagster pipeline."""
import os
import sys
sys.stdout.reconfigure(encoding='utf-8')

from pathlib import Path
from datetime import date

from synth_data import create_daily_aggregation

data_dir = Path(os.getenv("DATA_DIR", "./data/"))
assets_dir = data_dir / "assets"
assets_dir.mkdir(parents=True, exist_ok=True)

out_path = assets_dir / "daily_agg.parquet"
print("Generating synthetic data...")

df = create_daily_aggregation(
    start=date(2026, 1, 1),
    end=date(2026, 4, 1),
    min_types_per_uid=2,
    max_types_per_uid=5,
)

df.write_parquet(out_path)
print(f"Done! Shape: {df.shape}")
