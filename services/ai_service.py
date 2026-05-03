def calculate_business_health_score(summary):
    income = summary["total_income"]
    expenses = summary["total_expenses"]
    profit = summary["net_profit"]
    profit_margin = summary["profit_margin"]

    score = 50

    if profit > 0:
        score += 20
    else:
        score -= 25

    if profit_margin >= 30:
        score += 20
    elif profit_margin >= 15:
        score += 10
    elif profit_margin < 5:
        score -= 10

    if income > expenses:
        score += 10
    else:
        score -= 15

    score = max(0, min(100, score))

    return round(score, 2)


def determine_risk_level(score):
    if score >= 75:
        return "Low Risk"
    elif score >= 50:
        return "Medium Risk"
    return "High Risk"


def generate_recommendations(summary, category_data):
    recommendations = []

    income = summary["total_income"]
    expenses = summary["total_expenses"]
    profit = summary["net_profit"]
    profit_margin = summary["profit_margin"]

    if profit < 0:
        recommendations.append({
            "title": "Reduce Expenses Immediately",
            "message": "Your expenses are higher than your revenue. Review non-essential spending.",
            "priority": "High"
        })

    if profit_margin < 10:
        recommendations.append({
            "title": "Improve Profit Margin",
            "message": "Your profit margin is low. Consider increasing prices or reducing operating costs.",
            "priority": "High"
        })

    if expenses > income * 0.8:
        recommendations.append({
            "title": "Control Operating Costs",
            "message": "Expenses are consuming a large part of your revenue.",
            "priority": "Medium"
        })

    if not category_data.empty:
        top_category = category_data.iloc[0]["category"]
        recommendations.append({
            "title": f"Monitor {top_category} Spending",
            "message": f"{top_category} is your highest expense category. Track it closely.",
            "priority": "Medium"
        })

    if len(recommendations) == 0:
        recommendations.append({
            "title": "Business Looks Stable",
            "message": "Your business performance is healthy. Continue monitoring cash flow and expenses.",
            "priority": "Low"
        })

    return recommendations