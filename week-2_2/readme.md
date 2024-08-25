endpoint_url in `.aws/credentials` should be written without inverted commas.
Unable to execute `scripts/entrypoint.sh` in **docker-compose.yaml/scheduler** through **Entrypoint** and **command** using the file path  was not working.
The file executed only using `command: bash ./scripts/entrypoint.sh`

To check: `Entrypoint: bash ./scripts/entrypoint.sh`. Need to verify it the script gets executed this way.
**Update** The script can only be executed with bash and not directly with the script path. The problem seems to be with the file permissions i.e. the file does not becomes executeable even after exclusively being made in the Dockerfile.
g airflow was set as **private**. I could not find any options to create the bucket with user provided settings. A file was also uploaded to the created bucket using airflow aws operator. There 
The Minio bucket created usinwas donw without specifying any extra cerdentials.

Loop through all the URLS
Download the data file
Concatenate the files vertically. In this case all the dataset files have the same shape/dimensions.
Transform the data.
a. Partition the data by date and upload to the object storage
b. Upload the transformed data to the data ware house i.e. in this case postgres.
Verify the data has been transferred.

1. Download the datasets
2. Load the dataset as a single pandas dataframe
3. Transform the pandas dataframe
4a. Upload it to data warehouse(postgres)
4b. Convert it to parquet and upload it to data lake

When calling an external(from another file) python function, I was unable to pass airflow builtin functions in the external functions. The external function needs to have kwargs as an argument and ti needs be called using kwargs. Plus `"provide_context: True"` needs to set in the DAG argument.

https://stackoverflow.com/questions/52541911/keyerror-ti-in-apache-airflow-xcom

To upload the file