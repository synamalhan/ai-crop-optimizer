import joblib
import requests
import pandas as pd

api_key = "ba2998b9ecae4744a17195124242707"


def load_csv():
    # Load dataset from CSV file
    df = pd.read_csv("data/Crop_recommendation.csv")

    return df


def get_labels(df):
    unique_labels = df["label"].str.capitalize().unique().tolist()
    # Print the unique labels
    return unique_labels


def random_forest_classifier(N, P, K, temp, humid, rain, ph):
    rf_model = joblib.load("models/rf_model.pkl")
    label_encoder = joblib.load("models/label_encoder.pkl")

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
    xgb_regressor = joblib.load("models/xgb_regressor.pkl")
    label_encoder = joblib.load("models/label_encoder.pkl")
    scaler = joblib.load("models/scaler.pkl")

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


def soil_type_classifier():
    pass


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
