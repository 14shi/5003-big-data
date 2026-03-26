import argparse
import csv
import pathlib
from datetime import datetime
import requests

NYC_TAXI_API = "https://data.cityofnewyork.us/resource/gkne-dk5s.csv"
OPEN_METEO_API = "https://archive-api.open-meteo.com/v1/archive"


def download(url: str, output_path: pathlib.Path):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with requests.get(url, stream=True, timeout=60) as r:
        r.raise_for_status()
        with open(output_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)


def download_taxi_csv(output_path: pathlib.Path, rows: int = 50000):
    """
    Download real NYC Yellow Taxi records from NYC Open Data (Socrata).
    Normalize schema to match Spark job input.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    params = {"$limit": str(rows)}
    with requests.get(NYC_TAXI_API, params=params, timeout=120) as resp:
        resp.raise_for_status()
        raw_rows = list(csv.DictReader(resp.text.splitlines()))

    if not raw_rows:
        raise RuntimeError("No taxi rows returned from NYC Open Data API.")

    normalized_fields = [
        "tpep_pickup_datetime",
        "fare_amount",
        "trip_distance",
        "PULocationID",
    ]
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=normalized_fields)
        writer.writeheader()
        for row in raw_rows:
            pickup = row.get("tpep_pickup_datetime") or row.get("pickup_datetime")
            fare = row.get("fare_amount")
            dist = row.get("trip_distance")
            pu = row.get("pulocationid") or row.get("PULocationID")
            if not pickup or not fare or not dist or not pu:
                continue
            try:
                float(fare)
                float(dist)
                int(float(pu))
            except ValueError:
                continue
            writer.writerow(
                {
                    "tpep_pickup_datetime": pickup.replace("T", " ").replace("Z", ""),
                    "fare_amount": fare,
                    "trip_distance": dist,
                    "PULocationID": int(float(pu)),
                }
            )


def download_weather_csv(output_path: pathlib.Path, start_date: str, end_date: str):
    """
    Download real historical weather from Open-Meteo for NYC.
    Output schema: datetime, temperature, precipitation
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    params = {
        "latitude": "40.7128",
        "longitude": "-74.0060",
        "start_date": start_date,
        "end_date": end_date,
        "hourly": "temperature_2m,precipitation",
        "timezone": "UTC",
    }
    with requests.get(OPEN_METEO_API, params=params, timeout=120) as resp:
        resp.raise_for_status()
        payload = resp.json()

    hourly = payload.get("hourly", {})
    timestamps = hourly.get("time", [])
    temperatures = hourly.get("temperature_2m", [])
    precipitations = hourly.get("precipitation", [])

    if not timestamps:
        raise RuntimeError("No weather rows returned from Open-Meteo API.")

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["datetime", "temperature", "precipitation"])
        writer.writeheader()
        for ts, temp, precip in zip(timestamps, temperatures, precipitations):
            dt = datetime.fromisoformat(ts)
            writer.writerow(
                {
                    "datetime": dt.strftime("%Y-%m-%d %H:%M:%S"),
                    "temperature": temp if temp is not None else 0.0,
                    "precipitation": precip if precip is not None else 0.0,
                }
            )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir", default="data/raw")
    parser.add_argument("--taxi_rows", type=int, default=50000)
    parser.add_argument("--start_date", default="2024-01-01")
    parser.add_argument("--end_date", default="2024-01-31")
    args = parser.parse_args()

    data_dir = pathlib.Path(args.data_dir)
    taxi_file = data_dir / "taxi" / "yellow_tripdata_sample.csv"
    weather_file = data_dir / "weather" / "weather_sample.csv"

    print("Downloading real NYC taxi sample...")
    download_taxi_csv(taxi_file, rows=args.taxi_rows)

    print("Downloading real NYC weather sample...")
    download_weather_csv(weather_file, args.start_date, args.end_date)

    print(f"Done. Taxi: {taxi_file}")
    print(f"Done. Weather: {weather_file}")


if __name__ == "__main__":
    main()
