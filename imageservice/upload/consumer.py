from models.image import Image
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from kafka import KafkaConsumer
import os
import json


TOPIC_NAME = os.getenv('KAFKA_DITHER_TOPIC')
KAFKA_SERVER = os.getenv('KAFKA_SERVER')

consumer = KafkaConsumer(TOPIC_NAME, bootstrap_servers=KAFKA_SERVER)

print('start listening')

POSTGRES_URL = f"postgresql://{os.environ.get('POSTGRES_USER')}:{os.environ.get('POSTGRES_PASSWORD')}@{os.environ.get('POSTGRES_HOST')}:{os.environ.get('POSTGRES_PORT')}/{os.environ.get('POSTGRES_DB')}"
engine = create_engine(POSTGRES_URL)


def testService(uuid, url_dither):
    print('received')
    print(uuid, url_dither)
    with Session(engine) as session:
        stmt = select(Image).where(Image.uuid == uuid)
        try:
            img = session.scalar(stmt)
            img.url_dither = url_dither
            img.status = 'FINISHED'
            print(f'new url_dither {img.url_dither}, status {img.status}')
            session.add(img)
            session.commit()
        except:
            print('Error while updating sql row')


for message in consumer:
    value_bytes = message.value.decode('utf-8')
    data = json.loads(value_bytes)
    print(f"Processing uuid: {data['uuid']} url_dither: {data['url_dither']}")
    testService(data['uuid'], data['url_dither'])
