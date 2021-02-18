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
        # results.print()
        # results.save()
        # print(results.xyxy[0])  # print img1 predictions (pixels)
        # results.show()
        print(results.names)

        # https://github.com/ultralytics/yolov5/blob/master/models/common.py
        names = results.names
        detected = []
        if results.pred is not None:
            pred = results.pred[0]
            if pred is not None:
                for c in pred[:, -1].unique():
                    n = (pred[:, -1] == c).sum()
                    detected.append(f"{n} {names[int(c)]}{'s' * (n > 1)}")

        print(f"Detected: {detected}")

        processed_imgs = results.render()
        processed_img = Image.fromarray(processed_imgs[0]).convert("RGB")
        processed_img.save("test.jpg")
