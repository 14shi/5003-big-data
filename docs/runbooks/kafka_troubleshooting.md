# Kafka (Zookeeper mode) Troubleshooting

This project follows the original plan: single-node Kafka + ZooKeeper.

## Restart sequence on VM
```bash
pkill -f zookeeper || true
pkill -f kafka.Kafka || true
sleep 2

/opt/kafka/bin/zookeeper-server-start.sh -daemon /opt/kafka/config/zookeeper.properties
sleep 5
/opt/kafka/bin/kafka-server-start.sh -daemon /opt/kafka/config/server.properties
```

## Health checks
```bash
/opt/kafka/bin/zookeeper-shell.sh localhost:2181 ls /
/opt/kafka/bin/kafka-topics.sh --list --bootstrap-server localhost:9092
```

## Create topic
```bash
/opt/kafka/bin/kafka-topics.sh --create --if-not-exists --topic taxi_events --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
```

## Useful logs
```bash
tail -n 120 /tmp/zookeeper.log
tail -n 120 /tmp/kafka.log
```

If topic creation times out, check these first:
1. Java installed (`java -version`)
2. ZooKeeper started and reachable at `localhost:2181`
3. Kafka started without port conflict on `9092`
