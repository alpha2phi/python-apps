import io

import requests
import streamlit as st
from PIL import Image
from streamlit import uploaded_file_manager
from streamlit.cli import main

server_url=f"http://backend:8088/process"

st.title("GAN Model Serving Sample")
st.write(
    """Serving a GAN model using FastAPI and Streamlit."""
)  
uploaded_image = st.file_uploader("Upload Image")

if st.button("Process"):
    if uploaded_image is not None:
        # File details
        file_details = {"FileName": uploaded_image.name,"FileType": uploaded_image.type,"FileSize":uploaded_image.size}
        st.write(file_details)

        # File content
        files = {"file": uploaded_image.getvalue()}

        col1, col2 = st.beta_columns(2)

        # Show original image
        original_image = Image.open(uploaded_image)
        col1.header("Original Image")
        col1.image(original_image, use_column_width=True)

        # Post to server
        res = requests.post(server_url, files=files)
        processed_image = Image.open(io.BytesIO(res.content))
        col2.header("Processed Image")
        col2.image(processed_image, use_column_width=True)

    else:
        st.write("Upload image!")
