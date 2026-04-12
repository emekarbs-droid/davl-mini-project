import pandas as pd


def monthly_spending(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregates budgetwise transaction data by 'year_month'
    to create a time series of spending trends over the dataset range.
    """
    return (
        df.groupby("year_month", as_index=False)["amount"]
        .sum()
        .sort_values("year_month")
    )


def category_spending(df: pd.DataFrame, top_n: int = 12) -> pd.DataFrame:
    return (
        df.groupby("category", as_index=False)["amount"]
        .sum()
        .sort_values("amount", ascending=False)
        .head(top_n)
    )
