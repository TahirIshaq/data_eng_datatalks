# Software version

- Docker Compose version v2.29.1
- Docker version 27.1.1, build 6312585


Just run `docker compose up -d`

The hostname of the postgres db in etl needs to the same as the service name of the db. If the docker image has already been built it can updated by overwriting the `DB_HOST` variables in `docker-compose.yaml`. If the images had not been built or a new version needs to be built the default vales can be changed in `database.env`.

Initially the postgres database server will be initized. When the service is healthy, the etl pipeline will run which will populate the database.

The database can be accessed by:

`docker exec -it <database container ID> bash`

`psql "postgresql://<db_username>:<db_password>@<db_hostname>:<db_port>/<db_name>"`

The default login credentials for the database are:

`psql "postgresql://demo_user:demo:pass@localhost:5432/demo_db"`

To view the list of tables:

`\d`

To see the column details of tables:

`\d+ <table_name>`

Table or column names with Upper case or special characters e.g. Spaces, - etc need to enclosed in double quotes.