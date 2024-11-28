FROM apache/airflow:slim-2.10.0-python3.12

# First-time build can take upto 10 mins.

ENV AIRFLOW_HOME="/opt/airflow"

# Postgres Datawarehouse env variables
ENV DWH_USERNAME="dwh_user" \
	DWH_PASSWORD="dwh_pass" \
	DWH_HOST="localhost" \
	DWH_PORT="5432" \
	DWH_DB_NAME="dwh_db"

USER root
RUN apt-get update -qq && apt-get install -y vim wget -qqq

COPY ["requirements.txt",  "."]

USER $AIRFLOW_UID

RUN pip install --no-cache-dir -r requirements.txt

USER root

# Ref: https://airflow.apache.org/docs/docker-stack/recipes.html

SHELL ["/bin/bash", "-o", "pipefail", "-e", "-u", "-x", "-c"]

WORKDIR $AIRFLOW_HOME

COPY scripts scripts
RUN chmod +x scripts

USER $AIRFLOW_UID