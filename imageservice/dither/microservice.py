import io
import requests
from PIL import Image
import numpy as np
from cloudinary.uploader import upload
import cloudinary

from models.image import DitheredImage
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from config import Config

engine = create_engine(Config.POSTGRES_URL)

config = cloudinary.config(
    cloud_name=Config.CLOUDINARY_CLOUD_NAME,
    api_key=Config.CLOUDINARY_API_SECRET,
    api_secret=Config.CLOUDINARY_API_SECRET,
    secure=True,
)


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
    print("AFTER UPLOAD")
    with Session(engine) as session:
        try:
            ditheredimg = DitheredImage(
                uuid=uuid, channels=nc, url_dither=result["secure_url"]
            )
            session.add(ditheredimg)
            session.commit()
        except:
            return "SQL Error"
    print("AFTER SQL?")
    from producer import upload_prod, publish

    publish(
        producer=upload_prod,
        topic=Config.KAFKA_DITHER_TOPIC,
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
