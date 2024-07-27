import streamlit as st
import backend as bk

c1, c2, c3 = st.columns([1, 6, 1])
c1.page_link("pages/home.py", icon=":material/home:")
c3.page_link("pages/soil_predict.py", icon=":material/potted_plant:")
c2.subheader("")
c1.image("assets/logo.png", width=100)
c2.markdown(
    "<h1 style='text-align: center;'>Ideal Crop Predictor</h1>", unsafe_allow_html=True
)

form = st.form("Crop Prediction")

location = form.text_input("Location:")
form.write("Soil Analysis")
c1, c2, c3, c4 = form.columns(4)
N = c1.text_input("Soil N%:")
P = c2.text_input("Soil P%:")
K = c3.text_input("Soil K%:")
pH = c4.text_input("Soil pH:")
if form.form_submit_button("Submit"):
    form.success("Submitted")
    st.write("Location: ", location)
    st.write("Soil N%: ", N)
    st.write("Soil P%: ", P)
    st.write("Soil K%: ", K)
    st.write("Soil pH: ", pH)

    temp_c, humid, rain = bk.get_current_weather(location)
    st.write("Temperature: ", temp_c, " Humidity: ", humid, " Rainfall: ", rain)
