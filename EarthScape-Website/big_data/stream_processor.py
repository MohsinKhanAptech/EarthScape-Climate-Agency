import datetime
import random
import time

# Requirement: "Integrate real-time data streaming capabilities"
# Requirement: "Include algorithms for anomaly detection"

CITIES = ["New York", "London", "Mumbai", "Tokyo", "Sydney", "Paris"]


def generate_sensor_data():
    """Simulates reading from a weather sensor."""
    city = random.choice(CITIES)
    # Generate a temperature (mostly normal, occasionally extreme)
    if random.random() < 0.05:  # 5% chance of anomaly
        temp = random.uniform(40.0, 50.0)  # Extreme heat
    else:
        temp = random.uniform(10.0, 35.0)  # Normal range

    return {
        "timestamp": datetime.datetime.now().isoformat(),
        "city": city,
        "temperature": round(temp, 2),
        "sensor_id": f"SENS-{random.randint(1000, 9999)}",
    }


def process_stream():
    print("--- Starting Real-Time Weather Stream Processing ---")
    print("Listening for sensor data...")

    try:
        while True:
            data = generate_sensor_data()

            # Anomaly Detection Logic
            status = "NORMAL"
            if data["temperature"] > 38.0:
                status = "🔴 CRITICAL ANOMALY"
            elif data["temperature"] > 30.0:
                status = "🟡 HIGH"
            else:
                status = "🟢 NORMAL"

            print(
                f"[{data['timestamp']}] {data['city']}: {data['temperature']}°C | {status}"
            )

            # Simulate network latency
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nStream stopped by user.")


if __name__ == "__main__":
    process_stream()
