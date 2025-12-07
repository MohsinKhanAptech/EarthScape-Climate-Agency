import os

import joblib
import numpy as np
import pandas as pd
from flask import current_app

# Global variables to cache the model and data
model = None
le_city = None
city_metadata = None


def load_resources():
    """
    Loads the ML model, encoders, and city metadata (Lat/Long) into memory.
    """
    global model, le_city, city_metadata

    if model is not None:
        return  # Already loaded

    base_path = os.path.dirname(os.path.abspath(__file__))

    # Paths to .pkl files
    model_path = os.path.join(base_path, "climate_model.pkl")
    le_city_path = os.path.join(base_path, "le_city.pkl")

    # Path to Dataset (to get Lat/Long for cities)
    # We go up two levels from 'app/models' to root, then into 'data'
    data_path = os.path.join(
        base_path, "..", "..", "data", "GlobalLandTemperaturesByMajorCity.csv"
    )

    try:
        print("Loading ML Resources...")
        model = joblib.load(model_path)
        le_city = joblib.load(le_city_path)

        # Load just enough data to get City -> Lat/Long mapping
        # We drop duplicates to make the lookup fast
        df = pd.read_csv(data_path)

        # Clean coordinates (reuse the logic from your training script)
        def clean_coords(coord):
            if isinstance(coord, str):
                if "S" in coord or "W" in coord:
                    return -float(coord[:-1])
                return float(coord[:-1])
            return coord

        df["Latitude"] = df["Latitude"].apply(clean_coords)
        df["Longitude"] = df["Longitude"].apply(clean_coords)

        # Create a lookup dictionary: {'CityName': {'lat': 12.3, 'long': 45.6}}
        city_metadata = (
            df.drop_duplicates(subset=["City"])
            .set_index("City")[["Latitude", "Longitude"]]
            .to_dict("index")
        )
        print("Resources loaded successfully.")

    except Exception as e:
        print(f"Error loading ML resources: {e}")
        # Initialize empty if files are missing so app doesn't crash immediately
        model = None
        city_metadata = {}


def get_all_cities():
    """Returns a sorted list of cities for the dropdown menu."""
    if city_metadata is None:
        load_resources()
    return sorted(city_metadata.keys())


def predict_temperature(city, year, month):
    """
    Predicts temperature for a given city and date.
    Returns: Float (temperature) or None if error.
    """
    if model is None:
        load_resources()

    try:
        # 1. Get Lat/Long for the city
        if city not in city_metadata:
            return None

        lat = city_metadata[city]["Latitude"]
        long = city_metadata[city]["Longitude"]

        # 2. Encode City
        # Handle cases where the city might not be in the label encoder perfectly
        try:
            city_code = le_city.transform([city])[0]
        except:
            city_code = 0  # Fallback

        # 3. Prepare Input (must match training features: Year, Month, Lat, Long, City_Code, Country_Code)
        # Note: We are passing 0 for Country_Code as a placeholder if you didn't save that encoder
        input_data = pd.DataFrame(
            [[year, month, lat, long, city_code, 0]],
            columns=[
                "Year",
                "Month",
                "Latitude",
                "Longitude",
                "City_Code",
                "Country_Code",
            ],
        )

        # 4. Predict
        prediction = model.predict(input_data)[0]
        return round(prediction, 2)

    except Exception as e:
        print(f"Prediction Error: {e}")
        return None
