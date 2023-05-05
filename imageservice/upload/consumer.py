import os
from images.microservice import upadateDitherUploaded, updateDitherDeleted
from consumer.consumer import Consumer
from dataclasses import dataclass
from typing import Protocol
from enum import Enum
from config import Config


class IMessage(Protocol):
    def process():
        pass


@dataclass
class IDitherUploadedMessage:
    uuid: str
    url_dither: str

    def process(self):
        upadateDitherUploaded(self.uuid, self.url_dither)


@dataclass
class IDitherDeletedMessage:
    uuid: str

    def process(self):
        updateDitherDeleted(self.uuid)


objs = {
    "DITHER_DELETED": IDitherDeletedMessage,
    "DITHER_UPLOADED": IDitherUploadedMessage,
}


def handler(headers, data: any):
    print("handler called:", headers, data)

    message_type = None
    for header in headers:
        if header[0] == "message_type":
            message_type = header[1].decode("utf-8")
    print(message_type)
    message = objs[message_type]
    message_obj = message(**data)
    message_obj.process()


class MessageTypes(Enum):
    DITHER_IMAGE_UPLOADED = (IDitherUploadedMessage,)
    DITHER_IMAGE_DELETED = IDitherDeletedMessage


if __name__ == "__main__":
    consumer = Consumer(Config.KAFKA_SERVER)
    consumer.subscribe(Config.KAFKA_DITHER_TOPIC, handler)

    consumer.consume()
