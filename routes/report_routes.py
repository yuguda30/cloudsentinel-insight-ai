import os
from flask import Blueprint, render_template, redirect, url_for, session, send_file, flash

from services.data_service import load_user_dataset, calculate_summary, monthly_trend, category_summary
from services.ai_service import calculate_business_health_score, determine_risk_level, generate_recommendations
from services.report_service import generate_business_report, get_user_reports
from services.db_service import get_db


report_bp = Blueprint("reports", __name__)


@report_bp.route("/reports")
def reports():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    user_id = session["user_id"]

    df = load_user_dataset(user_id)
    has_data = not df.empty

    summary = calculate_summary(df)
    trend = monthly_trend(df)
    category_data = category_summary(df)

    health_score = calculate_business_health_score(summary) if has_data else 0
    risk_level = determine_risk_level(health_score) if has_data else "No Data"
    recommendations = generate_recommendations(summary, category_data) if has_data else []

    report_history = get_user_reports(user_id)

    return render_template(
        "reports.html",
        has_data=has_data,
        summary=summary,
        trend=trend.to_dict(orient="records"),
        category_data=category_data.to_dict(orient="records"),
        health_score=health_score,
        risk_level=risk_level,
        recommendations=recommendations,
        report_history=report_history
    )


@report_bp.route("/reports/generate")
def generate_report():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    user_id = session["user_id"]
    df = load_user_dataset(user_id)

    if df.empty:
        flash("Upload business data before generating a report.")
        return redirect(url_for("reports.reports"))

    summary = calculate_summary(df)
    category_data = category_summary(df)

    health_score = calculate_business_health_score(summary)
    risk_level = determine_risk_level(health_score)
    recommendations = generate_recommendations(summary, category_data)

    generate_business_report(
        user_id=user_id,
        summary=summary,
        health_score=health_score,
        risk_level=risk_level,
        recommendations=recommendations
    )

    flash("Report generated successfully.")
    return redirect(url_for("reports.reports"))


@report_bp.route("/reports/download/<int:report_id>")
def download_report(report_id):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    db = get_db()

    report = db.execute(
        """
        SELECT * FROM reports
        WHERE id = ? AND user_id = ?
        """,
        (report_id, session["user_id"])
    ).fetchone()

    if not report:
        flash("Report not found.")
        return redirect(url_for("reports.reports"))

    file_path = report["file_path"]

    if not os.path.exists(file_path):
        flash("Report file is missing.")
        return redirect(url_for("reports.reports"))

    return send_file(file_path, as_attachment=True)