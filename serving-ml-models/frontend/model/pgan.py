import io

import requests
import streamlit as st
from PIL import Image

server_url=f"http://backend:8088/pgan"

def pgan():
    st.title("PGAN - Progressive Growing of GANS")
    st.write(
        """Serving PGAN model using FastAPI and Streamlit."""
    )  

    if st.button("Generate"):
        res = requests.get(server_url)
        pgan_image = Image.open(io.BytesIO(res.content))

        col1, col2 = st.beta_columns(2)
        col1.header("PGAN Image")
        col1.image(pgan_image, use_column_width=True)
