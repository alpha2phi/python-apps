from io import BytesIO
import base64
import cv2
from ppgan.apps import Photo2CartoonPredictor
from PIL import Image


def photo_2_cartoon(input_image):
    p2c = Photo2CartoonPredictor(output_path="/tmp/")
    nd_arr = p2c.run(input_image)
    image = cv2.cvtColor(nd_arr, cv2.COLOR_RGB2BGR)
    return Image.fromarray(image)


def base64_encode_img(img):
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    buffered.seek(0)
    img_byte = buffered.getvalue()
    encoded_img = "data:image/png;base64," + base64.b64encode(
        img_byte).decode()
    return encoded_img
