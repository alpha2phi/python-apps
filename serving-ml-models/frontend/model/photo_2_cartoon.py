import io

import requests
import streamlit as st
from PIL import Image

server_url = f"http://backend:8088/photo2cartoon"


def photo_2_cartoon():
    st.title("Photo2Cartoon - Convert Photo to Cartoon")
    st.text("")
    st.text("")
    st.write("""Serving Photo2Cartoon model using FastAPI and Streamlit.""")
    uploaded_image = st.file_uploader("Upload Image")

    if st.button("Convert"):
        if uploaded_image is not None:
            # File details
            file_details = {
                "FileName": uploaded_image.name,
                "FileType": uploaded_image.type,
                "FileSize": uploaded_image.size
            }
            st.write(file_details)

            # File content
            files = {"file": uploaded_image.getvalue()}

            col1, col2 = st.beta_columns(2)

            # Show original image
            original_image = Image.open(uploaded_image)
            col1.header("Image")
            col1.image(original_image, use_column_width=True)

            # Post to server
            res = requests.post(server_url, files=files)
            col2.header("Cartoon")
            processed_image = Image.open(io.BytesIO(res.content))
            col2.image(processed_image, use_column_width=True)
        else:
            st.write("Upload image!")
