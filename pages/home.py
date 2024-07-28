import streamlit as st
import os

# from streamlit_gsheets import GSheetsConnection


c1, c2, c3 = st.columns([1, 6, 1])

c1.image(os.path.join(os.path.dirname(__file__), "../assets/logo.png"), width=100)
c2.markdown("<h1 style='text-align: center;'>CropGenius</h1>", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)

main_menu = c2.container(border=True)
if main_menu.button("Ideal Crop", use_container_width=True, type="primary"):
    st.switch_page("pages/crop_predict.py")

if main_menu.button("Ideal Soil Type", use_container_width=True, type="primary"):
    st.switch_page("pages/soil_predict.py")


# # Create a connection object.
# conn = st.connection("gsheets", type=GSheetsConnection)

# df = conn.read()

# # Print results.
# for row in df.itertuples():
#     st.write(f"{row.name} has a :{row.pet}:")
