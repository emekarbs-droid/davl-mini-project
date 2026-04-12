import pandas as pd


def build_model_frame(df: pd.DataFrame, expense_cols: list[str]) -> pd.DataFrame:
    """
    Selects relevant demographic and financial features for the ML models,
    including any specific expense category distributions dynamically grouped.
    """
    feature_columns = [column for column in ["income", "age", "dependents", "city_tier", "occupation", "total_expense"] + expense_cols if column in df.columns]
    return df[feature_columns].copy()
