import io
import uuid

import uvicorn
from fastapi import FastAPI, File, UploadFile
from PIL import Image
from starlette.responses import Response

from model.pgan import pgan

app = FastAPI(
    title="GAN Model Serving Tutorial",
    description="""Serving a GAN model. Visit port 8501 for the Streamlit interface.""",
    version="0.0.1"
)

@app.get("/")
def home():
    return {"message": "A GAN Model Serving Tutorial"}

@app.post("/resnext")
def process_resnext(file: UploadFile = File(...)):
    file_bytes = file.file.read()
    image = Image.open(io.BytesIO(file_bytes))
    name = f"/data/{str(uuid.uuid4())}.jpg"
    image.save(name) 
    return Response(file_bytes, media_type="image/jpg")

@app.get("/pgan")
def generate_pgan():
    pgan_image = pgan()
    bytes_io = io.BytesIO()
    pgan_image.save(bytes_io, format="PNG")
    return Response(bytes_io.getvalue(), media_type="image/png")

@app.get("/dcgan")
def generate_dcgan():
    pgan_image = pgan()
    bytes_io = io.BytesIO()
    pgan_image.save(bytes_io, format="PNG")
    return Response(bytes_io.getvalue(), media_type="image/png")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8088, reload=True)
