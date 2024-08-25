FROM apache/airflow:slim-2.10.0-python3.12

# First-time build can take upto 10 mins.

ENV AIRFLOW_HOME="/opt/airflow"

USER root
RUN apt-get update -qq && apt-get install vim -qqq

COPY ["requirements.tx",  "."]

USER $AIRFLOW_UID

RUN pip install --no-cache-dir -r requirements.txt

USER root

# Ref: https://airflow.apache.org/docs/docker-stack/recipes.html

SHELL ["/bin/bash", "-o", "pipefail", "-e", "-u", "-x", "-c"]

WORKDIR $AIRFLOW_HOME

COPY scripts scripts
RUN chmod +x scripts

USER $AIRFLOW_UID
