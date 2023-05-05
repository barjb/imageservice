import io
import os
import requests
from PIL import Image
import numpy as np
from cloudinary.uploader import upload
import cloudinary
from models.image import DitheredImage
from extensions import db

config = cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True,
)


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


def startService(uuid, filename, url):
    data = requests.get(url).content
    img = Image.open(io.BytesIO(data))
    nc = 2
    print("nc =", nc)
    dim = dither(img, nc)
    output = io.BytesIO()
    dim.save(output, "PNG")
    try:
        result = upload(output.getvalue(), public_id=filename)
    except:
        return "ERROR WHILE UPLOADING TO CLOUDINARY"
    try:
        ditheredimg = DitheredImage(
            uuid=uuid, channels=nc, url_dither=result["secure_url"]
        )
        db.session.add(ditheredimg)
        db.session.commit()
    except:
        return "SQL Error"

    from producer import upload_prod, publish

    TOPIC_NAME = os.getenv("KAFKA_DITHER_TOPIC")
    publish(
        producer=upload_prod,
        topic=TOPIC_NAME,
        message={"url_dither": result["secure_url"], "uuid": uuid},
        headers=[
            ("message_type", b"DITHER_UPLOADED"),
            ("version", b"1.0.0"),
        ],
    )
    return


def get_new_val(old_val, channel_colors):
    return np.round(old_val * (channel_colors - 1)) / (channel_colors - 1)


def dither(img, nc):
    arr = np.array(img, dtype=float) / 255
    width, height = img.size
    for i in range(height):
        for j in range(width):
            old_val = arr[i, j].copy()
            new_val = get_new_val(old_val, nc)
            arr[i, j] = new_val
            err = old_val - new_val
            if j < width - 1:
                arr[i, j + 1] += err * 7 / 16
            if i < height - 1:
                if j > 0:
                    arr[i + 1, j - 1] += err * 3 / 16
                arr[i + 1, j] += err * 5 / 16
                if j < width - 1:
                    arr[i + 1, j + 1] += err / 16

    carr = np.array(arr / np.max(arr, axis=(0, 1)) * 255, dtype=np.uint8)
    return Image.fromarray(carr)


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
