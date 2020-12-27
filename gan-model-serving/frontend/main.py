import streamlit as st

st.title("GAN Model Serving Sample")

st.write(
    """Serving a GAN model using FastAPI and Streamlit."""
)  

input_image = st.file_uploader("Upload Image")

if st.button("Process"):
    col1, col2 = st.beta_columns(2)
    if input_image:
        pass
    else:
        st.write("Upload image!")

if __name__ == "__main__":
    st.run()
