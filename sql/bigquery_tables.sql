-- Reference DDL for BigQuery tables

CREATE TABLE IF NOT EXISTS `PROJECT_ID.mobility_analytics.mart_trip_hourly` (
  hour_bucket TIMESTAMP,
  trip_count INT64,
  avg_fare FLOAT64,
  avg_distance FLOAT64,
  avg_temperature FLOAT64,
  avg_precipitation FLOAT64
)
PARTITION BY DATE(hour_bucket);

CREATE TABLE IF NOT EXISTS `PROJECT_ID.mobility_analytics.mart_zone_daily` (
  trip_date DATE,
  PULocationID INT64,
  trip_count INT64,
  avg_fare FLOAT64
)
PARTITION BY trip_date
CLUSTER BY PULocationID;

CREATE TABLE IF NOT EXISTS `PROJECT_ID.mobility_analytics.rt_zone_5m` (
  window_start TIMESTAMP,
  window_end TIMESTAMP,
  pu_location_id INT64,
  trip_count INT64,
  avg_fare FLOAT64,
  avg_distance FLOAT64
)
PARTITION BY DATE(window_start)
CLUSTER BY pu_location_id;
