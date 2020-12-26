from starlette.responses import Response

from fastapi import FastAPI, File

app = FastAPI(
    title="GAN Model Serving",
    description="""Serving a GAN model. Go to port 8501 for the streamlit interface.""",
    version="0.0.1"
)
