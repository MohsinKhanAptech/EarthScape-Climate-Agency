from flask import Blueprint, flash, render_template
from flask_mail import Message

from app import mail

notifications = Blueprint("notifications", __name__)


def send_alert(user_email, city, temperature):
    """
    Sends an automated alert if a predicted temperature exceeds a threshold.
    Called by the prediction engine or scheduled jobs.
    """
    threshold = 35.0  # Example: 35 degrees Celsius

    if temperature > threshold:
        try:
            msg = Message(
                subject=f"⚠️ CRITICAL ALERT: High Temperature in {city}",
                recipients=[user_email],
                body=f"Warning! The predictive model has detected an extreme temperature of {temperature}°C for {city}.\n\nPlease take necessary precautions.",
            )
            mail.send(msg)
            return True
        except Exception as e:
            print(f"Failed to send alert: {e}")
            return False
    return False


@notifications.route("/")
def alerts_log():
    """
    Simple view to show system alerts (Mockup for requirements).
    """
    # In a real app, you would fetch these from MongoDB
    fake_alerts = [
        {
            "date": "2025-01-10",
            "city": "Mumbai",
            "msg": "Heatwave warning: 42°C predicted",
        },
        {"date": "2025-02-15", "city": "London", "msg": "Storm surge risk detected"},
    ]
    return render_template("notifications.html", alerts=fake_alerts)
