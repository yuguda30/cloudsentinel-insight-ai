import os
import time
from flask import Blueprint, render_template, request, redirect, url_for, current_app, flash, session
from werkzeug.utils import secure_filename

from services.data_service import save_upload_record

upload_bp = Blueprint("upload", __name__)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in current_app.config["ALLOWED_EXTENSIONS"]


@upload_bp.route("/upload", methods=["GET", "POST"])
def upload_data():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        file = request.files.get("file")

        if not file or file.filename == "":
            flash("No file selected.")
            return redirect(url_for("upload.upload_data"))

        if not allowed_file(file.filename):
            flash("Only CSV and Excel files are allowed.")
            return redirect(url_for("upload.upload_data"))

        user_id = session["user_id"]
        original_filename = secure_filename(file.filename)

        timestamp = int(time.time())
        stored_filename = f"user_{user_id}_{timestamp}_{original_filename}"

        os.makedirs(current_app.config["UPLOAD_FOLDER"], exist_ok=True)

        file_path = os.path.join(current_app.config["UPLOAD_FOLDER"], stored_filename)
        file.save(file_path)

        save_upload_record(
            user_id=user_id,
            filename=original_filename,
            stored_filename=stored_filename,
            file_path=file_path
        )

        flash("Dataset uploaded successfully. Your dashboard has been updated.")
        return redirect(url_for("dashboard.dashboard"))

    return render_template("upload.html")