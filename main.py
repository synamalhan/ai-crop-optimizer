import streamlit as st

st.set_page_config(
    page_title="CropGenie",
    page_icon="https://github.com/synamalhan/ai-crop-optimizer/blob/197954692f89d54c95c5a1ee8a6fcf88f98a8c92/assets/favicon.png",
    layout="wide",
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
