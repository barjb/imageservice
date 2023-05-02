import io
import os
import requests
from PIL import Image
import numpy as np
from cloudinary.uploader import upload
# from cloudinary.utils import cloudinary_url
import cloudinary
config = cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)


def health():
    return "health_dither_ok"


def startService(uuid, filename, url):
    data = requests.get(url).content
    img = Image.open(io.BytesIO(data))
    nc = 2
    print('nc =', nc)
    dim = dither(img, nc)
    output = io.BytesIO()
    dim.save(output, 'PNG')
    result = upload(output.getvalue(),
                    public_id=filename)

    from producer import upload_prod, publish
    TOPIC_NAME = os.getenv('KAFKA_DITHER_TOPIC')
    publish(upload_prod, TOPIC_NAME, {
            'url_dither': result['secure_url'], 'uuid': uuid})

    pass


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
                arr[i, j+1] += err * 7/16
            if i < height - 1:
                if j > 0:
                    arr[i+1, j-1] += err * 3/16
                arr[i+1, j] += err * 5/16
                if j < width - 1:
                    arr[i+1, j+1] += err / 16

    carr = np.array(arr/np.max(arr, axis=(0, 1)) * 255, dtype=np.uint8)
    return Image.fromarray(carr)
