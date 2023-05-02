from service import startService
from kafka import KafkaConsumer
import os
import json

TOPIC_NAME = os.getenv('KAFKA_IMAGE_TOPIC')
KAFKA_SERVER = os.getenv('KAFKA_SERVER')

consumer = KafkaConsumer(TOPIC_NAME, bootstrap_servers=KAFKA_SERVER)

print('start listening')

for message in consumer:
    # print(message)
    value_bytes = message.value.decode('utf-8')
    data = json.loads(value_bytes)
    print(data)
    for key in data:
        print(key, data[key])
    # print(data['filename'])
    # print(data['url'])
    # print(data['url'])
    startService(data['uuid'], data['filename'], data['url'])
