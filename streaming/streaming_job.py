import argparse
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType, TimestampType


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--kafka_bootstrap", required=True)
    parser.add_argument("--topic", required=True)
    parser.add_argument("--output_bq", required=True, help="project:dataset")
    parser.add_argument("--checkpoint", default="/tmp/bd5003/checkpoint")
    return parser.parse_args()


def main():
    args = parse_args()

    spark = SparkSession.builder.appName("bd5003-streaming").getOrCreate()

    schema = StructType([
        StructField("event_ts", TimestampType(), True),
        StructField("pu_location_id", IntegerType(), True),
        StructField("fare_amount", DoubleType(), True),
        StructField("trip_distance", DoubleType(), True),
        StructField("weather_tag", StringType(), True),
    ])

    raw = (
        spark.readStream.format("kafka")
        .option("kafka.bootstrap.servers", args.kafka_bootstrap)
        .option("subscribe", args.topic)
        .option("startingOffsets", "latest")
        .load()
    )

    parsed = (
        raw.select(F.from_json(F.col("value").cast("string"), schema).alias("data"))
        .select("data.*")
        .filter(F.col("event_ts").isNotNull())
    )

    windowed = (
        parsed.withWatermark("event_ts", "10 minutes")
        .groupBy(
            F.window("event_ts", "5 minutes", "1 minute"),
            F.col("pu_location_id"),
        )
        .agg(
            F.count("*").alias("trip_count"),
            F.avg("fare_amount").alias("avg_fare"),
            F.avg("trip_distance").alias("avg_distance"),
        )
        .select(
            F.col("window.start").alias("window_start"),
            F.col("window.end").alias("window_end"),
            "pu_location_id",
            "trip_count",
            "avg_fare",
            "avg_distance",
        )
    )

    bq_project, bq_dataset = args.output_bq.split(":")
    table_fqn = f"{bq_project}.{bq_dataset}.rt_zone_5m"

    def write_to_bq(batch_df, _):
        (
            batch_df.write.format("bigquery")
            .option("table", table_fqn)
            .mode("append")
            .save()
        )

    query = (
        windowed.writeStream.outputMode("update")
        .option("checkpointLocation", args.checkpoint)
        .foreachBatch(write_to_bq)
        .start()
    )

    query.awaitTermination()


if __name__ == "__main__":
    main()
