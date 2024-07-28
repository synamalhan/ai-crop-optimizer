import streamlit as st
import backend as bk
import plotly.figure_factory as ff
import plotly.figure_factory as ff
import plotly.express as px
import numpy as np
from sklearn.metrics import (
    confusion_matrix,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
)
import joblib
import seaborn as sns
import matplotlib.pyplot as plt


df = bk.load_csv()
model = joblib.load("models/rf_model.pkl")
label_encoder = joblib.load("models/label_encoder.pkl")

X = df[["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]]

# Sample data for demonstration (Replace this with actual y_true and y_pred)
y_true = df["label"].values
y_true_encoded = label_encoder.transform(y_true)

# Predict y_pred based on the model
y_pred = model.predict(X)


# Function to calculate metrics
def calculate_metrics(y_true, y_pred):
    acc = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred, average="macro")
    recall = recall_score(y_true, y_pred, average="macro")
    f1 = f1_score(y_true, y_pred, average="macro")
    return acc, precision, recall, f1


# Calculate metrics
accuracy, precision, recall, f1 = calculate_metrics(y_true_encoded, y_pred)

# Confusion Matrix
conf_matrix = confusion_matrix(y_true_encoded, y_pred)

# Feature Importance
feature_importance = model.feature_importances_
features = ["N", "P", "K", "temperature", "humidity", "rainfall", "ph"]

c1, c2, c3 = st.columns([1, 6, 1])
c1.page_link("pages/home.py", icon=":material/home:")
c3.page_link("pages/soil_predict.py", icon=":material/potted_plant:")
c2.write("")
c2.write("")
c1.image("assets/logo.png", width=100)
c2.markdown(
    "<h1 style='text-align: center;'>Ideal Crop Predictor</h1>", unsafe_allow_html=True
)
c3.write("")
if c3.button(" ℹ️ info"):
    sidebar = st.sidebar
    sidebar.title(":green[About the Model]")
    sidebar.subheader("Why We Chose Random Forest Classifier:", divider="green")
    sidebar.markdown(
        "We selected the :green[Random Forest Classifier] for our crop prediction model due to its accuracy, robustness, and ability to handle large datasets. This method reduces overfitting by constructing multiple decision trees and averaging their results, leading to more reliable predictions."
    )
    sidebar.subheader("What is Random Forest Classifier:", divider="green")
    sidebar.markdown(
        "The :green[Random Forest Classifier] builds numerous decision trees using random subsets of the data and features, then outputs the most common class among the trees. This ensemble approach enhances predictive performance by combining the strengths of individual trees and mitigating their weaknesses."
    )
    sidebar.subheader("Weather API:", divider="green")
    sidebar.markdown(
        "To enhance user experience, we have integrated a weather API that retrieves real-time weather data for the location you enter. This feature ensures that our crop predictions are based on the most accurate and up-to-date climatic conditions, providing you with reliable and precise recommendations.\nWe are also using the weather API to forecast the future weather and issue any sort alerts or warning that may cause damage to Crop growth."
    )

    sidebar.subheader("Model Performance", divider="green")

    # Display metrics
    c1, c2, c3, c4 = sidebar.columns(4)
    c1.metric("Accuracy", f"{accuracy:.2f}")
    c2.metric("Precision", f"{precision:.2f}")
    c3.metric("Recall", f"{recall:.2f}")
    c4.metric("F1 Score", f"{f1:.2f}")

    with sidebar.popover(
        "Random Forest Classifier: Confusion Matrix", use_container_width=True
    ):
        # Display confusion matrix
        fig_conf_matrix = px.imshow(
            conf_matrix,
            text_auto=True,
            color_continuous_scale="Inferno",
            title="Confusion Matrix",
        )
        st.plotly_chart(fig_conf_matrix, use_container_width=True)

        st.caption(
            "This confusion matrix illustrates the performance of our crop prediction model. Each cell represents the count of predictions. The diagonal line indicates that the model's predictions align perfectly with the true labels, showing that all crops were correctly classified without any misclassifications."
        )

    with sidebar.popover(
        "Random Forest Classifier: Feature Importance", use_container_width=True
    ):
        # Display feature importance
        fig_feature_importance = px.pie(
            values=feature_importance, names=features, title="Feature Importance"
        )
        st.plotly_chart(fig_feature_importance, use_container_width=True)


container = st.container(border=True)

form = st.form("Crop Prediction")
form.subheader("Climate Details")
location = form.text_input("Location:")
form.subheader("Soil Analysis")
c1, c2, c3, c4 = form.columns(4)
N = c1.number_input("N ppm:", min_value=0)
P = c2.number_input("P ppm:", min_value=0)
K = c3.number_input("K ppm:", min_value=0)
pH = c4.number_input("pH:", min_value=0, max_value=14)
if form.form_submit_button("Submit"):
    temp_c, humid, rain = bk.get_current_weather(location)
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

    crop = bk.random_forest_classifier(N, P, K, temp_c, humid, rain, pH)

    container.subheader("Best Crop to Grow: ", divider="grey")
    container.subheader(f":green[{crop.capitalize()}]")
    with container.popover("Future Forecast", use_container_width=True):
        forecast_data = bk.get_weather_forecasting(location)
        col1, col2, col3 = st.columns(3)

        col1.markdown(
            f"<p style='text-align: center;'><strong>Date:</strong> {forecast_data[0]['date']}</p>"
            f"<p style='text-align: center;'><strong>Avg Temperature:</strong> {forecast_data[0]['avg_temp_c']}°C</p>"
            f"<p style='text-align: center;'><strong>Humidity:</strong> {forecast_data[0]['avg_humidity']}%</p>"
            f"<p style='text-align: center;'><strong>Rainfall:</strong> {forecast_data[0]['total_precip_mm']} mm</p>",
            unsafe_allow_html=True,
        )

        col2.markdown(
            f"<p style='text-align: center;'><strong>Date:</strong> {forecast_data[1]['date']}</p>"
            f"<p style='text-align: center;'><strong>Avg Temperature:</strong> {forecast_data[1]['avg_temp_c']}°C</p>"
            f"<p style='text-align: center;'><strong>Humidity:</strong> {forecast_data[1]['avg_humidity']}%</p>"
            f"<p style='text-align: center;'><strong>Rainfall:</strong> {forecast_data[1]['total_precip_mm']} mm</p>",
            unsafe_allow_html=True,
        )

        col3.markdown(
            f"<p style='text-align: center;'><strong>Date:</strong> {forecast_data[2]['date']}</p>"
            f"<p style='text-align: center;'><strong>Avg Temperature:</strong> {forecast_data[2]['avg_temp_c']}°C</p>"
            f"<p style='text-align: center;'><strong>Humidity:</strong> {forecast_data[2]['avg_humidity']}%</p>"
            f"<p style='text-align: center;'><strong>Rainfall:</strong> {forecast_data[2]['total_precip_mm']} mm</p>",
            unsafe_allow_html=True,
        )

        # Identify drastic changes and display a warning
        for i in range(1, len(forecast_data)):
            temp_change = abs(
                forecast_data[i]["avg_temp_c"] - forecast_data[i - 1]["avg_temp_c"]
            )
            humidity_change = abs(
                forecast_data[i]["avg_humidity"] - forecast_data[i - 1]["avg_humidity"]
            )
            rainfall_change = abs(
                forecast_data[i]["total_precip_mm"]
                - forecast_data[i - 1]["total_precip_mm"]
            )

            if temp_change > 5 or humidity_change > 20 or rainfall_change > 5:
                st.warning(
                    f"Drastic weather change detected between {forecast_data[i-1]['date']} and {forecast_data[i]['date']}. Make sure to adjust crop care accordingly"
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
