import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.telegram.org")
RUNNING_MODE = os.getenv("RUNNING_MODE", "polling")  # polling یا webhook
WEBHOOK_URL = os.getenv("WEBHOOK_URL", None)

DB_CONFIG = {
    "db_user": "postgres",
    "db_password": "1234",
    "db_host": "localhost",
    "db_port": "5432",
    "db_database": "social_chat_bot",
}