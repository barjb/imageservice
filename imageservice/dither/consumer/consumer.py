from kafka import KafkaConsumer
import json


class Consumer:
    def __init__(self, kafka_server) -> None:
        self.consumer = KafkaConsumer(bootstrap_servers=[kafka_server])
        self.callbacks = {}

    def subscribe(self, topic, callback):
        self.consumer.subscribe(topic)
        self.callbacks[topic] = callback

    def consume(self):
        print("consumer started listening")
        for message in self.consumer:
            print(message)
            topic = message.topic
            headers = message.headers
            value_bytes = message.value.decode("utf-8")
            data = json.loads(value_bytes)
            if topic in self.callbacks.keys():
                self.callbacks[topic](headers, data)
            else:
                print("No callbacks for: ", topic)
