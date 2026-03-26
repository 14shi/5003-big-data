# 5003 Big Data - Wide Project (GCP + Tableau)

This repository implements a full Wide Project pipeline:
- Batch analytics with Spark on Dataproc
- Streaming analytics with Kafka + Spark Structured Streaming
- Warehouse storage in BigQuery
- Dashboard visualization in Tableau

## Project Structure
- `docs/topic_selection.md`: Final track/topic confirmation
- `docs/proposal.md`: Proposal draft aligned with course requirements
- `architecture/gcp_architecture.md`: Service mapping and architecture
- `docs/deployment_guide.md`: End-to-end deployment steps
- `spark/jobs/batch_etl.py`: Batch ETL and aggregations
- `streaming/streaming_job.py`: Streaming windowed aggregations
- `kafka/producer.py`: Demo event producer
- `sql/bigquery_tables.sql`: Reference SQL for table creation
- `tableau/dashboard_spec.md`: Dashboard specification
- `docs/experiment_plan.md`: Metrics and evaluation plan
- `docs/cost_risk_checklist.md`: Budget and risk controls
- `scripts/gcp_setup.sh`: Provision infra
- `scripts/gcp_teardown.sh`: Destroy infra

## Quick Start
1. Follow `docs/deployment_guide.md`.
2. Deploy resources with `scripts/gcp_setup.sh`.
3. Run batch + streaming jobs.
4. Connect Tableau to BigQuery tables.

## Notes
This project is intentionally scoped for a course setting, prioritizing reproducibility, low cost, and clear demonstration value.
