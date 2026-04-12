from pathlib import Path

DATA_DIR = Path("data")
TRANSACTIONS_FILE = DATA_DIR / "budgetwise_finance_dataset.csv"
STRUCTURED_FILE = DATA_DIR / "IndianPersonalFinance.csv"

CATEGORY_MAP = {
    "foodd": "food",
    "foods": "food",
    "fod": "food",
    "rentt": "rent",
    "rnt": "rent",
    "traval": "travel",
    "travl": "travel",
    "utilties": "utilities",
    "utility": "utilities",
    "utlities": "utilities",
    "entrtnmnt": "entertainment",
    "entertain": "entertainment",
    "educaton": "education",
}

PAYMENT_MAP = {
    "csh": "cash",
    "crd": "card",
    "bank transfr": "bank transfer",
    "banktransfer": "bank transfer",
    "bank_transfer": "bank transfer",
}
