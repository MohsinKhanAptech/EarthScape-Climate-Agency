import os

import matplotlib
import pandas as pd

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import seaborn as sns
from flask import Blueprint, current_app, flash, render_template, request, url_for
from flask_login import login_required

from app.models.ml_engine import get_all_cities, predict_temperature

views = Blueprint("views", __name__)


def generate_global_trend_plot():
    """
    Generates a static plot of Global Average Temperature by Year
    and saves it to the static folder for the Home Page.
    """
    try:
        # Define paths
        base_path = os.path.dirname(os.path.abspath(__file__))

        # --- FIXED PATH HERE ---
        # views.py is in 'app/', so we only go up ONE level ('..') to reach the project root
        data_path = os.path.join(
            base_path, "..", "data", "GlobalLandTemperaturesByMajorCity.csv"
        )

        static_img_path = os.path.join(base_path, "static", "images", "plots")

        # Ensure directory exists
        os.makedirs(static_img_path, exist_ok=True)
        target_file = os.path.join(static_img_path, "global_trend.png")

        # Optimization: Don't regenerate if it already exists
        if os.path.exists(target_file):
            return

        # Load Data
        df = pd.read_csv(data_path)
        df["dt"] = pd.to_datetime(df["dt"])
        df["Year"] = df["dt"].dt.year

        # Group by Year to get Global Average
        global_trends = df.groupby("Year")["AverageTemperature"].mean().reset_index()
        # Filter for cleaner graph (e.g., 1900 onwards)
        global_trends = global_trends[global_trends["Year"] >= 1900]

        # Plot
        plt.figure(figsize=(10, 5))
        sns.lineplot(
            data=global_trends,
            x="Year",
            y="AverageTemperature",
            color="#e74c3c",
            linewidth=2.5,
        )
        plt.title(
            "Global Average Temperature Rise (1900 - Present)",
            fontsize=14,
            fontweight="bold",
            color="#2c3e50",
        )
        plt.xlabel("Year")
        plt.ylabel("Avg Temp (°C)")
        plt.grid(True, linestyle="--", alpha=0.6)
        plt.tight_layout()

        # Save
        plt.savefig(target_file)
        plt.close()
        print("Generated Global Trend Plot.")

    except Exception as e:
        print(f"Error generating global plot: {e}")


@views.route("/")
def index():
    """
    Landing Page (Public).
    Now generates and displays the Global Trend Graph.
    """
    # Ensure the public graph exists
    generate_global_trend_plot()

    return render_template("index.html")


@views.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    prediction = None
    selected_city = None
    selected_date = None
    plot_url = None

    # SAFETY CHECK: If CSV is missing, get_all_cities might return empty
    cities = get_all_cities()
    if not cities:
        flash(
            "Warning: City data not found. Please check data/GlobalLandTemperaturesByMajorCity.csv",
            "warning",
        )

    if request.method == "POST":
        try:
            selected_city = request.form.get("city")
            date_picker = request.form.get("date_picker")  # "2025-06"

            if date_picker and selected_city:
                selected_date = date_picker
                # Split "2025-06" into Year=2025, Month=6
                year_str, month_str = date_picker.split("-")
                year = int(year_str)
                month = int(month_str)

                # 1. Run Prediction
                prediction = predict_temperature(selected_city, year, month)

                if prediction is None:
                    flash(
                        "Could not generate prediction. Check if model files are loaded.",
                        "danger",
                    )
                else:
                    # 2. Generate Visualization
                    plot_url = generate_trend_plot(selected_city, year)
            else:
                flash("Please select both a city and a date.", "warning")

        except Exception as e:
            flash(f"Error processing request: {e}", "danger")

    return render_template(
        "dashboard.html",
        cities=cities,
        prediction=prediction,
        selected_city=selected_city,
        selected_date=selected_date,
        plot_url=plot_url,
    )


def generate_trend_plot(city, year):
    """Helper for Dashboard (Specific City/Year)"""
    months = list(range(1, 13))
    temps = []

    for m in months:
        t = predict_temperature(city, year, m)
        temps.append(t if t is not None else 0)

    plt.figure(figsize=(10, 5))
    sns.lineplot(x=months, y=temps, marker="o", color="#27ae60", linewidth=2.5)
    plt.title(f"Temperature Trend for {city} in {year}", fontsize=14, fontweight="bold")
    plt.xlabel("Month")
    plt.ylabel("Temperature (°C)")
    plt.grid(True, linestyle="--", alpha=0.7)

    filename = f"trend_{city}_{year}.png"
    save_path = os.path.join(current_app.root_path, "static", "images", "plots")
    os.makedirs(save_path, exist_ok=True)

    full_path = os.path.join(save_path, filename)
    plt.savefig(full_path)
    plt.close()

    return url_for("static", filename=f"images/plots/{filename}")
