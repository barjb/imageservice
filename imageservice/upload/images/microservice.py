from models.image import Image
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
import os

from config import Config

# POSTGRES_URL = f"postgresql://{os.environ.get('POSTGRES_USER')}:{os.environ.get('POSTGRES_PASSWORD')}@{os.environ.get('POSTGRES_HOST')}:{os.environ.get('POSTGRES_PORT')}/{os.environ.get('POSTGRES_DB')}"
engine = create_engine(Config.POSTGRES_URL)


def upadateDitherUploaded(uuid, url_dither):
    print("received")
    print(uuid, url_dither)
    with Session(engine) as session:
        stmt = select(Image).where(Image.uuid == uuid)
        try:
            img = session.scalar(stmt)
            img.url_dither = url_dither
            img.status = "FINISHED"
            print(f"new url_dither {img.url_dither}, status {img.status}")
            session.add(img)
            session.commit()
        except:
            print("Error while updating sql row")


def updateDitherDeleted(uuid):
    print("received")
    print(uuid)
    with Session(engine) as session:
        stmt = select(Image).where(Image.uuid == uuid)
        try:
            img = session.scalar(stmt)
            img.url_dither = ""
            img.status = "FINISHED/URL_DELETED"
            session.add(img)
            session.commit()
        except:
            print("Error while updating sql row")
