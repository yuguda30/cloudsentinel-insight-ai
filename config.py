import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "cloudsentinel-secret-key")

    DATABASE_PATH = os.path.join(BASE_DIR, "database", "app.db")

    UPLOAD_FOLDER = os.path.join(BASE_DIR, "data", "uploads")
    REPORT_FOLDER = os.path.join(BASE_DIR, "reports", "generated")

    ALLOWED_EXTENSIONS = {"csv", "xlsx"}