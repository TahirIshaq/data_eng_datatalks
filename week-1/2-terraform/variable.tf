# Variable of type local are like constants in other programming languages. They can not be changed on run time.
locals {
  data_lake_bucket = "dtc_data_lake"
}

# Vairables of type "variable" can be set/updated on runtime.
variable "project" {
  description = "Your GCP Project ID"
  default     = "algebraic-rider-395218"
  type        = string
}

variable "credentails" {
  description = "service account file path"
  default     = "algebraic-rider-395218-a9dcf88e7c6c.json"
}

variable "region" {
  description = "Region for GCP resources. Choose as per your location: https://cloud.google.com/about/locations"
  default     = "europe-west6"
  type        = string
}

variable "storage_class" {
  description = "Storage class type for your bucket. Check official docs for more info."
  default     = "STANDARD"
}

variable "BQ_DATASET" {
  description = "BigQuery Dataset that raw data (from GCS) will be written to"
  type        = string
  default     = "trips_data_all"
}