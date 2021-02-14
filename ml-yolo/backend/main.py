import io
import json
import uuid
import logging
import sys
import uvicorn
from PIL import Image
from starlette.responses import Response
from fastapi import FastAPI, File, UploadFile

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

from model import yolov5


app = FastAPI(
    title="Serving YOLO",
    description="""Visit port 8088/docs for the FastAPI documentation.""",
    version="0.0.1",
)


@app.get("/")
def home():
    return {"message": "YOLO - You Only Look Once"}


@app.get("/yolov5")
def process_yolov5(file: UploadFile = File(...)):
    file_bytes = file.file.read()
    image = Image.open(io.BytesIO(file_bytes))
    name = f"/data/{str(uuid.uuid4())}.jpg"
    image.save(name)
    classes, converted_img = yolov5(image)
    return converted_img


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8088, reload=True)
