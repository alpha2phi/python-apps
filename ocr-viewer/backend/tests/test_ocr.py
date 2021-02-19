import unittest
from PIL import Image


class TestOCR(unittest.TestCase):
    """Test OCR."""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_model(self):
        # Images
        imgs = [
            "backend/test_images/bus.jpg",
            "backend/test_images/zidane.jpg",
            "backend/test_images/bear.jpg",
            "backend/test_images/dragon.jpg",
        ]
        img = Image.open(imgs[3])

