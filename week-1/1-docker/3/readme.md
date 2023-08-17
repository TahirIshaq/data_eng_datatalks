# Task

Dataset link: `wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz`

`export URL=https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz`

Download dataset using: `os.system(wget source url -O destination file)`

Load the dataset: `df = pd.read_csv(dataset, nrows=100)`

Check the table creation sql command: `df.head(n=0).to_sql(name=table_name)`

Update the parameters to date time: `df.parameter = pd.to_datetime(df.parameter)`

Connect to the database: `engine = create_engine(postgresql://username:password@host_name:port/db_name)`

Load the dataset with iterator: `df_iter = pd.read_csv(dataset, iterator=True, chunksize=100000)`

Create a table: `df.head(n=0).to_sql(name=table_name, con=engine, if_exists="replace")`

Update the table: `dataframe.to_sql(name=table_name, con=engine, if_exists="append")`

Start/Create postgresql container:

```
docker run -it \
-e POSTGRES_USER="tahir" \
-e POSTGRES_PASSWORD="tahir" \
-e POSTGRES_DB="ny_taxi" \
-v /home/tahir/workspace/data_eng_datatalks/week-1/1-docker/3/ny_data_taxi:/var/lib/postgresql/data \
-p 5432:5432 \
postgres:13
```

Make sure to give the absolute path of the volume directory otherwise, there will be error in connecting to the database.

After creating/starting the container, login to the container: 
`docker exec -it <container_id> bash`

Connect to the database: `psql postgresql://tahir:tahir@localhost:5432/ny_taxi`

List all the users in the database: `\du`

List all the tables in the connected database: `\dt`

Verify if table has been updated with dataset data: `SELECT COUNT(*) FROM table`