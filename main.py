import streamlit as st

st.set_page_config(
    page_title="CropGenie", page_icon="assets/favicon.png", layout="wide"
)

pg = st.navigation(
    pages=[
        st.Page("pages/home.py"),
        st.Page("pages/crop_predict.py"),
        st.Page("pages/soil_predict.py"),
    ],
    position="hidden",
)
pg.run()
