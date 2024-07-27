import streamlit as st

c1, c2, c3 = st.columns([1, 6, 1])

c1.image("assets/logo.png", width=100)
c2.markdown("<h1 style='text-align: center;'>CropGenius</h1>", unsafe_allow_html=True)


if st.button("Ideal Crop", use_container_width=True, type="primary"):
    st.switch_page("pages/crop_predict.py")

if st.button("Ideal Soil Type", use_container_width=True, type="primary"):
    st.switch_page("pages/soil_predict.py")
