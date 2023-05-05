from consumer.consumer import Consumer
from dataclasses import dataclass
from typing import Protocol
from microservice import startService

from config import Config


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
    consumer = Consumer(kafka_server=Config.KAFKA_SERVER)
    consumer.subscribe(Config.KAFKA_IMAGE_TOPIC, handler)
    consumer.consume()
