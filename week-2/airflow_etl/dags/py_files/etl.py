from sqlalchemy import create_engine
import time
import pandas as pd
import os


def download_dataset(url):
	"""Download the dataset, renames and returns the file"""
	file_name_start_idx = len(url) - url[::-1].find("/")
	file_new_name = url[file_name_start_idx:]
	os.system(f"wget {url} -O {file_new_name}")
	return file_new_name


def get_file_name_wo_ext(file_full_name):
	"""Returns the file name without extension"""
	name_end_idx = file_full_name.find(".")
	file_name = file_full_name[:name_end_idx]
	return file_name


def load_dataset(name, dtype=None, parse_dates=None):
	"""
	Loads the dataset and returns the pandas df
	The columns in parse_dates should be present in dtype
	"""
	df = pd.read_csv(name=name, dtype=dtype, parse_dates=parse_dates)
	return df


def transform_dataset(df, file_file):
	"""Transforms and returns the dataset. Current support: green and yellow taxi"""
	if "green" in file_file:
		df = df[df["passenger_count"] > 0]
		df["tpep_pickup_datetime"] = pd.to_datetime(df["tpep_pickup_datetime"])
		df["tpep_dropoff_datetime"] = pd.to_datetime(df["tpep_dropoff_datetime"])
	elif "yellow" in file_file:
		df = df[df["passenger_count"] > 0]
		df["lpep_pickup_datetime"] = pd.to_datetime(df["lpep_pickup_datetime"])
		df["lpep_dropoff_datetime"] = pd.to_datetime(df["lpep_dropoff_datetime"])
	else:
		pass
	return df


def main():
	username = os.getenv("DB_USERNAME")
	password = os.getenv("DB_PASSWORD")
	host = os.getenv("DB_HOST")
	port = os.getenv("DB_PORT")
	db_name = os.getenv("DB_NAME")
	urls = os.getenv("URL")

	db_login = f"postgresql://{username}:{password}@{host}:{port}/{db_name}"
	engine = create_engine(db_login)
	for url in urls.split(","):
		dataset_name = download_dataset(url)
		table_name = get_file_name_wo_ext(dataset_name)
		with engine.connect() as con:
