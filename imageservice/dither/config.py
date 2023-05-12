import os


class Config:
    KAFKA_SERVER = os.getenv("KAFKA_SERVER")
    KAFKA_DITHER_TOPIC = os.getenv("KAFKA_DITHER_TOPIC")
    KAFKA_IMAGE_TOPIC = os.getenv("KAFKA_IMAGE_TOPIC")
    POSTGRES_URL = "postgresql://kriskrawiec99:mCe7uBwErMd9@ep-orange-snow-930075.eu-central-1.aws.neon.tech/neondb?options=project%3Dep-orange-snow-930075"
    # POSTGRES_URL = f"postgresql://{os.environ.get('POSTGRES_USER')}:{os.environ.get('POSTGRES_PASSWORD')}@{os.environ.get('POSTGRES_HOST')}:{os.environ.get('POSTGRES_PORT')}/{os.environ.get('POSTGRES_DB')}"
    CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME")
    CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
    CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET")
