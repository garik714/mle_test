# Getting Started
## Build the dev container
```bash
cd mle_test\images\
docker build -t mle-test:latest .
```
## Setup local dev environment
```bash
docker create --name mle-test-dev -v <local_path_to_mle_test>:/home/mle/src/mle_test mle-test:latest
# Windows Docker Desktop example
docker create --name mle-test-dev -v C:\Users\$env:UserName\dsml\work\data_lake\mle_test:/home/mle/src/mle_test mle-test:latest
```

```bash
# install libs expressions, feature_engine, synth-data
cd <lib_dir> 
pip install -e .
```

## Setup the dagster pipeline
The source data for job.py creates in nb/polars_backfill.ipynb
```bash
cd 
dg dev -f job.py
```