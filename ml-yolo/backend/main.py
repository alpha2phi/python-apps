import io
import json
import uuid

import uvicorn
from PIL import Image
from starlette.responses import Response

from fastapi import FastAPI, File, UploadFile

app = FastAPI(
    title="Serving YOLO",
    description="""Visit port 8088/docs for the FastAPI documentation.""",
    version="0.0.1",
)


@app.get("/")
def home():
    return {"message": "YOLO - You Only Look Once"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8088, reload=True)
