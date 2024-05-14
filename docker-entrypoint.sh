#!/bin/sh

# Ожидание Kafka
KAFKA_HOST="kafka"
KAFKA_PORT="9092"

echo "Waiting for Kafka to be ready..."
while ! nc -z $KAFKA_HOST $KAFKA_PORT; do
  sleep 0.1
done
echo "Kafka is up and running"

# Запуск Uvicorn
exec "$@"
