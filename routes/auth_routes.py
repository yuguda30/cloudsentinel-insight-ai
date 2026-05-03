from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from sqlite3 import IntegrityError

from services.auth_service import create_user, verify_user

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        full_name = request.form.get("full_name", "").strip()
        business_name = request.form.get("business_name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "").strip()

        if not full_name or not business_name or not email or not password:
            flash("Please fill all fields.")
            return redirect(url_for("auth.register"))

        try:
            create_user(full_name, business_name, email, password)
            flash("Account created successfully. Please login.")
            return redirect(url_for("auth.login"))

        except IntegrityError:
            flash("Email already exists. Please login instead.")
            return redirect(url_for("auth.register"))

    return render_template("auth/register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "").strip()

        user = verify_user(email, password)

        if user:
            session["user_id"] = user["id"]
            session["full_name"] = user["full_name"]
            session["business_name"] = user["business_name"]
            return redirect(url_for("dashboard.dashboard"))

        flash("Invalid email or password.")
        return redirect(url_for("auth.login"))

    return render_template("auth/login.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))