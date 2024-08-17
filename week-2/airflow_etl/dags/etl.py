from airflow import DAG
import user_sctipts
from airflow.utils.date import days_ago
from airflow.utils.dates import datetime
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.operators.s3 import S3CreateBucketOperator
from airflow.providers.amazon.aws.transfers.local_to_s3 import LocalFilesystemToS3Operator


URL = ""

default_args = {
	"owner": "Tahir",
	"start_date": days_ago(1),
	"depends_on_past": False,
	"retries": 1
}

def transform_data(df):
	"""Transform green taxi data"""
	df["lpep"]

with DAG(
	deg_id = data_ingestion_s3_postgres,
	default_args = default_args,
	schedule_interval = "@once",
	catchup = False,
	max_active_runs = 1,
	tags = ["postgres", "s3"]
) as dag:
	
	download_data = BashOperator(
		task_id = "download_dataset",
		bash_command = f"wget "
	)

	transform_data = PythonOperator(
		task_id = "user_sctipts.transform_data"
	)

	convert_to_parquet_task = PythonOperator(
		task_id = "transform_data",
		python_callable = format_to_parquet,
		kwargs = {
			"src_file": ""
		}
	)
	
	upload_to_dwh_task = PythonOperator(
		task_id = "upload_to_dwh_postgres",
		python_callable = upload_to_postgres,
		kwargs = {
		
		}
	)

	create_s3_bucket = 
	upload_to_s3 = LocalFilesystemToS3Operator(
	    task_id="create_local_to_s3_job",
	    filename="relative/path/to/file.csv",
	    dest_key=S3_KEY,
	    dest_bucket=S3_BUCKET,
	    replace=True
	)