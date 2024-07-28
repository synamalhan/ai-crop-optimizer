import streamlit as st
from PIL import Image
import requests
# from streamlit_gsheets import GSheetsConnection


# c1, c2, c3 = st.columns([1, 6, 1])

# c1.image(
#     "https://github.com/synamalhan/ai-crop-optimizer/blob/197954692f89d54c95c5a1ee8a6fcf88f98a8c92/assets/logo.png",
#     width=100,
# )
# c2.markdown("<h1 style='text-align: center;'>CropGenius</h1>", unsafe_allow_html=True)

# c1, c2, c3 = st.columns(3)

# main_menu = c2.container(border=True)
# if main_menu.button("Ideal Crop", use_container_width=True, type="primary"):
#     st.switch_page("pages/crop_predict.py")

# if main_menu.button("Ideal Soil Type", use_container_width=True, type="primary"):
#     st.switch_page("pages/soil_predict.py")

# Custom CSS for additional styling
st.markdown(
    """
    <style>
    .css-1aumxhk:hover {
        width: 220px;
    }
    /* Customize sidebar title */
    .css-12ttj6m {
        font-size: 24px;
        text-align: center;
        color: #4CAF50;
        margin-bottom: 20px;
    }
    /* Customize sidebar radio buttons */
    .css-1d391kg {
        font-size: 18px;
        margin: 10px 0;
        display: block;
        text-decoration: none;
        color: black;
        transition: color 0.3s, text-decoration 0.3s;
    }
    .css-1d391kg:hover {
        color: #4CAF50;
        text-decoration: underline;
    }
    .header {
        text-align: center;
        padding: 50px;
    }
    .subheader {
        text-align: center;
        font-size: 24px;
        color: #4CAF50;
    }
    .section-header {
        font-size: 28px;
        margin-top: 40px;
        color: #2E8B57;
        border-bottom: 2px solid #2E8B57;
        padding-bottom: 10px;
    }
    .steps {
        font-size: 18px;
        margin-top: 20px;
    }
    .cta {
        text-align: center;
        margin-top: 40px;
    }
    .footer {
        text-align: center;
        padding: 20px;
        position: relative;
        left: 0;
        bottom: 0;
        width: 100%;
    }
    .footer a {
    }
    .nav-item {
        display: inline;
        margin-right: 20px;
        font-size: 18px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# make a sidebar 
st.sidebar.title("Navigation")
page = st.sidebar.radio("", ["Home", "Crop Prediction", "Soil Prediction"], index=0)

if page == "Crop Prediction":
    st.switch_page("pages/crop_predict.py")
if page == "Soil Prediction":
    st.switch_page("pages/soil_predict.py")
elif page == "Home":
# Header
    st.markdown('<div class="header"><h1>CropGenius</h1></div>', unsafe_allow_html=True)
    st.markdown('<div class="subheader"><p>AI-powered crop optimizer software for farmers and gardeners!</p></div>', unsafe_allow_html=True)
    
    # Home Section
    st.markdown('<div class="section-header" id="home">Welcome to CropGenius!</div>', unsafe_allow_html=True)
    st.write("""
        CropGenius helps farmers and gardeners maximize their crop yield based on soil quality and weather conditions.
        Simply input your soil data and get the best crop recommendations instantly!
    """)
    
    # About Section
    st.markdown('<div class="section-header" id="about">About</div>', unsafe_allow_html=True)
    st.write("At CropGenius, we leverage advanced AI technology to empower farmers and gardeners by predicting the best crops for their specific locations. Our system analyzes a multitude of factors, including soil quality, weather conditions, and other environmental elements, to maximize yield and ensure optimal growth. Whether you're a farmer aiming to enhance your crop production or an individual looking to cultivate a thriving garden, our AI-driven recommendations provide you with the insights needed to make informed decisions. With CropGenius, achieving bountiful harvests and flourishing plants has never been easier.")


    st.markdown('<div class="section-header">How It Works</div>', unsafe_allow_html=True)
    st.write("""
        1. Input your soil data and weather conditions.
        2. Get personalized crop and soil recommendations.
        3. Optimize your yield and enjoy better harvests!
    """)
    # Placeholder for future screenshot/demo
    # image = Image.open('screenshot.png')  # Replace with your screenshot
    # st.image(image, caption="App Demo", use_column_width=True)

    # Features Section
    st.markdown('<div class="section-header" id="features">Features</div>', unsafe_allow_html=True)
    st.markdown('<div class="steps">1. Predict the Best Crop to Yield</div>', unsafe_allow_html=True)
    st.write("Based on soil quality (N, P, K, Ph), temperature, humidity, and rainfall, get the best crop recommendations.")
    st.markdown('<div class="steps">2. Predict Ideal Soil Type for Gardening</div>', unsafe_allow_html=True)
    st.write("Get recommendations on the ideal soil type for your gardening needs based on the plants you want to grow.")
    st.markdown('<div class="steps">3. Coming soon!</div>', unsafe_allow_html=True)
    st.write("Stay tuned for more exciting features that will be added soon!")

    # Feedback Section
    st.markdown('<div class="section-header" id="feedback">Feedback</div>', unsafe_allow_html=True)
    st.write("We would love to hear your thoughts, suggestions, concerns, or problems with anything so we can improve!")

    with st.form(key='feedback_form'):
        email = st.text_input("Email")
        feedback = st.text_area("Your Feedback")
        submit_button = st.form_submit_button(label='Submit')

        if submit_button:
            if email and feedback:
                # Placeholder URL for the API endpoint
                api_url = "https://example.com/api/feedback"
                
                # Data to be sent to the API
                feedback_data = {
                    "email": email,
                    "feedback": feedback
                }
                
                try:
                    response = requests.post(api_url, json=feedback_data)
                    if response.status_code == 200:
                        st.success("Thank you for your feedback!")
                    else:
                        st.error("There was an error submitting your feedback. Please try again later.")
                except Exception as e:
                    st.error(f"An error occurred: {e}")
            else:
                st.warning("Please fill in both fields.")

    # Footer
    st.markdown(
        """
        <div class="footer">
            <p>© 2024 CropGenius. All rights reserved.</p>
            <a href="#">Privacy Policy</a> | <a href="#">Terms of Service</a>
        </div>
        """,
        unsafe_allow_html=True
    )


    # # Create a connection object.
    # conn = st.connection("gsheets", type=GSheetsConnection)

    # df = conn.read()

    # # Print results.
    # for row in df.itertuples():
    #     st.write(f"{row.name} has a :{row.pet}:")
