from flask import Blueprint, render_template, redirect, url_for, session

from services.data_service import load_user_dataset, calculate_summary, monthly_trend, category_summary
from services.ai_service import calculate_business_health_score, determine_risk_level, generate_recommendations

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    df = load_user_dataset(session["user_id"])

    has_data = not df.empty

    summary = calculate_summary(df)
    trend = monthly_trend(df)
    category_data = category_summary(df)

    health_score = calculate_business_health_score(summary) if has_data else 0
    risk_level = determine_risk_level(health_score) if has_data else "No Data"
    recommendations = generate_recommendations(summary, category_data) if has_data else []

    return render_template(
        "dashboard.html",
        has_data=has_data,
        summary=summary,
        trend=trend.to_dict(orient="records"),
        category_data=category_data.to_dict(orient="records"),
        health_score=health_score,
        risk_level=risk_level,
        recommendations=recommendations
    )