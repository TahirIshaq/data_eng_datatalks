# Task

Access the database using pgadmin. Both containers should be running on the same docker network. And pgadmin will access postgres container using its name.

To run pgadmin

```
docker run -it \
-e PGADMIN_DEFAULT_EMAIL="tahir@mail.com" \
-e PGADMIN_DEFAULT_PASSWORD="tahir" \
-p 8080:80 \
--network=pg_network \
--name=pg_admin \
dpage/pgadmin4
```

To run postgres

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

Open the address in the internet browser in the host computer: `localhost:8080`

login using the credentials (tahir@mail.com, tahir) set in the docker run pgadmin command.

Add new server.

1. In the general tab, enter the desired name of the pgadmin server.
2. Enter the countainer name ("pg_database"), port(5432), username(tahir) and password(tahir) in the connections tab.
3. Click save.
4. Expand newly added server, databases, desired database (ny_Taxi), right click and select "CREATE script" to enter the query.
