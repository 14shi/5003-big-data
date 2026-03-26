import argparse
import csv
import random
import pathlib
from datetime import datetime, timedelta
import requests

# Public sample datasets for coursework-friendly quick start.
SOURCES = {
    "taxi": "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-01.parquet",
    "weather": "https://raw.githubusercontent.com/vega/vega-datasets/master/data/weather.csv",
}


def download(url: str, output_path: pathlib.Path):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with requests.get(url, stream=True, timeout=60) as r:
        r.raise_for_status()
        with open(output_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)


def generate_taxi_csv(output_path: pathlib.Path, rows: int = 5000):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "tpep_pickup_datetime",
        "fare_amount",
        "trip_distance",
        "PULocationID",
    ]
    start = datetime(2024, 1, 1, 0, 0, 0)
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for i in range(rows):
            ts = start + timedelta(minutes=i * 3)
            writer.writerow(
                {
                    "tpep_pickup_datetime": ts.strftime("%Y-%m-%d %H:%M:%S"),
                    "fare_amount": round(random.uniform(5.0, 60.0), 2),
                    "trip_distance": round(random.uniform(0.5, 25.0), 2),
                    "PULocationID": random.randint(1, 265),
                }
            )


def ensure_weather_schema(input_path: pathlib.Path, output_path: pathlib.Path):
    """Normalize weather data to required columns: datetime, temperature, precipitation."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(input_path, "r", encoding="utf-8") as src, open(
        output_path, "w", newline="", encoding="utf-8"
    ) as dst:
        reader = csv.DictReader(src)
        fieldnames = ["datetime", "temperature", "precipitation"]
        writer = csv.DictWriter(dst, fieldnames=fieldnames)
        writer.writeheader()
        written = 0
        for row in reader:
            # Vega weather.csv has columns: date, precipitation, temp_max, temp_min, wind, weather
            dt_raw = row.get("date")
            if not dt_raw:
                continue
            try:
                dt = datetime.fromisoformat(dt_raw.replace("Z", ""))
            except ValueError:
                continue
            temp_max = row.get("temp_max")
            temp_min = row.get("temp_min")
            try:
                if temp_max is not None and temp_min is not None:
                    temp = (float(temp_max) + float(temp_min)) / 2.0
                else:
                    temp = float(row.get("temperature", "0"))
            except ValueError:
                temp = 0.0
            try:
                precip = float(row.get("precipitation", "0"))
            except ValueError:
                precip = 0.0
            writer.writerow(
                {
                    "datetime": dt.strftime("%Y-%m-%d %H:%M:%S"),
                    "temperature": round(temp, 3),
                    "precipitation": round(precip, 3),
                }
            )
            written += 1
        if written == 0:
            # Fallback minimal synthetic weather rows
            base = datetime(2024, 1, 1)
            for i in range(365):
                writer.writerow(
                    {
                        "datetime": (base + timedelta(days=i)).strftime("%Y-%m-%d 00:%M:%S"),
                        "temperature": round(random.uniform(-5, 35), 2),
                        "precipitation": round(max(0, random.gauss(2, 3)), 2),
                    }
                )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir", default="data/raw")
    args = parser.parse_args()

    data_dir = pathlib.Path(args.data_dir)
    taxi_file = data_dir / "taxi" / "yellow_tripdata_sample.csv"
    weather_file = data_dir / "weather" / "weather_sample.csv"

    print("Preparing taxi sample...")
    # Use synthetic CSV by default to match Spark schema exactly.
    # (TLC official source is parquet and can be large for first-time setup.)
    generate_taxi_csv(taxi_file)

    print("Downloading weather sample...")
    weather_raw = data_dir / "weather" / "weather_raw.csv"
    download(SOURCES["weather"], weather_raw)
    ensure_weather_schema(weather_raw, weather_file)

    print(f"Done. Taxi: {taxi_file}")
    print(f"Done. Weather: {weather_file}")


if __name__ == "__main__":
    main()
