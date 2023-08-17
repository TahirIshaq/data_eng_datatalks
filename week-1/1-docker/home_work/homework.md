
# Setup

Download and insert the dataset in the database.

Make sure that postgres server is running. Then, save the URLs of the datasets in the environment variables.

`export URL=https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-01.csv.gz`

`export URL2=https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv`

```
python pipeline2.py \
--url $URL \
--dataset green_taxi.csv \
--compression ".gz" \
--table_name "green_taxi" \
--col_names "lpep_pickup_datetime" "lpep_dropoff_datetime" \
--col_datatypes "datetime" "datetime"
```

```
python pipeline2.py \
--url $URL2 \
--dataset taxi_zone.csv \
--table_name "taxi_zone"
```

This script can also be contaierized by `docker build -t pipeline:v02 .`

To update the databae using the pipeline container, both postgres and the pipeline container should be part of the same network.

```
docker run -it \
-e POSTGRES_USER="tahir" \
-e POSTGRES_PASSWORD="tahir" \
-e POSTGRES_DB="ny_taxi" \
-p "5432:5432" \
-v /home/tahir/workspace/data_eng_datatalks/week-1/1-docker/3/ny_data_taxi:/var/lib/postgresql/data \
--network=pg_network \
--name=pg_database \
postgres:13
```

```
docker run -it --network=pg_network \
--name=pg_pipeline \
pipeline:v02 \
--host pg_database \
--url $URL1 \
--dataset green_taxi.csv \
--compression ".gz" \
--table_name "green_taxi" \
--col_names "lpep_pickup_datetime" "lpep_dropoff_datetime" \
--col_datatypes "datetime" "datetime"
```

```
docker run -it --network=pg_network \
--name=pg_pipeline \
pipeline:v02 \
--host pg_database \
--url $URL2 \
--dataset taxi_zone.csv \
--table_name "taxi_tone"
```

# Answers

## Question 1

```
docker --help

docker build --help
```


**Answer:** `--iidfile string                Write the image ID to the file`

## Question 2

`docker run -it python:3.9 bash`

`pip list`

**Answer:** 3

## Question 3

Matching strings should be written in single quotes otherwise, it will result in an error. For example
`SELECT last_name FROM person WHERE first_name='ali'`.

**Setup**

```
docker start pg_database

docker exec -it pg_database

psql “<username>:<password>@<host name>:<port>/<database name>”
psql “tahir:tahir@localhost:5432/ny_taxi”

SELECT COUNT(*) 
FROM green_taxi 
WHERE 
DATE(lpep_pickup_datetime)='2019-01-15' AND DATE(lpep_dropoff_datetime)='2019-01-15';
```

**Answer:** 20530

## Question 4

List of all the table columns: `\d+ green_taxi`

```
SELECT DATE(lpep_pickup_datetime) 
FROM green_taxi 
WHERE trip_distance=
(SELECT  MAX(trip_distance) 
FROM green_taxi);
```

**Answer:** 2019-01-15

## Question 5

```
SELECT (SELECT 
    COUNT(lpep_pickup_datetime) 
    FROM green_taxi 
    WHERE passenger_count=2 
    AND DATE(lpep_pickup_datetime)='2019-01-01') AS "2 passengers", (SELECT COUNT(lpep_pickup_datetime) 
    FROM green_taxi 
    WHERE passenger_count=3 AND 
    DATE(lpep_pickup_datetime)='2019-01-01') AS "3 passengers";
```

**Answer:** `2 : 1282, 3: 254`

## Question 6

Column names with upper case characters need to enclosed in double quotes “”.


```
Copied from the solution video

SELECT z2."Zone", MAX(tip_amount) AS MAX_tip
FROM green_taxi gt
INNER JOIN taxi_zone z
ON gt."PULocationID" = z."LocationID"
INNER JOIN taxi_zone z2
ON gt."DOLocationID" = z2."LocationID"
WHERE z."Zone" = 'Astoria'
GROUP BY z2."Zone"
ORDER BY MAX_tip DESC
LIMIT 1;
```
