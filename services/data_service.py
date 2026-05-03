import os
import pandas as pd
from services.db_service import get_db


EMPTY_COLUMNS = [
    "date",
    "description",
    "category",
    "type",
    "amount",
    "currency",
    "payment_method",
    "source"
]


def empty_dataset():
    return pd.DataFrame(columns=EMPTY_COLUMNS)


def get_latest_upload(user_id):
    db = get_db()

    return db.execute(
        """
        SELECT * FROM uploads
        WHERE user_id = ?
        ORDER BY uploaded_at DESC
        LIMIT 1
        """,
        (user_id,)
    ).fetchone()


def save_upload_record(user_id, filename, stored_filename, file_path):
    db = get_db()

    db.execute(
        """
        INSERT INTO uploads (user_id, filename, stored_filename, file_path)
        VALUES (?, ?, ?, ?)
        """,
        (user_id, filename, stored_filename, file_path)
    )

    db.commit()


def load_user_dataset(user_id):
    latest_upload = get_latest_upload(user_id)

    if not latest_upload:
        return empty_dataset()

    file_path = latest_upload["file_path"]

    if not os.path.exists(file_path):
        return empty_dataset()

    try:
        if file_path.lower().endswith(".csv"):
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)
    except Exception:
        return empty_dataset()

    df.columns = df.columns.str.lower().str.strip().str.replace(" ", "_")

    # Flexible column support for different datasets
    if "date" not in df.columns:
        if "transactiondate" in df.columns:
            df["date"] = df["transactiondate"]
        elif "transaction_date" in df.columns:
            df["date"] = df["transaction_date"]
        elif "pay_date" in df.columns:
            df["date"] = df["pay_date"]
        else:
            df["date"] = pd.date_range(start="2026-01-01", periods=len(df), freq="D")

    if "description" not in df.columns:
        if "product_category" in df.columns:
            df["description"] = "Retail sale - " + df["product_category"].astype(str)
        elif "vendor" in df.columns:
            df["description"] = df["vendor"].astype(str)
        elif "category" in df.columns:
            df["description"] = df["category"].astype(str)
        elif "subcategory" in df.columns:
            df["description"] = df["subcategory"].astype(str)
        else:
            df["description"] = "Business transaction"

    if "category" not in df.columns:
        if "product_category" in df.columns:
            df["category"] = df["product_category"]
        elif "subcategory" in df.columns:
            df["category"] = df["subcategory"]
        else:
            df["category"] = "Miscellaneous"

    if "amount" not in df.columns:
        if "total_amount" in df.columns:
            df["amount"] = df["total_amount"]
        elif "total_sales_value" in df.columns:
            df["amount"] = df["total_sales_value"]
        elif "totalsalesvalue" in df.columns:
            df["amount"] = df["totalsalesvalue"]
        elif "transactionamount" in df.columns:
            df["amount"] = df["transactionamount"]
        elif "transaction_amount" in df.columns:
            df["amount"] = df["transaction_amount"]
        elif "gross_pay" in df.columns:
            df["amount"] = df["gross_pay"]
        else:
            df["amount"] = 0

    if "type" not in df.columns:
        if "income/expense" in df.columns:
            df["type"] = df["income/expense"]
        elif "product_category" in df.columns or "total_amount" in df.columns:
            df["type"] = "Income"
        elif "gross_pay" in df.columns:
            df["type"] = "Expense"
        else:
            df["type"] = "Expense"

    if "currency" not in df.columns:
        df["currency"] = "NGN"

    if "payment_method" not in df.columns:
        if "mode" in df.columns:
            df["payment_method"] = df["mode"]
        elif "transactionchannel" in df.columns:
            df["payment_method"] = df["transactionchannel"]
        elif "account" in df.columns:
            df["payment_method"] = df["account"]
        else:
            df["payment_method"] = "Unknown"

    if "source" not in df.columns:
        df["source"] = "user_upload"

    df["date"] = pd.to_datetime(df["date"], errors="coerce", dayfirst=True)

    df["amount"] = (
        df["amount"]
        .astype(str)
        .str.replace("₦", "", regex=False)
        .str.replace("NGN", "", regex=False)
        .str.replace("$", "", regex=False)
        .str.replace("USD", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.strip()
    )

    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df = df.dropna(subset=["date", "amount"])
    df = df[df["amount"] > 0]

    # Convert USD to NGN
    USD_TO_NGN = 1400
    df["currency"] = df["currency"].astype(str).str.upper().str.strip()

    usd_mask = df["currency"].isin(["USD", "$", "US DOLLAR", "DOLLAR"])
    df.loc[usd_mask, "amount"] = df.loc[usd_mask, "amount"] * USD_TO_NGN

    df["currency"] = "NGN"

    df["type"] = df["type"].astype(str).str.lower().str.strip()

    def normalize_type(value):
        value = str(value).lower().strip()

        income_words = ["income", "credit", "revenue", "sales", "sale", "deposit"]
        expense_words = ["expense", "debit", "payment", "pay", "withdrawal", "purchase", "cost"]

        if any(word in value for word in income_words):
            return "Income"

        if any(word in value for word in expense_words):
            return "Expense"

        return "Expense"

    df["type"] = df["type"].apply(normalize_type)

    return df[EMPTY_COLUMNS]


def calculate_summary(df):
    income = df[df["type"] == "Income"]["amount"].sum()
    expenses = df[df["type"] == "Expense"]["amount"].sum()
    profit = income - expenses
    profit_margin = (profit / income) * 100 if income > 0 else 0

    return {
        "total_income": income,
        "total_expenses": expenses,
        "net_profit": profit,
        "profit_margin": profit_margin,
        "transactions": len(df)
    }


def monthly_trend(df):
    if df.empty:
        return pd.DataFrame(columns=["month", "Income", "Expense", "Profit"])

    df = df.copy()
    df["month"] = df["date"].dt.to_period("M").astype(str)

    trend = df.pivot_table(
        index="month",
        columns="type",
        values="amount",
        aggfunc="sum",
        fill_value=0
    ).reset_index()

    if "Income" not in trend.columns:
        trend["Income"] = 0

    if "Expense" not in trend.columns:
        trend["Expense"] = 0

    trend["Profit"] = trend["Income"] - trend["Expense"]

    return trend.tail(12)


def category_summary(df):
    if df.empty:
        return pd.DataFrame(columns=["category", "amount"])

    expenses = df[df["type"] == "Expense"]

    if expenses.empty:
        return pd.DataFrame(columns=["category", "amount"])

    category_data = expenses.groupby("category")["amount"].sum()
    category_data = category_data.sort_values(ascending=False).head(8)

    return category_data.reset_index()