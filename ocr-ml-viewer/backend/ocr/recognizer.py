import numpy as np
from paddleocr import PaddleOCR, draw_ocr
from PIL import Image

ocr = PaddleOCR(use_angle_cls=True, lang="en", use_gpu=False)


def recognize(img):
    """Process a PIL image."""
    img_arr = np.array(img)
    result = ocr.ocr(img_arr, cls=True)

    if result is not None and len(result) > 0:
        boxes = [line[0] for line in result]
        txts = [line[1][0] for line in result]
        scores = [line[1][1] for line in result]
        processed_img = draw_ocr(
            img, boxes, txts, scores, font_path="./fonts/simfang.ttf"
        )
        return result, processed_img

    return result, ""
