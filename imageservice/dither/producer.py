from kafka import KafkaProducer
import json
import os

KAFKA_SERVER = os.getenv("KAFKA_SERVER")

upload_prod = KafkaProducer(
    bootstrap_servers=KAFKA_SERVER,
    value_serializer=lambda m: json.dumps(m).encode("utf-8"),
)


def publish(producer: KafkaProducer, topic: str, message: any, headers: str):
    producer.send(topic=topic, value=message, headers=headers)
