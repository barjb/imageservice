from extensions import db
from models.image import Image
from flask import request
from werkzeug.utils import secure_filename
import os
import cloudinary
import cloudinary.uploader
from uuid import uuid4

config = cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True,
)
print(
    os.getenv("CLOUDINARY_CLOUD_NAME"),
    os.getenv("CLOUDINARY_API_KEY"),
    os.getenv("CLOUDINARY_API_SECRET"),
)
print(
    "****1. Set up and configure the SDK:****\nCredentials: ",
    config.cloud_name,
    config.api_key,
    "\n",
)


def health():
    return "health_upload_ok"


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def post_image():
    if request.method == "POST":
        for key in request.files.keys():
            file = request.files[key]
            print(file)
            print(file.filename)

            if file.filename == "":
                return "No selected files", 404
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filename_without_ext = filename.rsplit(".", 1)[0]
                image_bytes = file.read()
                try:
                    result = cloudinary.uploader.upload(
                        image_bytes, public_id=filename_without_ext
                    )
                except:
                    return "ERROR WHILE UPLOADING TO CLOUDINARY"
                try:
                    image = Image(
                        filename=filename,
                        uuid=uuid4(),
                        status="PENDING",
                        url=result["secure_url"],
                        url_dither="",
                    )
                    db.session.add(image)
                    db.session.commit()
                except:
                    return "Exception SQL"
                from images.producer import upload_prod, publish

                TOPIC_NAME = os.getenv("KAFKA_IMAGE_TOPIC")
                obj = {
                    "filename": filename,
                    "url": result["secure_url"],
                    "uuid": str(image.uuid),
                }
                publish(
                    upload_prod,
                    TOPIC_NAME,
                    obj,
                    headers=[
                        ("message_type", b"IMAGE_UPLOADED"),
                        ("version", b"1.0.0"),
                    ],
                )
                return f'Saved file {result["secure_url"]}\n\nsent: {obj}'
        return "No keys"


def get_image(uuid: str):
    try:
        img = db.session.execute(db.select(Image).where(Image.uuid == uuid)).scalar()
        obj = {
            "uuid": img.uuid,
            "filename": img.filename,
            "status": img.status,
            "url": img.url,
            "url_dither": img.url_dither,
        }
        return obj
    except:
        return "SQL exception"


def event():
    from images.producer import upload_prod, publish

    TOPIC_NAME = os.getenv("KAFKA_IMAGE_TOPIC")

    custom_message = {
        "uuid": "1234-1234-asdf-qwer",
        "filename": "temp_filename",
        "url": "temp_url",
    }
    headers = [
        ("message_type", b"IMAGE_UPLOADED"),
        ("version", b"1.0.0"),
    ]
    publish(upload_prod, TOPIC_NAME, custom_message, headers)
    return "ok"


def get_images():
    try:
        images = Image.query.all()
    except:
        return "SQL exception"
    return [image.as_dict() for image in images]


def delete_image(uuid: str):
    try:
        # TO DO SAGA
        # Status: SCHEDULED TO DELETION
        # PRODCUCER => DITHER_SERVICE
        # DITHER_SERVICE => UPLOAD_CONSUMER
        # UPLOAD_CONSUMER DELETES
        db.session.execute(db.delete(Image).where(Image.uuid == uuid))
        db.session.commit()
    except:
        return "SQL exception"
    from images.producer import upload_prod, publish

    TOPIC_NAME = os.getenv("KAFKA_IMAGE_TOPIC")
    obj = {
        "uuid": uuid,
    }
    publish(
        upload_prod,
        TOPIC_NAME,
        obj,
        headers=[
            ("message_type", b"IMAGE_DELETED"),
            ("version", b"1.0.0"),
        ],
    )
    return f"Image deleted uuid: {uuid}"


def fix():
    stmt = db.select(Image).where(Image.status == "PENDING")
    try:
        result = db.session.execute(stmt).scalar()
    except:
        return "SQL Eception"

    from images.producer import upload_prod, publish

    TOPIC_NAME = os.getenv("KAFKA_IMAGE_TOPIC")
    custom_message = {
        "uuid": str(result.uuid),
        "filename": result.filename,
        "url": result.url,
    }
    headers = [
        ("message_type", b"IMAGE_UPLOADED"),
        ("version", b"1.0.0"),
    ]
    publish(upload_prod, TOPIC_NAME, custom_message, headers)
    return str(result.uuid)
