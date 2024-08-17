#!/usr/bin/env bash

echo "Creating airflow directories"

mkdir dags logs plugins

echo "airflow db migrate\nairflow users create -r Admin -u admin -p admin -e admin@example.com -f admin -l airflow\nairflow webserver" > entrypoint.sh

mv entrypoint.sh scripts/entrypoint.sh

chmod 777 dags logs plugins