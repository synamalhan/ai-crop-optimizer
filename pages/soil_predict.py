import streamlit as st
import backend as bg
import plotly.figure_factory as ff
import joblib
import plotly.express as px
from sklearn.metrics import r2_score
import os
import pickle
from xgboost import XGBRegressor


def load_model_with_pickle(file_path):
    try:
        with open(file_path, "rb") as f:
            model = pickle.load(f)
        return model
    except Exception as e:
        print(f"Error loading model with pickle: {e}")
        return None


current_dir = os.path.dirname(__file__)


# Load data and labels
df = bg.load_csv()
labels = bg.get_labels(df)

xgb_regressor = load_model_with_pickle(
    (os.path.join(current_dir, "..", "models", "xgb_regressor.pkl"))
)
label_encoder = load_model_with_pickle(
    (os.path.join(current_dir, "..", "models", "label_encoder.pkl"))
)
scaler = load_model_with_pickle(
    (os.path.join(current_dir, "..", "models", "scaler.pkl"))
)


# Layout for header and navigation
c1, c2, c3 = st.columns([1, 6, 1])
c1.page_link("pages/home.py", icon=":material/home:")
c3.page_link("pages/crop_predict.py", icon=":material/psychiatry:")
c1.image(
    (os.path.join(current_dir, "..", "assets", "logo.png")),
    width=100,
)
c2.write("")
c2.write("")
c3.write("")
c2.markdown(
    "<h1 style='text-align: center;'>Ideal Soil Type Predictor</h1>",
    unsafe_allow_html=True,
)

# Info button
info = c3.button(" ℹ️ info")


if info:
    sidebar = st.sidebar
    sidebar.title(":green[About the Model]")
    sidebar.subheader("Why We Chose XGBRegressor:", divider="green")
    sidebar.markdown(
        "We opted for the :green[XGBRegressor] for our soil prediction model because of its high accuracy, efficiency, and scalability. This method is particularly well-suited for handling large datasets and complex relationships, making it ideal for predicting soil conditions based on multiple input parameters."
    )
    sidebar.subheader("What is XGBRegressor:", divider="green")
    sidebar.markdown(
        ":green[XGBRegressor] is an implementation of gradient boosting that focuses on optimizing performance and speed. It builds an ensemble of decision trees in a sequential manner, where each tree corrects the errors of its predecessors. This iterative approach results in a robust and accurate predictive model."
    )
    sidebar.subheader("Weather API:", divider="green")
    sidebar.markdown(
        "To enhance user experience, we have integrated a weather API that retrieves real-time weather data for the location you enter. This feature ensures that our crop predictions are based on the most accurate and up-to-date climatic conditions, providing you with reliable and precise recommendations."
    )
    sidebar.subheader("Model Performance", divider="green")

    features = ["temperature", "humidity", "rainfall", "label"]
    target = ["N", "P", "K", "ph"]
    X = df[features]
    y = df[target]
    X["label"] = label_encoder.transform(X["label"])

    X_scaled = scaler.transform(X)
    y_pred = xgb_regressor.predict(X_scaled)

    r2 = r2_score(y, y_pred)
    sidebar.success(f"**R-squared (R²) Value**: {r2}")

    # Create performance and importance plots
    # Create performance and importance plots
    with sidebar.popover(
        "XGBRegressor: Actual vs Predicted Soil Conditions", use_container_width=True
    ):
        fig_performance = px.scatter(
            x=y.values.flatten(),
            y=y_pred.flatten(),
            labels={"x": "Actual", "y": "Predicted"},
            title="XGBRegressor: Actual vs Predicted Soil Conditions",
            color_discrete_sequence=["red"],
        )
        fig_performance.update_traces(marker=dict(opacity=0.5))
        fig_performance.add_shape(
            type="line",
            x0=min(y.values.flatten()),
            y0=min(y.values.flatten()),
            x1=max(y.values.flatten()),
            y1=max(y.values.flatten()),
            line=dict(dash="dash"),
        )
        st.plotly_chart(fig_performance, use_container_width=True)
        st.caption(
            "This graph depicts the relationship between the actual and predicted values generated by our XGBRegressor model. The straight diagonal line indicates that the predictions are closely aligned with the actual values, showcasing the model's accuracy and reliability in forecasting outcomes."
        )
    with sidebar.popover("XGBRegressor Feature Importance", use_container_width=True):
        importance = xgb_regressor.feature_importances_
        feature_names = [
            "temperature",
            "humidity",
            "rainfall",
            "crop",
        ]  # Rename 'label' to 'crop'
        vibrant_colors = px.colors.qualitative.Bold  # Vibrant color palette
        fig_importance = px.pie(
            values=importance,
            names=feature_names,
            title="XGBRegressor Feature Importance",
            color_discrete_sequence=vibrant_colors,
        )
        st.plotly_chart(fig_importance, use_container_width=True)

# Main container
container = st.container(border=True)

# Form for soil prediction
form = st.form("Soil Prediction")
c1, c2 = form.columns(2)
c1.subheader("Climate Conditions")
location = c1.text_input("Location:")
c2.subheader("Crop")
crop = c2.selectbox("Plant", labels)

if form.form_submit_button("Submit"):
    temp_c, humid, rain = bg.get_current_weather(location)
    container.subheader(f"Climate Conditions for {location}", divider="grey")
    cc1, cc2, cc3 = container.columns(3)

    cc1.markdown(
        "<p style='text-align: center;'><strong>Temperature: "
        + str(temp_c)
        + "</strong></p>",
        unsafe_allow_html=True,
    )
    cc2.markdown(
        "<p style='text-align: center;'><strong>Humidity: "
        + str(humid)
        + "</strong></p>",
        unsafe_allow_html=True,
    )
    cc3.markdown(
        "<p style='text-align: center;'><strong>Rainfall: "
        + str(rain)
        + "</strong></p>",
        unsafe_allow_html=True,
    )

    N, P, K, pH = bg.xgb_regressor(temp_c, humid, rain, crop.lower())

    predominant_comp, soil_comp = bg.soil_type_classifier(N, P, K, pH)
    container.subheader("Best Soil Type: ", divider="grey")
    container.subheader(f":green[{str(predominant_comp)}]")
    with container.popover("View Details", use_container_width=True):
        col1, col2, col3 = st.columns(3)
        col1.markdown(
            f"<p style='text-align: center;'><strong>Sand %</strong>: {soil_comp['Sand %']}</p>",
            unsafe_allow_html=True,
        )
        col2.markdown(
            f"<p style='text-align: center;'><strong>Clay %</strong>: {soil_comp['Clay %']}</p>",
            unsafe_allow_html=True,
        )
        col3.markdown(
            f"<p style='text-align: center;'><strong>Silt %</strong>: {soil_comp['Silt %']}</p>",
            unsafe_allow_html=True,
        )

        col1, col2, col3 = st.columns(3)
        col1.markdown(
            f"<p style='text-align: center;'><strong>N (NO3) ppm</strong>: {soil_comp['N_NO3 ppm']}</p>",
            unsafe_allow_html=True,
        )
        col2.markdown(
            f"<p style='text-align: center;'><strong>P ppm</strong>: {soil_comp['P ppm']}</p>",
            unsafe_allow_html=True,
        )
        col3.markdown(
            f"<p style='text-align: center;'><strong>K ppm</strong>: {soil_comp['K ppm ']}</p>",
            unsafe_allow_html=True,
        )

        col1, col2, col3 = st.columns(3)
        col1.markdown(
            f"<p style='text-align: center;'><strong>pH</strong>: {soil_comp['pH']}</p>",
            unsafe_allow_html=True,
        )
        col2.markdown(
            f"<p style='text-align: center;'><strong>EC mS/cm</strong>: {soil_comp['EC mS/cm']}</p>",
            unsafe_allow_html=True,
        )
        col3.markdown(
            f"<p style='text-align: center;'><strong>O.M. %</strong>: {soil_comp['O.M. %']}</p>",
            unsafe_allow_html=True,
        )

        col1, col2, col3 = st.columns(3)
        col1.markdown(
            f"<p style='text-align: center;'><strong>CACO3 %</strong>: {soil_comp['CACO3 %']}</p>",
            unsafe_allow_html=True,
        )
        col2.markdown(
            f"<p style='text-align: center;'><strong>Mg ppm</strong>: {soil_comp['Mg ppm']}</p>",
            unsafe_allow_html=True,
        )
        col3.markdown(
            f"<p style='text-align: center;'><strong>Fe ppm</strong>: {soil_comp['Fe ppm']}</p>",
            unsafe_allow_html=True,
        )

        col1, col2, col3 = st.columns(3)
        col1.markdown(
            f"<p style='text-align: center;'><strong>Zn ppm</strong>: {soil_comp['Zn ppm']}</p>",
            unsafe_allow_html=True,
        )
        col2.markdown(
            f"<p style='text-align: center;'><strong>Mn ppm</strong>: {soil_comp['Mn ppm']}</p>",
            unsafe_allow_html=True,
        )
        col3.markdown(
            f"<p style='text-align: center;'><strong>Cu ppm</strong>: {soil_comp['Cu ppm']}</p>",
            unsafe_allow_html=True,
        )

        col1, col2, col3 = st.columns(3)
        col1.markdown(
            f"<p style='text-align: center;'><strong>B ppm</strong>: {soil_comp['B ppm ']}</p>",
            unsafe_allow_html=True,
        )


chart = st.container(border=True)
if chart.checkbox("View DataBase"):
    with chart.expander("About the graph"):
        st.caption(
            "The histogram in our application represents the distribution of temperature data for various crops. Each bar in the histogram corresponds to the frequency of temperature values within specific ranges, allowing us to visualize how temperatures vary for each crop. This comparison highlights common temperature ranges and patterns, providing valuable insights into the environmental conditions suitable for different crops."
        )
    hist_data = []
    c1, c2 = chart.columns([6, 3])

    group_labels = c2.multiselect(
        "Select the crops", df["label"].unique(), df["label"].unique()
    )

    # Gather histogram data
    for label in group_labels:
        data_list = df[df["label"] == label]["temperature"].tolist()
        if data_list:
            hist_data.append(data_list)

    # Filter out empty labels corresponding to empty hist_data lists
    filtered_labels = [
        group_labels[i] for i in range(len(group_labels)) if hist_data[i]
    ]

    if filtered_labels:
        # Create distplot with custom bin_size
        fig = ff.create_distplot(
            hist_data, filtered_labels, bin_size=[0.1 for _ in filtered_labels]
        )

        # Plot!
        c1.plotly_chart(fig, use_container_width=True)
    else:
        c1.write("No data available for the selected crops.")
