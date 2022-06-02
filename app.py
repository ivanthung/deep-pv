import streamlit as st

refresh = st.button("Click to Refresh")

image = st.file_uploader("Upload Picture")

st.markdown("Your image:")

if image:
    st.image(image)
