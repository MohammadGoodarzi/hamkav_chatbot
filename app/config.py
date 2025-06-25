import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.telegram.org")
RUNNING_MODE = os.getenv("RUNNING_MODE", "polling")  # polling یا webhook
WEBHOOK_URL = os.getenv("WEBHOOK_URL", None)

DB_CONFIG = {
    "user": "your_db_user",
    "password": "your_db_password",
    "host": "localhost",
    "port": "5432",
    "database": "your_db_name",
}