from models.image import DitheredImage
from extensions import db
import os


def health():
    return "health_dither_ok"


def get_image(uuid: str):
    try:
        img = db.session.execute(
            db.select(DitheredImage).where(DitheredImage.uuid == uuid)
        ).scalar()
    except:
        return "SQL Error"
    return img.as_dict()


def get_images():
    try:
        images = DitheredImage.query.all()
    except:
        return "SQL Error"
    return [image.as_dict() for image in images]


def event():
    TOPIC_NAME = os.getenv("KAFKA_DITHER_TOPIC")
    from producer import upload_prod, publish

    publish(
        producer=upload_prod,
        topic=TOPIC_NAME,
        message={"uuid": "temp_uuid"},
        headers=[
            ("message_type", b"DITHER_DELETED"),
            ("version", b"1.0.0"),
        ],
    )
    # publish(
    #     producer=upload_prod,
    #     topic=TOPIC_NAME,
    #     message={"uuid": "temp_uuid", "url_dither": "temp_url"},
    #     headers=[
    #         ("message_type", b"DITHER_UPLOADED"),
    #         ("version", b"1.0.0"),
    #     ],
    # )

    return "event dither"


def delete_image(uuid: str):
    try:
        db.session.execute(db.delete(DitheredImage).where(DitheredImage.uuid == uuid))
    except:
        return "SQL Error"
    TOPIC_NAME = os.getenv("KAFKA_DITHER_TOPIC")
    from producer import upload_prod, publish

    publish(
        producer=upload_prod,
        topic=TOPIC_NAME,
        message={"uuid": uuid},
        headers=[
            ("message_type", b"DITHER_DELETED"),
            ("version", b"1.0.0"),
        ],
    )
    return f"uuid: {uuid} deleted"
