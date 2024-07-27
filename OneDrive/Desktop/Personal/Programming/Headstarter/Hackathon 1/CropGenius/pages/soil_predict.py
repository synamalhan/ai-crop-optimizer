import streamlit as st
import backend as bg

c1, c2, c3 = st.columns([1, 6, 1])
c1.page_link("pages/home.py", icon=":material/home:")
c3.page_link("pages/crop_predict.py", icon=":material/psychiatry:")
c1.subheader("")
c2.subheader("")
c1.image("assets/logo.png", width=100)
c2.markdown(
    "<h1 style='text-align: center;'>Ideal Soil Type Predictor</h1>",
    unsafe_allow_html=True,
)

df = bg.load_csv()
labels = bg.get_labels(df)

form = st.form("Soil Prediction")
c1, c2 = form.columns(2)
location = c1.text_input("Location:")
crop = c2.selectbox("Plant", labels)
if form.form_submit_button("Submit"):
    form.success("submitted")
    st.write("Location", location)
    st.write("Crop:", crop)

    temp_c, humid, rain = bg.get_current_weather(location)
    st.write("Temperature: ", temp_c, " Humidity: ", humid, " Rainfall: ", rain)
