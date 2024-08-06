import pandas as pd

# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.dtypes.html
# https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv
# https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-09.csv.gz
# https://www.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf
# https://www.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_green.pdf

green_taxi_data_types_test = {
	"VendorID": pd.Int64Dtype(),
	"Passenger_count": pd.Int64Dtype(),
	"Trip_distance": pd.Float64Dtype(),
	"PULocationID": pd.Int64Dtype(),
	"DOLocationID": pd.Int64Dtype(),
	"RateCodeID": pd.Int64Dtype(),
	"Store_and_fwd_flag": "object",
	"Payment_type": pd.Int64Dtype(),
	"Fare_amount": pd.Float64Dtype(),
	"Extra": pd.Float64Dtype(),
	"MTA_tax": pd.Float64Dtype(),
	"Improvement_surcharge": pd.Float64Dtype(),
	"Tip_amount": pd.Float64Dtype(),
	"Tolls_amount": pd.Float64Dtype(),
	"Total_amount": pd.Float64Dtype(),
	"Trip_type": pd.Int64Dtype()
}

green_taxi_data_types = {
	"VendorID": "int64",
	"Passenger_count": "int64",
	"Trip_distance": "float64",
	"PULocationID": "int64",
	"DOLocationID": "int64",
	"RateCodeID": "int64",
	"Store_and_fwd_flag": "object",
	"Payment_type": "int64",
	"Fare_amount": "float64",
	"Extra": "float64",
	"MTA_tax": "float64",
	"Improvement_surcharge": "float64",
	"Tip_amount": "float64",
	"Tolls_amount": "float64",
	"Total_amount": "float64",
	"Trip_type": "int64"
}
green_taxi_datetime = ["lpep_pickup_datetime", "lpep_dropoff_datetime"]

yellow_taxi_data_types = {
	"VendorID": "int64",
	"Passenger_count": "int64",
	"Trip_distance": "float64",
	"PULocationID": "int64",
	"DOLocationID": "int64",
	"RateCodeID": "int64",
	"Store_and_fwd_flag": "object",
	"Payment_type": "int64",
	"Fare_amount": "float64",
	"Extra": "float64",
	"MTA_tax": "float64",
	"Improvement_surcharge": "float64",
	"Tip_amount": "float64",
	"Tolls_amount": "float64",
	"Total_amount": "float64",
	"Congestion_Surcharge": "float64",
	"Airport_fee": "float64"
}
yellow_taxi_datetime = ["tpep_pickup_datetime", "tpep_dropoff_datetime"]

taxi_zone = {
	"LocationID": pd.Int64Dtype(),
	"Borough": "object",
	"Zone": "object",
	"service_zone": "object"
}