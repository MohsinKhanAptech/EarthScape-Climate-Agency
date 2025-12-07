import os
import warnings

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest, RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Suppress warnings for cleaner output
warnings.filterwarnings("ignore")

# ==========================================
# 0. CONFIGURATION & PATHS
# ==========================================
# Get the directory where this script lives (EarthScape-Website/training/)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Path to Data: Go up one level (..), then into 'data'
DATA_PATH = os.path.join(
    BASE_DIR, "..", "data", "GlobalLandTemperaturesByMajorCity.csv"
)

# Path to Save Models: Go up one level (..), then into 'app/models'
MODEL_DIR = os.path.join(BASE_DIR, "..", "app", "models")

# Ensure model directory exists
os.makedirs(MODEL_DIR, exist_ok=True)


def train():
    # ==========================================
    # 1. DATA INGESTION & CLEANING
    # ==========================================
    print(f"--- Starting Model Training ---")
    print(f"Reading data from: {DATA_PATH}")

    if not os.path.exists(DATA_PATH):
        print("❌ Error: Dataset not found. Please check the path.")
        return

    df = pd.read_csv(DATA_PATH)

    # Convert Date to datetime object
    df["dt"] = pd.to_datetime(df["dt"])

    # Handle missing values
    df = df.dropna(subset=["AverageTemperature"])

    # Convert Latitude/Longitude to numeric
    def clean_coords(coord):
        if isinstance(coord, str):
            if "S" in coord or "W" in coord:
                return -float(coord[:-1])
            return float(coord[:-1])
        return coord

    df["Latitude"] = df["Latitude"].apply(clean_coords)
    df["Longitude"] = df["Longitude"].apply(clean_coords)

    # ==========================================
    # 2. FEATURE ENGINEERING
    # ==========================================
    print("Feature Engineering...")
    df["Year"] = df["dt"].dt.year
    df["Month"] = df["dt"].dt.month

    # Encode Categorical Variables
    le_city = LabelEncoder()
    le_country = LabelEncoder()

    # We use fit_transform to learn the mapping and convert the data
    df["City_Code"] = le_city.fit_transform(df["City"])
    df["Country_Code"] = le_country.fit_transform(df["Country"])

    # Select Features for Training
    features = ["Year", "Month", "Latitude", "Longitude", "City_Code", "Country_Code"]
    target = "AverageTemperature"

    X = df[features]
    y = df[target]

    # Split Data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # ==========================================
    # 3. MODEL 1: TREND PREDICTION (Regression)
    # ==========================================
    print("Training Random Forest Regressor (this may take a minute)...")
    rf_model = RandomForestRegressor(n_estimators=50, random_state=42, n_jobs=-1)
    rf_model.fit(X_train, y_train)

    # Evaluation
    y_pred = rf_model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f"\n--- Model Performance ---")
    print(f"Mean Squared Error: {mse:.4f}")
    print(f"R2 Score: {r2:.4f}")

    # ==========================================
    # 4. OPTIONAL: ANOMALY DETECTION CHECK
    # ==========================================
    # We won't save this model, but we run it to ensure the logic holds up
    print("\nRunning quick Anomaly Detection check on New York...")
    city_data = df[df["City"] == "New York"].copy()
    if not city_data.empty:
        iso_forest = IsolationForest(contamination=0.01, random_state=42)
        city_data["anomaly"] = iso_forest.fit_predict(city_data[["AverageTemperature"]])
        num_anomalies = len(city_data[city_data["anomaly"] == -1])
        print(f"Found {num_anomalies} historical anomalies in New York data.")

    # ==========================================
    # 5. SAVE MODELS
    # ==========================================
    print(f"\nSaving models to {MODEL_DIR}...")

    # Save the main model
    joblib.dump(rf_model, os.path.join(MODEL_DIR, "climate_model.pkl"))

    # Crucial: Save the encoders so the web app can understand "New York"
    joblib.dump(le_city, os.path.join(MODEL_DIR, "le_city.pkl"))
    joblib.dump(le_country, os.path.join(MODEL_DIR, "le_country.pkl"))

    print("✅ Success! Models and encoders are saved and ready for the website.")


if __name__ == "__main__":
    train()
