# Deployment Guide (GCP + Tableau)

## Prerequisites
- GCP account and project with billing enabled
- `gcloud`, `gsutil`, `bq` CLI installed
- Tableau Desktop or Tableau Public

## Step 1: Configure local environment
```bash
export PROJECT_ID=<your-gcp-project-id>
export REGION=us-central1
export ZONE=us-central1-a
export TEAM=<team-name>
```

## Step 2: Provision cloud resources
```bash
chmod +x scripts/gcp_setup.sh
./scripts/gcp_setup.sh
```

## Step 3: Upload datasets
```bash
gsutil cp data/raw/taxi/*.csv gs://bd5003-${TEAM}-raw-${PROJECT_ID}/raw/taxi/
gsutil cp data/raw/weather/*.csv gs://bd5003-${TEAM}-raw-${PROJECT_ID}/raw/weather/
```

## Step 4: Run batch Spark pipeline
```bash
gcloud dataproc jobs submit pyspark spark/jobs/batch_etl.py \
  --cluster=bd5003-spark-cluster \
  --region=${REGION} \
  -- \
  --input_taxi gs://bd5003-${TEAM}-raw-${PROJECT_ID}/raw/taxi/*.csv \
  --input_weather gs://bd5003-${TEAM}-raw-${PROJECT_ID}/raw/weather/*.csv \
  --output_bq ${PROJECT_ID}:mobility_analytics
```

## Step 5: Start Kafka and streaming job
1. SSH to Kafka VM and start Kafka/Zookeeper (single-node demo).
2. Run `kafka/producer.py` to emit events.
3. Submit streaming job:
```bash
gcloud dataproc jobs submit pyspark streaming/streaming_job.py \
  --cluster=bd5003-spark-cluster \
  --region=${REGION} \
  -- \
  --kafka_bootstrap <kafka-vm-ip>:9092 \
  --topic taxi_events \
  --output_bq ${PROJECT_ID}:mobility_analytics
```

## Step 6: Connect Tableau
- Connector: Google BigQuery
- Dataset: `mobility_analytics`
- Suggested tables:
  - `mart_trip_hourly`
  - `mart_zone_daily`
  - `rt_zone_5m`

## Step 7: Cost-saving shutdown
After demo/tests, run:
```bash
chmod +x scripts/gcp_teardown.sh
./scripts/gcp_teardown.sh
```
