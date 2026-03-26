# 5003 Big Data - Wide Project (GCP + Tableau)

This repository now includes a runnable coursework scaffold for:
- Spark batch analytics on Dataproc
- Kafka + Spark Structured Streaming pipeline
- BigQuery analytical tables
- Tableau dashboard delivery

## Start Here
- End-to-end runbook: `docs/runbooks/e2e_quickstart.md`
- Deployment details: `docs/deployment_guide.md`

## Data
Use automatic downloader:
```bash
python scripts/download_data.py
```
This fetches publicly available sample datasets into `data/raw/`.

## Key Files
- `spark/jobs/batch_etl.py`
- `streaming/streaming_job.py`
- `kafka/producer.py`
- `scripts/gcp_setup.sh`
- `scripts/gcp_teardown.sh`
- `scripts/kafka/install_kafka_vm.sh`
- `scripts/kafka/start_kafka_vm.sh`
- `sql/bigquery_tables.sql`
- `tableau/dashboard_spec.md`

## Local sanity check
```bash
./scripts/run_smoke_checks.sh
```
