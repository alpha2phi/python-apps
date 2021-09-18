from paddleocr import PaddleOCR, draw_ocr

ocr = PaddleOCR(use_angle_cls=True, lang="en", use_gpu=False)


def recognize(img):
    """Process a PIL image."""
    result = ocr.ocr(img, cls=True)
    return result
