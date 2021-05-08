import cv2
from ppgan.apps import Photo2CartoonPredictor
from PIL import Image


def photo_2_cartoon(input_image):
    p2c = Photo2CartoonPredictor()
    nd_arr = p2c.run(input_image)
    image = cv2.cvtColor(nd_arr, cv2.COLOR_RGB2BGR)
    return Image.fromarray(image)
