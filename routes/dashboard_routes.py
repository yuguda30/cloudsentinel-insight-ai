from flask import Blueprint, render_template, redirect, url_for, session
from services.data_service import load_user_dataset, calculate_summary, monthly_trend, category_summary
from services.ai_service import calculate_business_health_score, determine_risk_level, generate_recommendations

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    user_id = session["user_id"]
    df = load_user_dataset(user_id)
    has_data = not df.empty

    summary = calculate_summary(df)
    trend_df = monthly_trend(df)
    category_df = category_summary(df)

    trend = trend_df.to_dict(orient="records") if has_data else []
    category_data = category_df.to_dict(orient="records") if has_data else []

    health_score = calculate_business_health_score(summary) if has_data else 0
    risk_level = determine_risk_level(health_score) if has_data else "No Data"
    recommendations = generate_recommendations(summary, category_df) if has_data else []

    return render_template(
        "dashboard.html",
        has_data=has_data,
        summary=summary,
        trend=trend,
        category_data=category_data,
        health_score=health_score,
        risk_level=risk_level,
        recommendations=recommendations
    )