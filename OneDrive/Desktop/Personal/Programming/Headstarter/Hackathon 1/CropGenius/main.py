import streamlit as st

pg = st.navigation(
    pages=[
        st.Page("pages/home.py"),
        st.Page("pages/crop_predict.py"),
        st.Page("pages/soil_predict.py"),
    ],
    position="hidden",
)
pg.run()
