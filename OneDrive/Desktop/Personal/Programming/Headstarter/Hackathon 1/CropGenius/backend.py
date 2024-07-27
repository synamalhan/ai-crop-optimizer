import requests
import pandas as pd
from sklearn.calibration import LabelEncoder

api_key = "ba2998b9ecae4744a17195124242707"


def load_csv():
    # Load dataset from CSV file
    df = pd.read_csv("Crop_recommendation.csv")

    return df


def get_labels(df):
    unique_labels = df["label"].str.capitalize().unique().tolist()
    # Print the unique labels
    return unique_labels


def train_model(df):
    # Encode the labels
    label_encoder = LabelEncoder()
    df["label"] = label_encoder.fit_transform(df["label"])


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
