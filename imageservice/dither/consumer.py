from consumer.consumer import Consumer
import os
from dataclasses import dataclass
from typing import Protocol
from functools import partial
from service import startService
from enum import Enum


class IMessage(Protocol):
    def process():
        pass


@dataclass
class IUploadMessage:
    uuid: str
    filename: str
    url: str

    def process(self):
        startService(self.uuid, self.filename, self.url)


@dataclass
class IDeleteMessage:
    uuid: str

    def process(self):
        pass


objs = {"IMAGE_UPLOADED": IUploadMessage, "IMAGE_DELETED": IDeleteMessage}


def handler(headers, data: any):
    print("handler called:", data)

    message_type = None
    for header in headers:
        if header[0] == "message_type":
            message_type = header[1].decode("utf-8")
    print(message_type)
    message = objs[message_type]
    message_obj = message(**data)
    message_obj.process()


if __name__ == "__main__":
    consumer = Consumer(kafka_server=os.getenv("KAFKA_SERVER"))
    consumer.subscribe(os.getenv("KAFKA_IMAGE_TOPIC"), handler)
    consumer.consume()
    # startService(data["uuid"], data["filename"], data["url"])
