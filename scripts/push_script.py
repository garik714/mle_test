import json
import os
files=[
"mle_test/README.md",
"mle_test/dagster_home/.nux/nux.yaml",
"mle_test/dagster_home/.telemetry/id.yaml",
"mle_test/dg/exprs/README.md",
"mle_test/dg/exprs/pyproject.toml",
"mle_test/dg/exprs/src/exprs/__init__.py",
"mle_test/dg/exprs/src/exprs/windows.py",
"mle_test/dg/exprs/tests/__init__.py",
"mle_test/dg/feng/README.md",
"mle_test/dg/feng/pyproject.toml",
"mle_test/dg/feng/src/feng/__init__.py",
"mle_test/dg/feng/src/feng/daily_w_f.py",
"mle_test/dg/feng/tests/__init__.py",
"mle_test/dg/job/job.py",
"mle_test/dg/synth-data/README.md",
"mle_test/dg/synth-data/pyproject.toml",
"mle_test/dg/synth-data/src/synth_data/__init__.py",
"mle_test/dg/synth-data/src/synth_data/daily_agg.py",
"mle_test/dg/synth-data/tests/__init__.py",
"mle_test/images/Dockerfile",
"mle_test/setup_data.py",
"mle_test/nb/polars_backfill.ipynb",
"mle_test/nb/polars_daily_opt.ipynb"
]
out = []
for f in files:
    if os.path.exists(f) and os.path.getsize(f) > 0:
        try:
            with open(f, 'r', encoding='utf-8') as fh:
                content = fh.read()
            out.append({"path": f.replace('mle_test/', ''), "content": content})
        except Exception as e:
            pass
with open('push_payload.json', 'w', encoding='utf-8') as f:
    json.dump(out, f)
