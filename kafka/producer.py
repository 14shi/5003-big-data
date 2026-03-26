import argparse
import csv
import json
import random
import time
from datetime import datetime

from kafka import KafkaProducer


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--bootstrap", required=True)
    parser.add_argument("--topic", default="taxi_events")
    parser.add_argument("--input_csv", required=True)
    parser.add_argument("--sleep", type=float, default=0.2)
    parser.add_argument("--max_rows", type=int, default=5000)
    return parser.parse_args()


def main():
    args = parse_args()
    producer = KafkaProducer(
        bootstrap_servers=args.bootstrap,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )

    sent = 0
    with open(args.input_csv, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            event = {
                "event_ts": datetime.utcnow().isoformat(),
                "pu_location_id": int(row.get("PULocationID", 0) or 0),
                "fare_amount": float(row.get("fare_amount", 0) or 0),
                "trip_distance": float(row.get("trip_distance", 0) or 0),
                "weather_tag": random.choice(["clear", "rain", "cloudy"]),
            }
            producer.send(args.topic, event)
            sent += 1
            if sent >= args.max_rows:
                break
            time.sleep(args.sleep)

    producer.flush()
    print(f"Sent {sent} events to topic {args.topic}")


if __name__ == "__main__":
    main()
