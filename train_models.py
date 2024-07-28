import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import mean_squared_error, r2_score
from xgboost import XGBRegressor
import pickle

# Load your CSV file into a pandas DataFrame
df = pd.read_csv("data/Crop_recommendation.csv")

# Encode the labels if they are not numeric
label_encoder = LabelEncoder()
df["label"] = label_encoder.fit_transform(df["label"])

# --------------------------- Random Forest Classifier -------------------------------------

# Split the data into features and labels
X = df.drop("label", axis=1)
y = df["label"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train the Random Forest Classifier
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# Save the trained model and the label encoder
with open("rf_model.pkl", "wb") as f:
    pickle.dump(rf_model, f)

with open("label_encoder.pkl", "wb") as f:
    pickle.dump(label_encoder, f)

# -------------------------- XGBRegressor -----------------------------------------------

# Define features and targets
X = df[["temperature", "humidity", "rainfall", "label"]]
y = df[["N", "P", "K", "ph"]]

# Normalize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)

# Train the XGBRegressor for soil conditions
xgb_regressor = XGBRegressor(
    learning_rate=0.1, max_depth=5, n_estimators=50, subsample=0.8, random_state=42
)
xgb_regressor.fit(X_train, y_train)

# Save the trained model and scaler
with open("xgb_regressor.pkl", "wb") as f:
    pickle.dump(xgb_regressor, f)

with open("scaler.pkl", "wb") as f:
    pickle.dump(scaler, f)
