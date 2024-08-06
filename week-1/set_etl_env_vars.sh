#!/usr/bin/bash
# Run this script if etl.py needs to run without docker.
# . ./set_etl_env_vars.sh
# This will execute the file in the current shell. If this file is run like "./set_etl_env_vars.sh". This will open a new shell, execute the file and exit the shell.
# To test the initialized env variables
# printenv URL or any other env variable
echo "Unset variables if already exists"
unset DB_USERNAME \
		DB_PASSWORD \
		DB_HOST \
		DB_PORT \
		DB_NAME \
		URL

echo "Set env variables"
export 	DB_USERNAME="demo_user" \
		DB_PASSWORD="demo_pass" \
		DB_HOST="localhost" \
		DB_PORT="5432" \
		DB_NAME="demo_db" \
		URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-09.csv.gz,https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv"

echo ""
echo "Printing the initialized env variables"
echo $DB_USERNAME
echo $DB_PASSWORD
echo $DB_HOST
echo $DB_PORT
echo $DB_NAME
echo $URL