#!/usr/bin/env bash
set -euo pipefail

KAFKA_HOME="/opt/kafka"

# Ensure stale processes do not block port binding.
pkill -f zookeeper || true
pkill -f kafka.Kafka || true
sleep 2

nohup ${KAFKA_HOME}/bin/zookeeper-server-start.sh ${KAFKA_HOME}/config/zookeeper.properties >/tmp/zookeeper.log 2>&1 &

# Wait for ZooKeeper to accept connections.
for i in {1..30}; do
  if ${KAFKA_HOME}/bin/zookeeper-shell.sh localhost:2181 ls / >/tmp/zk_ready.log 2>&1; then
    break
  fi
  sleep 2
done

nohup ${KAFKA_HOME}/bin/kafka-server-start.sh ${KAFKA_HOME}/config/server.properties >/tmp/kafka.log 2>&1 &

# Wait for Kafka broker readiness before topic creation.
for i in {1..30}; do
  if ${KAFKA_HOME}/bin/kafka-topics.sh --list --bootstrap-server localhost:9092 >/tmp/kafka_ready.log 2>&1; then
    break
  fi
  sleep 2
done

${KAFKA_HOME}/bin/kafka-topics.sh --create --if-not-exists --topic taxi_events --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1

echo "Kafka and ZooKeeper started; topic taxi_events ready."
