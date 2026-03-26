#!/usr/bin/env bash
set -euo pipefail

KAFKA_VERSION="3.7.1"
SCALA_VERSION="2.13"

sudo apt-get update
sudo apt-get install -y openjdk-17-jre-headless curl

cd /opt
# Use archive mirror to avoid 404 when files are moved from primary downloads site.
sudo curl -fSL -o kafka.tgz "https://archive.apache.org/dist/kafka/${KAFKA_VERSION}/kafka_${SCALA_VERSION}-${KAFKA_VERSION}.tgz"
sudo tar -xzf kafka.tgz
sudo ln -sfn "/opt/kafka_${SCALA_VERSION}-${KAFKA_VERSION}" /opt/kafka

sudo useradd -m -s /bin/bash kafka || true
sudo chown -R kafka:kafka "/opt/kafka_${SCALA_VERSION}-${KAFKA_VERSION}"
sudo chown -h kafka:kafka /opt/kafka

echo "Kafka installed at /opt/kafka"
