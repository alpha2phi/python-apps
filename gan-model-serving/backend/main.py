import uvicorn
from fastapi import FastAPI, File
from starlette.responses import Response

app = FastAPI(
    title="GAN Model Serving Tutorial",
    description="""Serving a GAN model. Visit port 8501 for the Streamlit interface.""",
    version="0.0.1"
)

@app.get("/")
def home():
    return {"message": "A GAN Model Serving Tutorial"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8088, reload=True)
