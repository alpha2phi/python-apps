import sys
from pathlib import Path

file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

try:
    sys.path.remove(str(parent))
except ValueError:
    pass

import streamlit as st
import validators

from model.dcgan import dcgan
from model.pgan import pgan
from model.resnext import resnext
from model.photo_2_cartoon import photo_2_cartoon
from model.retinaface_anticov import retinaface_anticov

model_pages = {
    "DCGAN": dcgan,
    "PGAN": pgan,
    "RESNEXT": resnext,
    "Photo2Cartoon": photo_2_cartoon,
    "RetinaFaceAntiCov": retinaface_anticov,
}

intro = """
This app serves a number of machine learning models using FastAPI and Streamlit.
"""


def draw_main_page():
    st.write(f"""
    # Welcome to my machine learning playground! 👋
    """)
    st.text("")
    st.text("")

    st.write(intro)

    st.info("""
        :point_left: **To get started, choose a model on the left sidebar.**
    """)


# Draw sidebar
pages = list(model_pages.keys())
pages.insert(0, "Home")

st.sidebar.title(f"Machine Learning Models")
selected_demo = st.sidebar.radio("", pages)

# Draw main page
if selected_demo in model_pages:
    model_pages[selected_demo]()
else:
    draw_main_page()
