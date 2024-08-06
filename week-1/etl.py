import time
from sqlalchemy import create_engine, text
import pandas as pd
import dataset_col_dtypes
#import queries
import os


def download_dataset(url):
	"""Download the dataset"""
	fullname_idx_start = len(url) - url[::-1].find("/")
	dataset_fullname = url[fullname_idx_start:]
	os.system(f"wget {url} -O {dataset_fullname}")
	return dataset_fullname


def get_file_name(full_name):
	"""Returns the file name without extension"""
	name_end_idx = full_name.find(".")
	name = full_name[:name_end_idx]
	return name


def get_df_dtypes(name):
	"""Transform the data"""
	date_cols = None
	mixtype_cols = None
	if "green" in name:
		date_cols = dataset_col_dtypes.green_taxi_datetime
		mixtype_cols = dataset_col_dtypes.green_taxi_data_types_test
	elif "yellow" in name:
		date_cols = dataset_col_dtypes.yellow_taxi_data_types
		mixtype_cols = dataset_col_dtypes.yellow_taxi_datetime
	elif "zone":
		mixtype_cols = dataset_col_dtypes.taxi_zone
	return date_cols, mixtype_cols


def main():
	"""Main function"""
	username = os.getenv("DB_USERNAME")
	password = os.getenv("DB_PASSWORD")
	host = os.getenv("DB_HOST")
	port = os.getenv("DB_PORT")
	db_name = os.getenv("DB_NAME")
	urls = os.getenv("URL")

	urls = urls.split(",")
	db_login = f"postgresql://{username}:{password}@{host}:{port}/{db_name}"
	for url in urls:
		dataset = download_dataset(url)
		table_name = get_file_name(dataset)
		datetime_cols, mixtype_cols = get_df_dtypes(table_name)
		with create_engine(db_login).connect() as con:
			df = pd.read_csv(dataset, parse_dates=datetime_cols, dtype=mixtype_cols, iterator=True, chunksize=100000)
			create_table = True
			for data in df:
				start_time = time.time()
				if create_table:
					create_table = False
					data.head(0).to_sql(name=table_name, con=con, if_exists="replace")
				data.to_sql(name=table_name, con=con, if_exists="append")
				total_time = time.time() - start_time
				print(f"Updated table {table_name} with {len(data)} rows in {total_time:.2f} seconds")


if __name__ == "__main__":
	main()