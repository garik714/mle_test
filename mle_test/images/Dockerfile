FROM python:3.11-slim


RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    build-essential \
    git \
    vim \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash mle

USER mle

# The default working directory for the user
WORKDIR /home/mle


RUN pip install \
    dagster \
    numpy \
    dagster-webserver \
    dagster-dg-cli \
    pandas \
    polars \
    narwhals \
    jupyter \
    jupyter_black \
    poetry

ENV DAGSTER_HOME=/home/mle/dagster_home/
ENV DATA_DIR=/home/mle/data/
RUN mkdir -p $DAGSTER_HOME $DATA_DIR/src/mle_test

EXPOSE 3000
EXPOSE 8888

ENTRYPOINT [ "tail", "-f", "/dev/null" ]