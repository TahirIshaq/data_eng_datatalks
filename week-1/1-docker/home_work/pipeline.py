import os
import time
import argparse
import pandas as pd
from sqlalchemy import create_engine

def get_args():
    """
    Returns the postgres credentials
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--username", default="tahir", help="DB username")
    parser.add_argument("--password", default="tahir", help="DB password")
    parser.add_argument("--host", default="localhost", help="DB host")
    parser.add_argument("--port", default="5432", help="DB port")
    parser.add_argument("--db_name", default="ny_taxi", help="DB name")
    parser.add_argument("--url", default=None, help="Dataset URL")
    parser.add_argument("--dataset", default=None, help="Dataset name")
    parser.add_argument("--compression", default="", help="Dataset compression")
    parser.add_argument("--table_name", default="yellow_taxi", help="Table name")
    parser.add_argument("--col_names", nargs="*", help="Column names")
    parser.add_argument("--col_datatypes", nargs="*", help="Column data types")

    args = parser.parse_args()
    return args


def download_dataset(url, file_name, compression):
    """
    Downloads the dataset and extracts if required.
    
    url(str): URL of the dataset
    file_name(str): New name of the dataset
    compressed(bool): If the file compressed or not.
    """
    os.system("wget {} -O {}{}".format(url, file_name, compression))
    if compression == ".gz":
        os.system("gunzip {}{}".format(file_name, compression))


def load_dataset(name, nrows=None, iterator=False, chunksize=None):
    """
    Load the dataset and return the pandas dataframe

    name(str): Name of the dataset
    nrows(int): How many rows to read. None by default
    iterator(Bool): Iterate over the dataset. False by default
    chunksize(int): Data size over each iteration
    """
    df = pd.read_csv(name, nrows=nrows, iterator=iterator, chunksize=chunksize)
    return df


def connect_database(user, password, host, port, db_name):
    """
    Connects to the postgres server and returns the connection reference.
    
    user(str): Db username
    password(str): Password of the db
    host(str): URL of the database server
    port(str): Port number of the database server
    db_name(str): Name of the database/relation
    """
    engine = create_engine("postgresql://{}:{}@{}:{}/{}".format(user, password, host, port, db_name))
    engine.connect()
    return engine


def update_datatype(df, col_name, datatype):
    """
    Updates the column data type of the pandas dataframe
    
    df(pd.dataframe): Pandas data frame
    col_name(list): Names of the column
    datatype(list): New data types of the columns
    """
    # for index, _ in enumerate(col_name):
    for index in range(len(col_name)):
        if col_name[index] in ("datetime", "timestamp"):
            df[col_name[index]] = pd.to_datetime(df[col_name[index]])


def insert_in_database(df, table_name, con, operation):
    """
    Coverts the pandas dataframe to sql query and executes it

    df(pd.Dataframe): Pandas dataframe
    table_name(str): Table name in which data is to inserted.
    con(): Postgres server reference
    operation(str): Query operation.(Append, replace)
    """
    df.to_sql(name=table_name, con=con, if_exists=operation)


def main():
    """
    Main function
    """
    args = get_args()

    username = args.username
    password = args.password
    host = args.host
    port = args.port
    db_name = args.db_name
    url = args.url
    table_name = args.table_name
    dataset = args.dataset
    compression = args.compression
    col_names = args.col_names
    col_datatypes = args.col_datatypes

    download_dataset(url, dataset, compression)
    df = load_dataset(dataset, nrows=100)
    # Updating column data type should be optional
    if col_names and col_datatypes:
        update_datatype(df, col_names, col_datatypes)
    engine = connect_database(username, password, host, port, db_name)
    insert_in_database(df.head(n=0), table_name, engine, "replace")
    df_iter = load_dataset(dataset, iterator=True, chunksize=100000)
    for data in df_iter:
        start_time = time.time()
        if col_names and col_datatypes:
            update_datatype(data, col_names, col_datatypes)
        insert_in_database(data, table_name, engine, "append")
        end_time = time.time() - start_time
        print("Datachunk inserted in {:.2f} seconds".format(end_time))

if __name__ == "__main__":
    main()