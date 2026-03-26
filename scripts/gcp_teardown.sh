#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   PROJECT_ID=your-project-id TEAM=team1 ./scripts/gcp_teardown.sh

PROJECT_ID="${PROJECT_ID:?PROJECT_ID is required}"
REGION="${REGION:-us-central1}"
ZONE="${ZONE:-us-central1-a}"
TEAM="${TEAM:-team1}"
BUCKET="bd5003-${TEAM}-raw-${PROJECT_ID}"
BQ_DATASET="mobility_analytics"
CLUSTER="bd5003-spark-cluster"
KAFKA_VM="bd5003-kafka-vm"

gcloud config set project "${PROJECT_ID}"

gcloud dataproc clusters delete "${CLUSTER}" --region "${REGION}" --quiet || true
gcloud compute instances delete "${KAFKA_VM}" --zone "${ZONE}" --quiet || true
bq rm -r -f -d "${PROJECT_ID}:${BQ_DATASET}" || true
gsutil -m rm -r "gs://${BUCKET}" || true

echo "Teardown completed"
