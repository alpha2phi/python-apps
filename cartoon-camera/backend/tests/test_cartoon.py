import unittest

from PIL import Image
from ..cartoon import cartoonify


class TestCartoon(unittest.TestCase):
    """Test cartoon."""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_model(self):
        imgs = [
            "backend/test_images/sky.jpg",
        ]
        img = Image.open(imgs[0])
        output_image = cartoonify(img)
        output_image.save("output.jpg")

