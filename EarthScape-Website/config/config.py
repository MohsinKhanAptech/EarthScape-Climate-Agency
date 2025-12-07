import os

from dotenv import load_dotenv

# Load variables from the .env file in the root directory
load_dotenv()


class Config:
    """
    Central Configuration Class.
    Reads sensitive data from environment variables to keep code secure.
    """

    # Security
    SECRET_KEY = os.getenv("SECRET_KEY", "default-fallback-key")

    # Database (MongoDB)
    MONGO_URI = os.getenv("MONGO_URI")

    # Email Settings (Flask-Mail)
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS") == "True"
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")

    # Uploads (Optional, if you add image upload features later)
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload size
