# End-to-End Quickstart (Entity Deployment First)

## 0) Local setup
```bash
chmod +x scripts/bootstrap_local.sh scripts/run_smoke_checks.sh
./scripts/bootstrap_local.sh
source .venv/bin/activate
./scripts/run_smoke_checks.sh
```

## 1) Download sample datasets automatically
```bash
python scripts/download_data.py
```
Outputs:
- `data/raw/taxi/yellow_tripdata_sample.csv`
- `data/raw/weather/weather_sample.csv`

## 2) Provision GCP resources
```bash
export PROJECT_ID=<your-project-id>
export REGION=us-central1
export ZONE=us-central1-a
export TEAM=<team-name>
chmod +x scripts/gcp_setup.sh
./scripts/gcp_setup.sh
```

## 3) Upload datasets to GCS
```bash
gsutil cp data/raw/taxi/*.csv gs://bd5003-${TEAM}-raw-${PROJECT_ID}/raw/taxi/
gsutil cp data/raw/weather/*.csv gs://bd5003-${TEAM}-raw-${PROJECT_ID}/raw/weather/
```

## 4) Run batch job
```bash
gcloud dataproc jobs submit pyspark spark/jobs/batch_etl.py \
  --cluster=bd5003-spark-cluster --region=${REGION} -- \
  --input_taxi gs://bd5003-${TEAM}-raw-${PROJECT_ID}/raw/taxi/*.csv \
  --input_weather gs://bd5003-${TEAM}-raw-${PROJECT_ID}/raw/weather/*.csv \
  --output_bq ${PROJECT_ID}:mobility_analytics
```

## 5) Install/start Kafka on VM
Copy scripts to VM and run:
```bash
chmod +x install_kafka_vm.sh start_kafka_vm.sh
./install_kafka_vm.sh
./start_kafka_vm.sh
```

## 6) Run producer and streaming
```bash
python kafka/producer.py --bootstrap <kafka-vm-ip>:9092 --topic taxi_events --input_csv data/raw/taxi/yellow_tripdata_sample.csv --max_rows 2000

gcloud dataproc jobs submit pyspark streaming/streaming_job.py \
  --cluster=bd5003-spark-cluster --region=${REGION} -- \
  --kafka_bootstrap <kafka-vm-ip>:9092 --topic taxi_events \
  --output_bq ${PROJECT_ID}:mobility_analytics
```

## 7) Tableau
Connect BigQuery dataset `mobility_analytics` and build dashboards per `tableau/dashboard_spec.md`.

## 8) Teardown
```bash
chmod +x scripts/gcp_teardown.sh
./scripts/gcp_teardown.sh
```
