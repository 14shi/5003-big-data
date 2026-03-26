import argparse
import os
import pathlib
import requests

# Public sample datasets for coursework-friendly quick start.
SOURCES = {
    "taxi": "https://raw.githubusercontent.com/toddwschneider/nyc-taxi-data/master/data-samples/yellow_tripdata_2016-01_sample.csv",
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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir", default="data/raw")
    args = parser.parse_args()

    data_dir = pathlib.Path(args.data_dir)
    taxi_file = data_dir / "taxi" / "yellow_tripdata_sample.csv"
    weather_file = data_dir / "weather" / "weather_sample.csv"

    print("Downloading taxi sample...")
    download(SOURCES["taxi"], taxi_file)

    print("Downloading weather sample...")
    download(SOURCES["weather"], weather_file)

    print(f"Done. Taxi: {taxi_file}")
    print(f"Done. Weather: {weather_file}")


if __name__ == "__main__":
    main()
