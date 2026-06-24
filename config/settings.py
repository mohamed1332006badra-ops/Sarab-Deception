import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    PORT = int(os.getenv('PORT', 5000))
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_NAME = os.getenv('DB_NAME', 'sarab_db')
    DB_USER = os.getenv('DB_USER', 'sarab_admin')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
    REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
    REDIS_DB = int(os.getenv('REDIS_DB', 0))
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
    TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '')
    SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
    SMTP_EMAIL = os.getenv('SMTP_EMAIL', '')
    SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', '')
    MAX_FAILED_ATTEMPTS = int(os.getenv('MAX_FAILED_ATTEMPTS', 5))
    ALERT_THRESHOLD = int(os.getenv('ALERT_THRESHOLD', 3))
    ALLOWED_IPS = ['127.0.0.1', '::1']
    HONEYPOT_TYPES = ['ssh', 'web', 'database', 'ftp', 'rdp']
