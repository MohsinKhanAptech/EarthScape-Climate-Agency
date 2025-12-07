from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_pymongo import PyMongo

from config.config import Config

# --- Initialize Extensions (Global Scope) ---
mongo = PyMongo()
mail = Mail()
login_manager = LoginManager()


def create_app():
    """
    Construct the core application.
    """
    app = Flask(__name__)

    # Load configuration from config/config.py
    app.config.from_object(Config)

    # --- Connect Extensions to the App ---
    mongo.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)

    # Configure Login Manager
    login_manager.login_view = "auth.signin"
    login_manager.login_message_category = "info"

    # --- Register Blueprints ---
    from .auth import auth
    from .data_ingestion import ingestion  # <--- IMPORT THIS
    from .feedback import feedback
    from .notifications import notifications
    from .views import views

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    app.register_blueprint(feedback, url_prefix="/support")
    app.register_blueprint(notifications, url_prefix="/alerts")
    app.register_blueprint(ingestion, url_prefix="/ingestion")  # <--- REGISTER THIS

    return app
