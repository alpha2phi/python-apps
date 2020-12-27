import requests
import streamlit as st
from streamlit import uploaded_file_manager
from streamlit.cli import main

server_url=f"http://localhost:8088/{process}"

st.title("GAN Model Serving Sample")
st.write(
    """Serving a GAN model using FastAPI and Streamlit."""
)  
uploaded_image = st.file_uploader("Upload Image")

if st.button("Process"):
    # col1, col2 = st.beta_columns(2)
    if uploaded_image is not None:
        # File details
        file_details = {"FileName": uploaded_image.name,"FileType": uploaded_image.type,"FileSize":uploaded_image.size}
        st.write(file_details)

        # File content
        file_content = {"file": uploaded_image.getvalue()}
        # st.write(file_content)

        # res = requests.post(f"http://backend:8080/{style}", files=files)
        # img_path = res.json()
        # image = Image.open(img_path.get("name"))
        # st.image(image)
    else:
        st.write("Upload image!")
