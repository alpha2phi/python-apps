import torch
import os
import logging
from dotenv import load_dotenv, find_dotenv
from PIL import Image

load_dotenv(find_dotenv())
yolo_model = os.getenv("YOLO_MODEL", "yolov5s")

logging.info(f"YOLO model - {yolo_model}")

model = torch.hub.load("ultralytics/yolov5", yolo_model, pretrained=True)


def yolov5(img):
    """Process a PIL image."""

    # Inference
    results = model(img)

    detected_classes = []
    names = results.names
    if results.pred is not None:
        pred = results.pred[0]
        if pred is not None:
            for c in pred[:, -1].unique():
                n = (pred[:, -1] == c).sum()
                detected_classes.append(f"{n} {names[int(c)]}{'s' * (n > 1)}")

    logging.info(f"Detected classes: {detected_classes}")

    rendered_imgs = results.render()
    converted_img = Image.fromarray(rendered_imgs[0]).convert("RGB")

    return detected_classes, converted_img
