#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   PROJECT_ID=your-project-id BILLING_ACCOUNT=XXXX ./scripts/gcp_setup.sh
# Optional env:
#   REGION=us-central1 ZONE=us-central1-a TEAM=team1

PROJECT_ID="${PROJECT_ID:?PROJECT_ID is required}"
REGION="${REGION:-us-central1}"
ZONE="${ZONE:-us-central1-a}"
TEAM="${TEAM:-team1}"
BUCKET="bd5003-${TEAM}-raw-${PROJECT_ID}"
BQ_DATASET="mobility_analytics"
CLUSTER="bd5003-spark-cluster"
KAFKA_VM="bd5003-kafka-vm"

echo "[1/7] Set gcloud project"
gcloud config set project "${PROJECT_ID}"

echo "[2/7] Enable required APIs"
gcloud services enable dataproc.googleapis.com compute.googleapis.com bigquery.googleapis.com storage.googleapis.com

echo "[3/7] Create storage bucket"
gsutil mb -l "${REGION}" "gs://${BUCKET}" || true

echo "[4/7] Create BigQuery dataset"
bq --location="${REGION}" mk -d --description "5003 mobility analytics" "${PROJECT_ID}:${BQ_DATASET}" || true

echo "[5/7] Create Dataproc cluster (small footprint)"
gcloud dataproc clusters create "${CLUSTER}" \
  --region "${REGION}" \
  --single-node \
  --master-machine-type e2-standard-2 \
  --image-version 2.2-debian12 \
  --optional-components JUPYTER

echo "[6/7] Create Kafka VM (demo)"
gcloud compute instances create "${KAFKA_VM}" \
  --zone "${ZONE}" \
  --machine-type e2-small \
  --image-family debian-12 \
  --image-project debian-cloud \
  --boot-disk-size 20GB

echo "[7/7] Print outputs"
echo "BUCKET=gs://${BUCKET}"
echo "BQ_DATASET=${PROJECT_ID}:${BQ_DATASET}"
echo "DATAPROC_CLUSTER=${CLUSTER}"
echo "KAFKA_VM=${KAFKA_VM}"
