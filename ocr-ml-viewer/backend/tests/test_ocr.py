import unittest

from PIL import Image

import pytesseract


class TestOCR(unittest.TestCase):
    """Test OCR."""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_model(self):
        # Images
        imgs = [
            "backend/test_images/image_1.png",
            "backend/test_images/image_2.jpg",
            "backend/test_images/image_3.png",
            "backend/test_images/image_4.jpg",
            "backend/test_images/image_5.jpg",
        ]
        img = Image.open(imgs[2])

        # Simple image to string
        print(pytesseract.image_to_string(img))

        # List of available languages
        # print(pytesseract.get_languages(config=""))

        # Get verbose data including boxes, confidences, line and page numbers
        print(pytesseract.image_to_data(img))

        # Chinese Simplified
        print(
            pytesseract.image_to_string(
                "backend/test_images/image_5.jpg", lang="chi_sim"
            )
        )
