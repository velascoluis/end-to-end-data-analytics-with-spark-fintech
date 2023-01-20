
kafka-topics.sh --zookeeper localhost:2181 --alter --topic transactions  --config retention.ms=1000 && sleep 5
kafka-topics.sh --zookeeper localhost:2181 --alter --topic transactions  --config retention.ms=604800000 



