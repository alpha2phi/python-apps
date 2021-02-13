import unittest

import torch
import torchvision

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
        imgs = ["backend/test_images/bus.jpg"]  # batched list of images

        # Inference
        results = model(imgs)

        # Results
        results.print()
        results.save()  # or .show()

        # Data
        print(results.xyxy[0])  # print img1 predictions (pixels)
