#!/usr/bin/env bash
set -euo pipefail

KAFKA_HOME="/opt/kafka"

nohup ${KAFKA_HOME}/bin/zookeeper-server-start.sh ${KAFKA_HOME}/config/zookeeper.properties > /tmp/zookeeper.log 2>&1 &
sleep 5
nohup ${KAFKA_HOME}/bin/kafka-server-start.sh ${KAFKA_HOME}/config/server.properties > /tmp/kafka.log 2>&1 &
sleep 8

${KAFKA_HOME}/bin/kafka-topics.sh --create --if-not-exists --topic taxi_events --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1

echo "Kafka and Zookeeper started; topic taxi_events ready."
