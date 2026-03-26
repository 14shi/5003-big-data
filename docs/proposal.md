# Proposal - Wide Project

## 1. Task Description
This project builds a big-data analytics pipeline for urban mobility demand analysis using NYC Taxi and weather data. The system supports both historical analysis (batch) and near-real-time monitoring (streaming), then presents insights through Tableau dashboards.

Key analytics goals:
- Identify peak demand periods and geographic hotspots.
- Analyze fare distribution and demand-weather relationships.
- Provide short-window real-time demand indicators for operations monitoring.

## 2. Planned Datasets
### Dataset A: NYC Taxi Trip Records
- Type: Structured CSV/Parquet
- Fields used: pickup/dropoff timestamps, location IDs, fare amount, distance, passenger count
- Source: NYC TLC public records (sample or monthly subset)

### Dataset B: Historical Weather Data (NYC)
- Type: Structured CSV
- Fields used: datetime, temperature, precipitation, wind speed
- Source: NOAA/Kaggle weather datasets

### Streaming Data
- Type: Semi-structured JSON events
- Generated from sampled trip records and published to Kafka topic `taxi_events`.

## 3. Planned Technologies
- Apache Spark (RDD/Spark SQL/Structured Streaming)
- Kafka (real-time messaging)
- Google Cloud Dataproc (managed Spark runtime)
- Google Cloud Storage (raw/stage storage)
- BigQuery (analytical warehouse)
- Tableau (dashboard and service demo)

## 4. Brief Implementation Process
1. Ingest raw taxi and weather datasets into GCS.
2. Run Spark batch ETL on Dataproc:
   - data cleaning and schema normalization
   - join trip and weather by time window
   - aggregate metrics by hour/zone/day
3. Store curated tables into BigQuery.
4. Build Kafka producer that emits real-time trip events.
5. Run Spark Structured Streaming consumer:
   - compute 1-min and 5-min window metrics
   - output real-time tables to BigQuery
6. Connect Tableau to BigQuery and build dashboards:
   - operations overview
   - spatial demand heatmap
   - hourly trend and weather impact
   - near-real-time monitoring panel

## 5. Expected Deliverables
- Reproducible source code (batch + streaming + deployment scripts)
- System architecture diagram and implementation details
- Experiment section (throughput, latency, cost/performance observations)
- Tableau demo dashboard and presentation-ready screenshots

## 6. Why this is a good Wide Project
- Demonstrates synergy across more than three big-data technologies.
- Integrates multiple data forms (batch files + streaming events).
- Produces clear, demo-friendly UI with practical value.
