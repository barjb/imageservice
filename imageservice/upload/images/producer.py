from kafka import KafkaProducer
import json
import os

from config import Config

upload_prod = KafkaProducer(
    bootstrap_servers=Config.KAFKA_SERVER,
    value_serializer=lambda m: json.dumps(m).encode("utf-8"),
)


def publish(producer: KafkaProducer, topic: str, message: any, headers):
    producer.send(topic=topic, value=message, headers=headers)
