import argparse
from pyspark.sql import SparkSession
from pyspark.sql import functions as F


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_taxi", required=True)
    parser.add_argument("--input_weather", required=True)
    parser.add_argument("--output_bq", required=True, help="project:dataset")
    parser.add_argument(
        "--temp_gcs_bucket",
        required=True,
        help="GCS bucket name (without gs://) for BigQuery temporary data",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    spark = SparkSession.builder.appName("bd5003-batch-etl").getOrCreate()

    taxi = (
        spark.read.option("header", True).csv(args.input_taxi)
        .withColumn("pickup_datetime", F.to_timestamp("tpep_pickup_datetime"))
        .withColumn("fare_amount", F.col("fare_amount").cast("double"))
        .withColumn("trip_distance", F.col("trip_distance").cast("double"))
        .withColumn("PULocationID", F.col("PULocationID").cast("int"))
        .filter(F.col("pickup_datetime").isNotNull())
    )

    weather = (
        spark.read.option("header", True).csv(args.input_weather)
        .withColumn("weather_ts", F.to_timestamp("datetime"))
        .withColumn("temperature", F.col("temperature").cast("double"))
        .withColumn("precipitation", F.col("precipitation").cast("double"))
        .filter(F.col("weather_ts").isNotNull())
    )

    taxi_hourly = taxi.withColumn("hour_bucket", F.date_trunc("hour", F.col("pickup_datetime")))
    weather_hourly = weather.withColumn("hour_bucket", F.date_trunc("hour", F.col("weather_ts")))

    joined = taxi_hourly.join(weather_hourly, on="hour_bucket", how="left")

    mart_trip_hourly = (
        joined.groupBy("hour_bucket")
        .agg(
            F.count("*").alias("trip_count"),
            F.avg("fare_amount").alias("avg_fare"),
            F.avg("trip_distance").alias("avg_distance"),
            F.avg("temperature").alias("avg_temperature"),
            F.avg("precipitation").alias("avg_precipitation"),
        )
        .orderBy("hour_bucket")
    )

    mart_zone_daily = (
        taxi.withColumn("trip_date", F.to_date("pickup_datetime"))
        .groupBy("trip_date", "PULocationID")
        .agg(
            F.count("*").alias("trip_count"),
            F.avg("fare_amount").alias("avg_fare"),
        )
        .orderBy("trip_date", "PULocationID")
    )

    bq_project, bq_dataset = args.output_bq.split(":")

    (
        mart_trip_hourly.write.format("bigquery")
        .option("table", f"{bq_project}.{bq_dataset}.mart_trip_hourly")
        .option("temporaryGcsBucket", args.temp_gcs_bucket)
        .mode("overwrite")
        .save()
    )

    (
        mart_zone_daily.write.format("bigquery")
        .option("table", f"{bq_project}.{bq_dataset}.mart_zone_daily")
        .option("temporaryGcsBucket", args.temp_gcs_bucket)
        .mode("overwrite")
        .save()
    )

    spark.stop()


if __name__ == "__main__":
    main()
