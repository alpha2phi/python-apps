import unittest

from PIL import Image


class TestCartoon(unittest.TestCase):
    """Test OCR."""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_model(self):
        # Images
        imgs = [
            "backend/test_images/image_1.png",
        ]
        img = Image.open(imgs[0])

