import os
import time
import argparse
from sqlalchemy import create_engine
import pandas as pd


def get_args():
    """Returns postgres credentials"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--user", default="tahir", help="DB username")
    parser.add_argument("--password", default="tahir", help="DB password")
    parser.add_argument("--host", default="localhost", help="DB host")
    parser.add_argument("--port", default="5432", help="DB port")
    parser.add_argument("--db", default="ny_taxi", help="DB name")
    parser.add_argument("--table_name", default="yellow_taxi", help="Table name")
    parser.add_argument("--dataset", default="dataset.csv", help="Dataset")
    parser.add_argument("--url", default=None, help="Dataset URL")

    return parser.parse_args()


def connect_database(username, password, host, port, db_name):
    """Connects to the database and returns the connection"""
    engine = create_engine("postgresql://{}:{}@{}:{}/{}".format(username, password, host, port, db_name))
    engine.connect()
    return engine


def read_dataset(dataset, nrows=None, iterator=None, chunksize=None):
    """Loads the dataset and returns its handle"""
    df = pd.read_csv(dataset, nrows=nrows, iterator=iterator, chunksize=chunksize)
    return df


def download_dataset(url, dataset):
    """Downloads and extracts the dataset"""
    os.system("wget {} -O {}.gz".format(url, dataset))
    os.system("gunzip {}.gz".format(dataset))


def main():
    """The main function"""
    # Initialize database arguments
    args = get_args()
    username = args.user
    password = args.password
    host = args.host
    port = args.port
    db_name = args.db
    table_name = args.table_name
    dataset = args.dataset
    url = args.url

    download_dataset(url, dataset)
    df = read_dataset(dataset, nrows=10)

    engine = connect_database(username, password, host, port, db_name)

    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
    
    df.head(n=0).to_sql(name=table_name, con=engine, if_exists="replace")

    df_iter = read_dataset(dataset, iterator=True, chunksize=100000)

    for data in df_iter:
        start_time = time.time()
        data.tpep_pickup_datetime = pd.to_datetime(data.tpep_pickup_datetime)
        data.tpep_dropoff_datetime = pd.to_datetime(data.tpep_dropoff_datetime)
        data.to_sql(name=table_name, con=engine, if_exists="append")
        end_time = time.time() - start_time
        print("Chunk inserted in table in {:.2f} seconds".format(end_time))


if __name__ == "__main__":
    main()