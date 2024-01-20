# Homework Solution

## Docker & SQL

In this homework we'll prepare the environment 
and practice with Docker and SQL


## Question 1. Knowing docker tags

Run the command to get information on Docker 

```docker --help```

Now run the command to get help on the "docker build" command:

```docker build --help```

Do the same for "docker run".

Which tag has the following text? - *Automatically remove the container when it exits* 

```
$ docker run --help | grep "Automatically remove"
      --rm                             Automatically remove the
```


## Question 2. Understanding docker first run 

Run docker with the python:3.9 image in an interactive mode and the entrypoint of bash.
Now check the python modules that are installed ( use ```pip list``` ). 

What is version of the package *wheel* ?

```
$ pip list | grep wheel
wheel                     0.41.2
```


# Prepare Postgres

Run Postgres and load data as shown in the videos
We'll use the green taxi trips from September 2019:

```wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-09.csv.gz```

You will also need the dataset with zones:

```wget https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv```

Download this data and put it into Postgres (with jupyter notebooks or with a pipeline)


## Question 3. Count records 

How many taxi trips were totally made on September 18th 2019?

```
ny_taxi=# select count(*) from green_taxi_2 where date(lpep_pickup_datetime) = '2019-09-18' and date(lpep_dropoff_datetime)='2019-09-18';
 count 
-------
 15612
(1 row)
```

## Question 4. Largest trip for each day

Which was the pick up day with the largest trip distance
Use the pick up time for your calculations.

```
ny_taxi=# select date(lpep_pickup_datetime) as long_day, max(trip_distance) as distance from green_taxi_2 group by long_day order by distance desc limit 1;
  long_day  | distance 
------------+----------
 2019-09-26 |   341.64
(1 row)
```


## Question 5. Three biggest pick up Boroughs

Consider lpep_pickup_datetime in '2019-09-18' and ignoring Borough has Unknown

Which were the 3 pick up Boroughs that had a sum of total_amount superior to 50000?
 
```
ny_taxi=# select "Borough", sum(total_amount)  as today from green_taxi_2 join taxi_zone on "PULocationID"="LocationID"::int and date(lpep_pickup_datetime) = '2019-09-18' group by "Borough" order by today desc limit 3;
  Borough  |       today       
-----------+-------------------
 Brooklyn  | 96333.24000000028
 Manhattan | 92271.29999999984
 Queens    | 78671.70999999935
(3 rows)


ny_taxi=# select "Borough", sum(total_amount) from green_taxi_2 join taxi_zone on "PULocationID"="LocationID"::int and date(lpep_pickup_datetime) = '2019-09-18' group by "Borough" having sum(total_amount) > 50000;
  Borough  |        sum        
-----------+-------------------
 Brooklyn  | 96333.23999999944
 Manhattan | 92271.29999999887
 Queens    | 78671.70999999899
(3 rows)
```


## Question 6. Largest tip

For the passengers picked up in September 2019 in the zone name Astoria which was the drop off zone that had the largest tip?
We want the name of the zone, not the id.

Note: it's not a typo, it's `tip` , not `trip`

```
ny_taxi=# select "Zone" FROM (select "DOLocationID" from green_taxi_2 where tip_amount = (select max(tip_amount) from green_taxi_2 where "PULocationID"=7 and DATE(lpep_pickup_datetime)::text LIKE '2019-09-%')) as dol JOIN taxi_zone on "DOLocationID"="LocationID"::int;
    Zone     
-------------
 JFK Airport
(1 row)
```


## Terraform

In this section homework we'll prepare the environment by creating resources in GCP with Terraform.

In your VM on GCP/Laptop/GitHub Codespace install Terraform. 
Copy the files from the course repo
[here](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/01-docker-terraform/1_terraform_gcp/terraform) to your VM/Laptop/GitHub Codespace.

Modify the files as necessary to create a GCP Bucket and Big Query Dataset.


## Question 7. Creating Resources

After updating the main.tf and variable.tf files run:

```
terraform apply
```

Paste the output of this command into the homework submission form.

```
$ terraform apply

Terraform used the selected providers to generate the following execution plan.
Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # google_bigquery_dataset.demo_dataset will be created
  + resource "google_bigquery_dataset" "demo_dataset" {
      + creation_time              = (known after apply)
      + dataset_id                 = "demo_dataset"
      + default_collation          = (known after apply)
      + delete_contents_on_destroy = false
      + effective_labels           = (known after apply)
      + etag                       = (known after apply)
      + id                         = (known after apply)
      + is_case_insensitive        = (known after apply)
      + last_modified_time         = (known after apply)
      + location                   = "US"
      + max_time_travel_hours      = (known after apply)
      + project                    = "wise-coyote-411413"
      + self_link                  = (known after apply)
      + storage_billing_model      = (known after apply)
      + terraform_labels           = (known after apply)
    }

  # google_storage_bucket.demo-bucket will be created
  + resource "google_storage_bucket" "demo-bucket" {
      + effective_labels            = (known after apply)
      + force_destroy               = true
      + id                          = (known after apply)
      + location                    = "US"
      + name                        = "terraform-demo-terra-bucket-1232432-234234234-234"
      + project                     = (known after apply)
      + public_access_prevention    = (known after apply)
      + rpo                         = (known after apply)
      + self_link                   = (known after apply)
      + storage_class               = "STANDARD"
      + terraform_labels            = (known after apply)
      + uniform_bucket_level_access = (known after apply)
      + url                         = (known after apply)

      + lifecycle_rule {
          + action {
              + type = "AbortIncompleteMultipartUpload"
            }
          + condition {
              + age                   = 1
              + matches_prefix        = []
              + matches_storage_class = []
              + matches_suffix        = []
              + with_state            = (known after apply)
            }
        }
    }

Plan: 2 to add, 0 to change, 0 to destroy.

Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value: yes

google_bigquery_dataset.demo_dataset: Creating...
google_storage_bucket.demo-bucket: Creating...
google_storage_bucket.demo-bucket: Creation complete after 2s [id=terraform-demo-terra-bucket-1232432-234234234-234]
google_bigquery_dataset.demo_dataset: Creation complete after 3s [id=projects/wise-coyote-411413/datasets/demo_dataset]

```