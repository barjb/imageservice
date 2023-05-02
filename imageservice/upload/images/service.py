
from extensions import db
from models.image import Image
from flask import request
from werkzeug.utils import secure_filename
import os
import cloudinary
import cloudinary.uploader
from uuid import uuid4

config = cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)
print(os.getenv('CLOUDINARY_CLOUD_NAME'), os.getenv(
    "CLOUDINARY_API_KEY"), os.getenv("CLOUDINARY_API_SECRET"))
print("****1. Set up and configure the SDK:****\nCredentials: ",
      config.cloud_name, config.api_key, "\n")


def health():
    return "health_upload_ok"


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def upload_file():
    if request.method == 'POST':
        for key in request.files.keys():
            file = request.files[key]
            print(file)
            print(file.filename)

            if file.filename == '':
                return 'No selected files', 404
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filename_without_ext = filename.rsplit('.', 1)[0]
                image_bytes = file.read()
                try:
                    result = cloudinary.uploader.upload(
                        image_bytes, public_id=filename_without_ext)

                    image = Image(filename=filename, uuid=uuid4(), status='PENDING',
                                  url=result['secure_url'], url_dither="")
                    db.session.add(image)
                    db.session.commit()

                    from images.producer import upload_prod, publish
                    TOPIC_NAME = os.getenv('KAFKA_IMAGE_TOPIC')
                    obj = {
                        'filename': filename, 'url': result['secure_url'], 'uuid': str(image.uuid)}
                    publish(upload_prod, TOPIC_NAME, obj)

                    return f'Saved file {result["secure_url"]}\n\nsent: {obj}'
                except:
                    return 'Exception'
        return 'No keys'


def get_file(uuid: str):
    img = db.session.execute(
        db.select(Image).where(Image.uuid == uuid)).scalar()
    obj = {
        'uuid': img.uuid,
        'filename': img.filename,
        'status': img.status,
        'url': img.url,
        'url_dither': img.url_dither
    }
    return obj


def event():
    from images.producer import upload_prod, publish
    TOPIC_NAME = os.getenv('KAFKA_IMAGE_TOPIC')

    custom_message = {
        'filename': 'temp_filename', 'url': 'temp_url'}
    publish(upload_prod, TOPIC_NAME, custom_message)
    return 'ok'
