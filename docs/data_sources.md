# Real Data Sources

This project uses only real public datasets/APIs:

## 1) NYC Taxi Trip Records (Real)
- Source: NYC Open Data (Socrata)
- Endpoint: `https://data.cityofnewyork.us/resource/gkne-dk5s.csv`
- License/Access: Public open data API
- Usage in project:
  - `tpep_pickup_datetime`
  - `fare_amount`
  - `trip_distance`
  - `PULocationID`

## 2) NYC Historical Weather (Real)
- Source: Open-Meteo Historical Archive API
- Endpoint: `https://archive-api.open-meteo.com/v1/archive`
- Coordinates used: NYC (`40.7128, -74.0060`)
- Fields used:
  - hourly timestamp
  - temperature_2m
  - precipitation

## Reproducible Download Command
```bash
python scripts/download_data.py --taxi_rows 50000 --start_date 2024-01-01 --end_date 2024-01-31
```
