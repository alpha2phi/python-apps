from starlette.responses import Response
from fastapi import FastAPI, File
import uvicorn

app = FastAPI(
    title="GAN Model Serving",
    description="""Serving a GAN model. Visit port 8501 for the Streamlit interface.""",
    version="0.0.1"
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080)
