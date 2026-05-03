import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = "change-this-secret-key-before-deployment"

    DATABASE_PATH = os.path.join(BASE_DIR, "database", "app.db")

    UPLOAD_FOLDER = os.path.join(BASE_DIR, "data", "uploads")
    REPORT_FOLDER = os.path.join(BASE_DIR, "reports", "generated")

    ALLOWED_EXTENSIONS = {"csv", "xlsx"}