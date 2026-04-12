import pandas as pd

from modules.config import STRUCTURED_FILE, TRANSACTIONS_FILE


def _to_snake(columns: list[str]) -> list[str]:
    return [
        column.strip()
        .replace("%", "percentage")
        .replace("/", "_")
        .replace(" ", "_")
        .replace("-", "_")
        .lower()
        for column in columns
    ]


def load_datasets() -> tuple[pd.DataFrame, pd.DataFrame]:
    if not TRANSACTIONS_FILE.exists() or not STRUCTURED_FILE.exists():
        raise FileNotFoundError("Expected CSV files were not found inside the data folder.")

    transactions = pd.read_csv(TRANSACTIONS_FILE)
    structured = pd.read_csv(STRUCTURED_FILE)

    transactions.columns = _to_snake(transactions.columns.tolist())
    structured.columns = _to_snake(structured.columns.tolist())

    return transactions, structured
