# GCP Architecture Mapping (Wide Project)

## Services Mapping

| Layer | Technology | GCP Service | Purpose |
|---|---|---|---|
| Data Lake | Object Storage | Cloud Storage (GCS) | Store raw taxi/weather files and staged outputs |
| Batch Compute | Spark SQL / RDD | Dataproc | ETL and historical analytics |
| Streaming Ingest | Messaging | Kafka (single VM for demo) | Simulate and process real-time taxi events |
| Stream Compute | Spark Structured Streaming | Dataproc / Spark client | Windowed metrics and anomaly signals |
| Analytical Warehouse | SQL Analytics | BigQuery | Curated analytics tables and dashboard source |
| Visualization | BI Dashboard | Tableau | Final UI/demo and business storytelling |

## Proposed Data Flow
1. Upload raw datasets to `gs://<bucket>/raw/`.
2. Run Spark batch job on Dataproc to clean/join taxi + weather data.
3. Write curated historical outputs to BigQuery (`mart_trip_hourly`, `mart_zone_daily`).
4. Run Kafka producer to publish simulated trip events.
5. Spark streaming job consumes Kafka topic and writes window metrics to BigQuery (`rt_zone_5m`).
6. Tableau connects to BigQuery for dashboard pages (overview, heatmap, trend, realtime).

## Cost-Conscious Topology (<100 USD)
- Dataproc single-node or 1 master + 2 small workers (only when running jobs).
- Kafka on one e2-small VM for short demo window.
- BigQuery with partitioned tables and limited scans.
- Shut down/delete transient resources immediately after experiments.

## Naming Convention
- Project: `<gcp_project_id>`
- Region: `us-central1`
- Bucket: `bd5003-<team>-raw`
- Dataset: `mobility_analytics`
- Dataproc cluster: `bd5003-spark-cluster`
- Kafka topic: `taxi_events`

## Security and Access
- Use service account with minimum required roles:
  - `roles/storage.objectAdmin`
  - `roles/bigquery.dataEditor`
  - `roles/dataproc.editor`
- Avoid embedding keys in code; use ADC or VM-attached service account.
