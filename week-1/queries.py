# https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/cohorts/2024/01-docker-terraform/homework.md
query1 = """
	SELECT 
		COUNT(1) AS total_trips
	FROM
		"green_tripdata_2019-09"
	WHERE
		DATE(lpep_pickup_datetime)='2019-09-18' AND
		DATE(lpep_dropoff_datetime)='2019-09-18'
	GROUP BY
		DATE(lpep_pickup_datetime);
"""

query2 = """
SELECT
	DATE(lpep_pickup_datetime) AS max_trip_day
FROM
	"green_tripdata_2019-09"
GROUP BY
	max_trip_day
ORDER BY
	MAX(trip_distance) DESC
LIMIT
	1;
"""

query3 = """
SELECT
	taxi_zone."Borough",
	SUM(green_taxi.total_amount) AS sum_total
FROM
	"green_tripdata_2019-09" AS green_taxi
	JOIN
	taxi_zone_lookup AS taxi_zone
	ON
	green_taxi."PULocationID"=taxi_zone."LocationID"::INT
	WHERE taxi_zone."Borough" != 'Unknown'
	AND
	DATE(green_taxi.lpep_pickup_datetime)='2019-09-18'
GROUP BY
	taxi_zone."Borough"
HAVING
	SUM(green_taxi.total_amount) > 50000;
"""

query4_0 = """
SELECT
	COUNT(1) AS total_count
FROM
	"green_tripdata_2019-09"
WHERE
	DATE(lpep_pickup_datetime) BETWEEN '2019-09-01' AND '2019-09-30';
"""

query4_1 = """
SELECT
	"Zone"
FROM
	taxi_zone_lookup
WHERE
	"LocationID"::INT = 132;
"""

query4_2 = """
WITH zones AS
(
	SELECT
		"LocationID"
	FROM
		taxi_zone_lookup
	WHERE
		"Zone" = 'Astoria'
)

"""

query4_3 = """
SELECT
	"DOLocationID"
FROM
	"green_tripdata_2019-09"
WHERE
	DATE(lpep_pickup_datetime) BETWEEN '2019-09-01' AND '2019-09-30'
	AND
	"PULocationID" = 7
GROUP BY
	"DOLocationID"
ORDER BY
	MAX(tip_amount) DESC
LIMIT
	1;
"""

query4 = """
SELECT
	"Zone"
FROM
	taxi_zone_lookup
WHERE
	"LocationID"::INT = 
						(SELECT
							"DOLocationID"
						FROM
							"green_tripdata_2019-09"
						WHERE
							DATE(lpep_pickup_datetime) BETWEEN '2019-09-01' AND '2019-09-30'
							AND
							"PULocationID" = (
												SELECT
													"LocationID"::INT
												FROM
													taxi_zone_lookup
												WHERE
													"Zone" = 'Astoria'
											)
						GROUP BY
							"DOLocationID"
						ORDER BY
							MAX(tip_amount) DESC
						LIMIT
							1
						);
"""