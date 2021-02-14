import unittest

import torch
import torchvision
from PIL import Image

print(torch.__version__)

model = torch.hub.load("ultralytics/yolov5", "yolov5s", pretrained=True)


class TestYoloModel(unittest.TestCase):
    """Test YOLO model."""

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

        # Inference
        results = model(img)
        self.assertIsNotNone(results)

        # Results
        results.print()
        results.save()
        # results.show()
        print(results.xyxy[0])  # print img1 predictions (pixels)
