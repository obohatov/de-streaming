from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'shop_data',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8')),
    consumer_timeout_ms=10000
)

print("Listening for messages on topic 'shop_data'...")

for message in consumer:
    print(f"Received message: {message.value}")
