def generate_business_insight_text(summary, health_score, risk_level):
    income = summary["total_income"]
    expenses = summary["total_expenses"]
    profit = summary["net_profit"]
    margin = summary["profit_margin"]

    if risk_level == "High Risk":
        return (
            "The business is currently exposed to high financial risk. "
            "Expenses are significantly affecting profitability, and urgent cost control is recommended."
        )

    if risk_level == "Medium Risk":
        return (
            "The business is performing moderately, but there are signs that expenses and profit margin "
            "should be monitored closely."
        )

    return (
        "The business appears financially healthy. Revenue performance is stronger than expenses, "
        "and the business has a good foundation for growth."
    )


def generate_risk_alerts(summary):
    alerts = []

    income = summary["total_income"]
    expenses = summary["total_expenses"]
    profit = summary["net_profit"]
    margin = summary["profit_margin"]

    if expenses > income:
        alerts.append("Expenses are higher than revenue.")

    if profit < 0:
        alerts.append("The business is operating at a loss.")

    if margin < 10:
        alerts.append("Profit margin is below a healthy level.")

    if not alerts:
        alerts.append("No major financial risk detected.")

    return alerts