
import io

import requests
import streamlit as st
from PIL import Image

server_url=f"http://backend:8088/dcgan"

def dcgan():
    st.title("DCGAN on FashionGen")
    st.write(
        """Serving DCGAN model using FastAPI and Streamlit."""
    )  

    if st.button("Generate"):
        res = requests.get(server_url)
        dcgan_image = Image.open(io.BytesIO(res.content))
        col1, col2 = st.beta_columns(2)
        col1.header("DCGAN Image")
        col1.image(dcgan_image, use_column_width=True)
