# Task

Containerize the pipeline script. Both pipeline and postgres container should be running in the same network. Pipeline container will use postgres containers name as the host name.

All docker containers are a part of the some kind of network. If not explicitely specified, the container becomes a part of a new network.

To see available docker containers: `docker network ls`

Create a new docker network: `docker network create pg_network`

Start the postgres container with a specific network.

```
docker run -it \
-e POSTGRES_USER="tahir" \
-e POSTGRES_PASSWORD="tahir" \
-e POSTGRES_DB="ny_taxi" \
-v $(pwd)/ny_data_taxi:/var/lib/postgresql/data \
-p 5432:5432 \
--network=pg_network \
--name=pg_database \
postgres:13
```

To build the pipeline container: `docker build -t pipeline:v01 .`

Store the URL of the database:

`export URL=https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz`

To run the container

```
docker run -it --network=pg_network pipeline:v01 --host="pg_database" --url=$URL
```