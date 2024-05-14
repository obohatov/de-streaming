from kafka import KafkaProducer
import json

class KafkaProducerManager:
    def __init__(self, bootstrap_servers: str):
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

    def send(self, topic: str, value: dict):
        self.producer.send(topic, value)
        self.producer.flush()
