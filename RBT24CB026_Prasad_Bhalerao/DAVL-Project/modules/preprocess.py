import pandas as pd

from modules.config import CATEGORY_MAP, PAYMENT_MAP


def parse_mixed_dates(series: pd.Series) -> pd.Series:
    """
    Parses a Pandas Series containing mixed date formats (US vs UK, missing separators) 
    into a standardized datetime format.
    """
    values = series.astype(str).str.strip()
    # Try parsing safely first
    parsed = pd.to_datetime(values, errors="coerce", dayfirst=False)
    unresolved = parsed.isna()
    
    # Fallback for remaining unresolved dates using dayfirst=True
    if unresolved.any():
        parsed.loc[unresolved] = pd.to_datetime(values[unresolved], errors="coerce", dayfirst=True)
    return parsed


def preprocess_transactions(raw: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, int]]:
    """
    Cleans raw transaction data by normalizing categories, parsing mixed date formats, 
    and extracting numeric currency values using Regex.
    """
    df = raw.copy()

    if "category" in df.columns:
        df["category"] = df["category"].astype(str).str.strip().str.lower().replace(CATEGORY_MAP)
    if "payment_mode" in df.columns:
        df["payment_mode"] = df["payment_mode"].astype(str).str.strip().str.lower().replace(PAYMENT_MAP)
    if "transaction_type" in df.columns:
        df["transaction_type"] = df["transaction_type"].astype(str).str.strip().str.lower()

    non_numeric_amounts = 0
    if "amount" in df.columns:
        amount_text = df["amount"].astype(str)
        non_numeric_amounts = int(amount_text.str.contains(r"[^0-9.\-]", regex=True, na=False).sum())
        cleaned_amount = amount_text.str.replace(r"[^0-9.\-]", "", regex=True)
        df["amount"] = pd.to_numeric(cleaned_amount, errors="coerce")

    invalid_dates = 0
    if "date" in df.columns:
        df["date"] = parse_mixed_dates(df["date"])
        invalid_dates = int(df["date"].isna().sum())

    before_drop = len(df)
    if {"amount", "date", "category"}.issubset(df.columns):
        df = df.dropna(subset=["amount", "date", "category"])
    dropped_missing = before_drop - len(df)

    removed_outliers = 0
    if "amount" in df.columns and len(df) > 2:
        q1 = df["amount"].quantile(0.25)
        q3 = df["amount"].quantile(0.75)
        iqr = q3 - q1
        low = q1 - 1.5 * iqr
        high = q3 + 1.5 * iqr
        before_outlier = len(df)
        df = df[(df["amount"] >= low) & (df["amount"] <= high)]
        removed_outliers = before_outlier - len(df)

    if "date" in df.columns:
        df["year_month"] = df["date"].dt.to_period("M").astype(str)

    summary = {
        "non_numeric_amount_values": non_numeric_amounts,
        "invalid_dates": invalid_dates,
        "rows_dropped_core_missing": dropped_missing,
        "rows_removed_outliers": removed_outliers,
    }
    return df, summary


def preprocess_structured(raw: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    df = raw.copy()

    for column in ["occupation", "city_tier"]:
        if column in df.columns:
            df[column] = df[column].astype(str).str.strip()

    for column in df.columns:
        if column not in {"occupation", "city_tier"}:
            df[column] = pd.to_numeric(df[column], errors="coerce")

    expense_candidates = [
        "rent",
        "loan_repayment",
        "insurance",
        "groceries",
        "transport",
        "eating_out",
        "entertainment",
        "utilities",
        "healthcare",
        "education",
        "miscellaneous",
    ]
    expense_cols = [column for column in expense_candidates if column in df.columns]

    if expense_cols:
        df["total_expense"] = df[expense_cols].sum(axis=1)

    if {"desired_savings", "income"}.issubset(df.columns):
        df["savings_ratio"] = pd.NA
        valid_income = df["income"] > 0
        df.loc[valid_income, "savings_ratio"] = df.loc[valid_income, "desired_savings"] / df.loc[valid_income, "income"]

    df = df.replace([float("inf"), float("-inf")], pd.NA)
    if {"income", "desired_savings", "total_expense"}.issubset(df.columns):
        df = df.dropna(subset=["income", "desired_savings", "total_expense"])

    return df, expense_cols
