import joblib
import requests
import pandas as pd
from scipy.spatial import distance
import numpy as np
import streamlit as st
import os
import pickle
from xgboost import XGBRegressor



@st.cache_resource
def load_model_with_pickle(file_path):
    try:
        with open(file_path, "rb") as f:
            model = pickle.load(f)
        return model
    except Exception as e:
        print(f"Error loading model with pickle: {e}")
        return None


api_key = st.secrets["api-key"]


@st.cache_data
def load_csv():
    current_dir = os.path.dirname(__file__)
    csv_path = os.path.join(current_dir, "data", "Crop_recommendation.csv")

    # Load dataset from CSV file
    df = pd.read_csv(csv_path)

    return df


def get_labels(df):
    unique_labels = df["label"].str.capitalize().unique().tolist()
    # Print the unique labels
    return unique_labels


def random_forest_classifier(N, P, K, temp, humid, rain, ph):
    current_dir = os.path.dirname(__file__)

    rf_model = load_model_with_pickle(
        (os.path.join(current_dir, "models", "rf_model.pkl"))
    )
    label_encoder = load_model_with_pickle(
        (os.path.join(current_dir, "models", "label_encoder.pkl"))
    )

    new_data = {
        "N": [N],  # Example N value
        "P": [P],  # Example P value
        "K": [K],  # Example K value
        "temperature": [temp],
        "humidity": [humid],
        "ph": [ph],  # Example pH value
        "rainfall": [rain],
    }
    new_df = pd.DataFrame(new_data)

    # Predict the crop using the random forest model
    predicted_label = rf_model.predict(new_df)
    predicted_crop = label_encoder.inverse_transform(predicted_label)
    return predicted_crop[0]


def xgb_regressor(temp, humid, rain, crop):
    current_dir = os.path.dirname(__file__)

    xgb_regressor = load_model_with_pickle(
        (os.path.join(current_dir, "models", "xgb_regressor.pkl"))
    )
    label_encoder = load_model_with_pickle(
        (os.path.join(current_dir, "models", "label_encoder.pkl"))
    )
    scaler = load_model_with_pickle((os.path.join(current_dir, "models", "scaler.pkl")))

    new_soil_data = {
        "temperature": [temp],
        "humidity": [humid],
        "rainfall": [rain],
        "label": [label_encoder.transform([crop])[0]],
    }

    new_soil_df = pd.DataFrame(new_soil_data)

    # Scale the input data
    new_soil_df_scaled = scaler.transform(new_soil_df)

    # Predict soil conditions using the XGBRegressor model
    predicted_conditions = xgb_regressor.predict(new_soil_df_scaled)
    N = predicted_conditions[0][0]
    P = predicted_conditions[0][1]
    K = predicted_conditions[0][2]
    pH = predicted_conditions[0][3]
    return N, P, K, pH


def soil_type_classifier(N, K, P, pH):
    current_dir = os.path.dirname(__file__)
    csv_path = os.path.join(current_dir, "data", "soil_data.csv")
    new_dataset = pd.read_csv(csv_path)

    predicted_npkph = [N, P, K, pH]

    def find_closest_match(predicted_npkph, dataset):
        dataset_npkph = dataset[["N_NO3 ppm", "P ppm", "K ppm ", "pH"]]
        distances = distance.cdist([predicted_npkph], dataset_npkph, "euclidean")
        closest_index = np.argmin(distances)
        return dataset.iloc[closest_index]

    # Remove any rows with NaNs in the relevant columns
    new_dataset_clean = new_dataset.dropna(
        subset=["N_NO3 ppm", "P ppm", "K ppm ", "pH"]
    )

    closest_match = find_closest_match(predicted_npkph, new_dataset_clean)

    # Convert the closest match to a dictionary
    closest_match_dict = closest_match.to_dict()

    # Determine the predominant percentage and check for loamy soil
    sand_pct = closest_match_dict.get("Sand %")
    clay_pct = closest_match_dict.get("Clay %")
    silt_pct = closest_match_dict.get("Silt %")

    if sand_pct is not None and clay_pct is not None and silt_pct is not None:

        # Check for loamy soil
        if 30 <= sand_pct <= 50 and 10 <= clay_pct <= 30 and 30 <= silt_pct <= 50:
            predominant_component = "Loamy Soil"
        else:
            max_pct = max(sand_pct, clay_pct, silt_pct)
            predominant_component = (
                "Sandy Soil"
                if sand_pct == max_pct
                else "Clay Soil" if clay_pct == max_pct else "Silt Soil"
            )

    else:
        print("Unable to determine soil composition due to missing data.")
    return predominant_component, closest_match_dict


def get_current_weather(location):
    # Define the API endpoint
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={location}"

    # Make the API request
    response = requests.get(url)

    # Check the status code and response
    if response.status_code == 200:
        data = response.json()
        current_weather = data["current"]

        temp_c = current_weather["temp_c"]
        humidity = current_weather["humidity"]
        rainfall = current_weather["precip_mm"]  # Rainfall in millimeters

        return temp_c, humidity, rainfall
    else:
        return f"Failed to retrieve data: {response.status_code}"


def get_weather_forecasting(location):
    url = (
        f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={location}&days=3"
    )
    response = requests.get(url)

    forecast_data = []

    if response.status_code == 200:
        data = response.json()
        forecast_days = data["forecast"]["forecastday"]

        for day in forecast_days:
            date = day["date"]
            day_weather = day["day"]
            avg_temp_c = day_weather["avgtemp_c"]
            avg_humidity = day_weather["avghumidity"]
            total_precip_mm = day_weather["totalprecip_mm"]

            forecast_data.append(
                {
                    "date": date,
                    "avg_temp_c": avg_temp_c,
                    "avg_humidity": avg_humidity,
                    "total_precip_mm": total_precip_mm,
                }
            )

    else:
        print(f"Failed to retrieve data: {response.status_code}")
    return forecast_data
