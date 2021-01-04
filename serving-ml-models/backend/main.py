import io
import json
import uuid

import uvicorn
from PIL import Image
from starlette.responses import Response

from fastapi import FastAPI, File, UploadFile
from model.dcgan import dcgan
from model.pgan import pgan
from model.resnext import resnext

app = FastAPI(
    title="Serving Machine Learning Models",
    description="""Visit port 8501/docs for the Streamlit interface.""",
    version="0.0.1"
)

@app.get("/")
def home():
    return {"message": "Serving Machine Learning Models"}

@app.post("/resnext")
def process_resnext(file: UploadFile = File(...)):
    file_bytes = file.file.read()
    image = Image.open(io.BytesIO(file_bytes))
    name = f"/data/{str(uuid.uuid4())}.jpg"
    image.save(name)
    predictions = resnext(image)
    return predictions
    # return Response(content=json.dumps(predictions), media_type="application/json")
    # return Response(file_bytes, media_type="image/jpg")

@app.get("/pgan")
def generate_pgan():
    pgan_image = pgan()
    bytes_io = io.BytesIO()
    pgan_image.save(bytes_io, format="PNG")
    return Response(bytes_io.getvalue(), media_type="image/png")

@app.get("/dcgan")
def generate_dcgan():
    dcgan_image = dcgan()
    bytes_io = io.BytesIO()
    dcgan_image.save(bytes_io, format="PNG")
    return Response(bytes_io.getvalue(), media_type="image/png")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8088, reload=True)
