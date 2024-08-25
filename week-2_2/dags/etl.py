import os
from airflow import DAG
import user_funcs.ny_taxi as ny_taxi
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator, PythonVirtualenvOperator, is_venv_installed
from airflow.providers.amazon.aws.operators.s3 import S3CreateBucketOperator

BASE_PATH = os.getenv("HOME", "/home/airflow")

DATASET_KEY = ""
BUCKET_NAME = "b1-test"
TABLE_NAME = "ny_green_taxi"
DOWNLOAD_DATA_KEY = "downloaded_data"
DOWNLOAD_DATA_TASK_ID = "download_data"
LOAD_DATA_KEY = "load_data"
LOAD_DATA_TASK_ID = "load_data"
TRANSFORM_DATA_KEY = "transform_data"
TRANSFORM_DATA_TASK_ID = "transform_data"
CREATE_BUCKET_TASK_ID = "create_bucket"
UPLOAD_TO_S3_TASK_ID = "upload_to_s3"
UPLOAD_TO_DWH_TASK_ID = "upload_to_dwh"


TAXI_YEAR = "2020"
TAXI_MONTHS = ["10", "11", "12"]
TAXI_COLOR = "green"
BASE_URL = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/"
URLS = [f"{BASE_URL}{TAXI_COLOR}_tripdata_{TAXI_YEAR}-{month}.csv.gz" for month in TAXI_MONTHS]

default_args = {
    "owner": "Tahir",
	"start_date": days_ago(1),
	"depends_on_past": False,
	"retries": 0,
    "provide_context": True
}

with DAG(
	dag_id = "hello",
	default_args = default_args,
	schedule_interval = "@once",
	catchup = False,
	max_active_runs = 1,
	tags = ["hello"]
) as dag:
    download_data_from_url = PythonOperator(
        task_id = DOWNLOAD_DATA_TASK_ID,
        python_callable = ny_taxi.download_from_url,
        op_kwargs = {"urls": URLS, "dir_path": BASE_PATH, "write_key": DOWNLOAD_DATA_KEY}
    )
    load_data = PythonOperator(
        task_id = LOAD_DATA_TASK_ID,
        python_callable = ny_taxi.load_data,
        op_kwargs = {"dir_path": BASE_PATH, "read_key": DOWNLOAD_DATA_KEY, "task_ids": DOWNLOAD_DATA_TASK_ID, "write_key": LOAD_DATA_KEY}
    )
    transform_data = PythonOperator(
        task_id = TRANSFORM_DATA_TASK_ID,
        python_callable = ny_taxi.transform_data,
        op_kwargs = {"dir_path": BASE_PATH, "read_key": LOAD_DATA_KEY, "write_key": TRANSFORM_DATA_KEY, "task_ids": LOAD_DATA_TASK_ID}
    )
    create_bucket = S3CreateBucketOperator(
        task_id = CREATE_BUCKET_TASK_ID,
        bucket_name = BUCKET_NAME
    )
    upload_to_s3 = PythonOperator(
        task_id = UPLOAD_TO_S3_TASK_ID,
        python_callable = ny_taxi.upload_s3,
        op_kwargs = {"read_key": TRANSFORM_DATA_KEY, "task_ids": TRANSFORM_DATA_TASK_ID, "bucket_name": BUCKET_NAME, "table_name": TABLE_NAME}
    )
    # upload_to_dwh = PythonVirtualenvOperator(
        # task_id = UPLOAD_TO_DWH_TASK_ID,
        # python_callable = ny_taxi.upload_dwh_alt,
        # requirements=["SQLAlchemy~=2.0.31"],
        # op_kwargs = {"read_key": TRANSFORM_DATA_KEY, "table_name": TABLE_NAME}
    # )
    upload_to_dwh = PythonOperator(
        task_id = UPLOAD_TO_DWH_TASK_ID,
        python_callable = ny_taxi.upload_dwh,
        op_kwargs = {"read_key": TRANSFORM_DATA_KEY, "task_ids": TRANSFORM_DATA_TASK_ID, "table_name": TABLE_NAME}
    )
    # create_local_to_s3_job = LocalFilesystemToS3Operator(
    #     task_id="create_local_to_s3_job",
    #     filename=f"{base_path}/sample.txt",
    #     dest_key="sample.txt",
    #     dest_bucket="b1-test",
    #     replace=True,
    # )
    # create_sample_file >> create_bucket >> create_local_to_s3_job
    # download_data_from_url >> load_data >> transform_data >> create_bucket >> [upload_to_s3, upload_to_dwh]
    download_data_from_url >> load_data >> transform_data >> create_bucket >> [upload_to_s3, upload_to_dwh]
    # upload_to_dwh