"""
DAVL — Data Handler Module
Handles dataset loading, preview, overview, and target column detection.
"""

import pandas as pd
import numpy as np
import streamlit as st


def load_dataset(uploaded_file) -> pd.DataFrame:
    """Load a CSV or Excel file into a pandas DataFrame."""
    try:
        name = uploaded_file.name.lower()
        if name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        elif name.endswith((".xls", ".xlsx")):
            df = pd.read_excel(uploaded_file, engine="openpyxl")
        else:
            st.error("Unsupported file format. Please upload a CSV or Excel file.")
            return None

        if df.empty:
            st.warning("The uploaded file is empty.")
            return None

        return df
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None


def get_preview(df: pd.DataFrame, n: int = 10) -> dict:
    """Return head and tail previews of the DataFrame."""
    return {
        "head": df.head(n),
        "tail": df.tail(n),
        "sample": df.sample(min(n, len(df))),
    }


def get_overview(df: pd.DataFrame) -> dict:
    """Compute a comprehensive overview of the dataset."""
    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    categorical_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
    datetime_cols = df.select_dtypes(include=["datetime64"]).columns.tolist()
    boolean_cols = df.select_dtypes(include=["bool"]).columns.tolist()

    memory_usage_bytes = df.memory_usage(deep=True).sum()
    if memory_usage_bytes < 1024:
        memory_str = f"{memory_usage_bytes} B"
    elif memory_usage_bytes < 1024 ** 2:
        memory_str = f"{memory_usage_bytes / 1024:.2f} KB"
    else:
        memory_str = f"{memory_usage_bytes / (1024 ** 2):.2f} MB"

    dtypes_summary = df.dtypes.astype(str).value_counts().to_dict()

    unique_counts = df.nunique()

    overview = {
        "shape": df.shape,
        "rows": df.shape[0],
        "columns": df.shape[1],
        "numeric_columns": numeric_cols,
        "categorical_columns": categorical_cols,
        "datetime_columns": datetime_cols,
        "boolean_columns": boolean_cols,
        "num_numeric": len(numeric_cols),
        "num_categorical": len(categorical_cols),
        "num_datetime": len(datetime_cols),
        "num_boolean": len(boolean_cols),
        "memory_usage": memory_str,
        "memory_bytes": memory_usage_bytes,
        "dtypes_summary": dtypes_summary,
        "unique_counts": unique_counts,
        "dtypes": df.dtypes,
        "missing_total": df.isnull().sum().sum(),
        "duplicate_rows": df.duplicated().sum(),
    }
    return overview


def detect_target_column(df: pd.DataFrame) -> str | None:
    """
    Heuristic detection of the target / label column.
    Priority:
      1. Column named 'target', 'label', 'class', 'y', 'output'
      2. Last categorical column with low cardinality (2-20 unique)
      3. Last column if categorical with low cardinality
    Returns column name or None.
    """
    target_keywords = ["target", "label", "class", "output", "y"]

    # Check for exact name matches (case-insensitive)
    for col in df.columns:
        if col.strip().lower() in target_keywords:
            return col

    # Check for partial matches
    for col in df.columns:
        col_lower = col.strip().lower()
        for keyword in target_keywords:
            if keyword in col_lower:
                return col

    # Last categorical column with low cardinality
    cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
    for col in reversed(cat_cols):
        if 2 <= df[col].nunique() <= 20:
            return col

    # Last column check
    last_col = df.columns[-1]
    if df[last_col].nunique() <= 20:
        return last_col

    return None


def get_column_info(df: pd.DataFrame) -> pd.DataFrame:
    """Generate a detailed column information table."""
    info_data = []
    for col in df.columns:
        col_data = df[col]
        info_data.append({
            "Column": col,
            "Type": str(col_data.dtype),
            "Non-Null": col_data.notna().sum(),
            "Null": col_data.isna().sum(),
            "Null %": round(col_data.isna().mean() * 100, 2),
            "Unique": col_data.nunique(),
            "Sample Value": str(col_data.dropna().iloc[0]) if col_data.notna().any() else "N/A",
        })
    return pd.DataFrame(info_data)
