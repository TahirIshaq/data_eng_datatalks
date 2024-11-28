"""
Functions related to ny taxi dataset
"""
import os
import re
import user_funcs.data_types as data_types
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from sqlalchemy import create_engine


def get_file_name_from_url(url):
    """Returns file name from URL"""
    name_idx_st = len(url) - url[::-1].find("/")
    file_name = url[name_idx_st:]
    return file_name


def download_from_url(urls, dir_path, write_key, **kwargs):
    """
    Download file from URL
    urls(list): A list of URLs
    **kwargs: Airflow classes/functions/variables
    """
    file_names = [] # Contains the absolute path
    for url in urls:
        file_name = f"{dir_path}/{get_file_name_from_url(url)}"
        os.system(f"wget {url} -O {file_name}")
        file_names.append(file_name)
    kwargs["ti"].xcom_push(key=write_key, value=file_names)


def load_data_test(dir_path, read_key, task_ids, write_key, **kwargs):
    """Load the dataset, combined it and save it locally and push the name of the dataset in xcom"""
    load_val = kwargs["ti"].xcom_pull(key=read_key, task_ids=task_ids)
    print("The type of all_datasets")
    print(type(load_val))
    print("The loaded value from xcom")
    print(load_val)


def load_data(dir_path, read_key, task_ids, write_key, **kwargs):
    """Load the dataset, combined it and save it locally and push the name of the dataset in xcom"""
    all_datasets = kwargs["ti"].xcom_pull(key=read_key, task_ids=task_ids)
    print("The type of all_datasets")
    print(type(all_datasets))
    print("The value of all_datasets")
    print(all_datasets)
    for idx, dataset in enumerate(all_datasets):
        print("The value of dataset")
        print(dataset)
        if idx == 0:
            df = pd.read_csv(dataset, dtype=data_types.green_taxi_other_col, parse_dates=data_types.green_taxi_date_col, nrows=0)
        new_df = pd.read_csv(dataset, dtype=data_types.green_taxi_other_col, parse_dates=data_types.green_taxi_date_col)
        df = pd.concat([df, new_df])
    df_name = f"{dir_path}/combined_dataset.parquet"
    df.to_parquet(df_name)
    # write_key = "combined_dataset"
    print(df_name)
    kwargs["ti"].xcom_push(key=write_key, value=df_name)


def camel_to_snake(name):
    """
    Converts camel case string to snake case
    Copied from https://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-snake-case#1176023
    """
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()


def transform_data(dir_path, read_key, write_key, task_ids, **kwargs):
    """
    Transform and return the updated dataframe
    All columns names should be snake case
    A new col Date column needs to added
    """
    dataset = kwargs["ti"].xcom_pull(key=read_key, task_ids=task_ids)
    df = pd.read_parquet(dataset)
    df.columns = [camel_to_snake(col_name) for col_name in df.columns]
    df = df[df["passenger_count"] > 0]
    df = df[df["trip_distance"] > 0]
    df = df[df["vendor_id"].isin(df["vendor_id"].unique())]
    df["lpep_pickup_date"] = df["lpep_pickup_datetime"].dt.date
<<<<<<< HEAD
    print(pd.io.sql.get_schema(df, name="schema_test"))
=======
>>>>>>> fbd3b5b (etl pipeline with s3 and postgres)
    df_name = f"{dir_path}/transformed_dataset.parquet"
    df.to_parquet(df_name)
    os.environ[write_key] = df_name
    kwargs["ti"].xcom_push(key=write_key, value=df_name)


def upload_dwh(read_key, task_ids, table_name, **kwargs):
    """Upload pd.df data to dwh"""
    dataset = kwargs["ti"].xcom_pull(key=read_key, task_ids=task_ids)
    df = pd.read_parquet(dataset)
<<<<<<< HEAD
    print(pd.io.sql.get_schema(df, name="schema_test"))
    username = os.getenv("DWH_USERNAME")
    password = os.getenv("DWH_PASSWORD")
=======
    username = os.getenv("DWH_USERNAME")
    password = os.getenv("DWH_PASSWORD")
    # password = "dwh_pass"
>>>>>>> fbd3b5b (etl pipeline with s3 and postgres)
    host = os.getenv("DWH_HOST")
    port = os.getenv("DWH_PORT")
    db_name = os.getenv("DWH_DB_NAME")
    db_login = f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{db_name}"
    print("postgres db_login string")
    print(db_login)
    # engine = create_engine(db_login)
    with create_engine(db_login).connect() as con:
        df.head(n=0).to_sql(name=table_name, con=con, if_exists="replace")
        df.to_sql(name=table_name, con=con, if_exists="append")


def upload_s3(read_key, task_ids, bucket_name, table_name, **kwargs):
    """Upload data to S3"""
    file_name = kwargs["ti"].xcom_pull(key=read_key, task_ids=task_ids)
    table = pq.read_table(file_name)
    root_path = f"{bucket_name}/{table_name}"
    s3 = pa.fs.S3FileSystem(scheme="http", endpoint_override="s3:9000")
    pq.write_to_dataset(
        table,
        root_path=root_path,
        partition_cols=["lpep_pickup_date"],
        filesystem=s3
    )


def upload_dwh_alt(read_key, table_name, **kwargs):
    """Upload pd.df data to dwh"""
    dataset = os.getenv(read_key)
    print(f"The value of {read_key} is: {dataset}")
    df = pd.read_parquet(dataset)
    username = os.getenv("DWH_USERNAME")
    password = os.getenv("DWH_PASSWORD")
    # password = "dwh_pass"
    host = os.getenv("DWH_HOST")
    port = os.getenv("DWH_PORT")
    db_name = os.getenv("DWH_DB_NAME")
    db_login = f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{db_name}"
    print("postgres db_login string")
    print(db_login)
    # engine = create_engine(db_login)
    with create_engine(db_login).connect() as con:
        df.head(n=0).to_sql(name=table_name, con=con.connection, if_exists="replace")
        df.to_sql(name=table_name, con=con, if_exists="append")