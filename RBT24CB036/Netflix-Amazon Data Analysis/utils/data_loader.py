"""
data_loader.py — CSV/Excel loading, feature engineering, target detection.
"""
import pandas as pd
import numpy as np
import streamlit as st


@st.cache_data
def load_csv(path):
    """Load a CSV file and return a DataFrame."""
    return pd.read_csv(path)


@st.cache_data
def load_uploaded(file):
    """Load an uploaded file (CSV or Excel)."""
    name = file.name.lower()
    if name.endswith(".csv"):
        return pd.read_csv(file)
    elif name.endswith((".xls", ".xlsx")):
        return pd.read_excel(file)
    else:
        st.error("Unsupported file type. Use CSV or Excel.")
        return None


def engineer_features(df):
    """
    Extract numeric features from the streaming dataset so that
    PCA/LDA/correlation/etc. have columns to work with.
    """
    df = df.copy()

    # Parse date_added → year_added, month_added
    df["date_added"] = pd.to_datetime(df["date_added"], errors="coerce")
    df["year_added"] = df["date_added"].dt.year
    df["month_added"] = df["date_added"].dt.month

    # duration → duration_int (minutes for movies, seasons for TV)
    if "duration" in df.columns:
        df["duration_int"] = df["duration"].str.extract(r"(\d+)").astype(float)

    # Number of genres listed
    if "listed_in" in df.columns:
        df["genre_count"] = df["listed_in"].str.split(",").apply(
            lambda x: len(x) if isinstance(x, list) else 0)

    # Title length
    if "title" in df.columns:
        df["title_length"] = df["title"].astype(str).str.len()

    # Number of cast members
    if "cast" in df.columns:
        df["cast_count"] = df["cast"].fillna("").str.split(",").apply(
            lambda x: len(x) if x != [""] else 0)

    # Number of countries
    if "country" in df.columns:
        df["country_count"] = df["country"].fillna("").str.split(",").apply(
            lambda x: len(x) if x != [""] else 0)

    # Description length
    if "description" in df.columns:
        df["desc_length"] = df["description"].astype(str).str.len()

    # is_movie binary
    if "type" in df.columns:
        df["is_movie"] = (df["type"] == "Movie").astype(int)

    return df


def detect_target(df, threshold=20):
    """Auto-detect a likely target column."""
    hints = ["type", "label", "class", "target", "category", "rating"]
    candidates = []
    for col in df.columns:
        n_unique = df[col].nunique()
        if n_unique < threshold and df[col].dtype == "object":
            priority = 0
            for h in hints:
                if h in col.lower():
                    priority = 10
                    break
            candidates.append((col, n_unique, priority))
    if not candidates:
        return None
    candidates.sort(key=lambda x: (-x[2], x[1]))
    return candidates[0][0]


def get_column_types(df):
    """Return dict of numeric, categorical, datetime column lists."""
    numeric = df.select_dtypes(include="number").columns.tolist()
    categorical = df.select_dtypes(include=["object", "category"]).columns.tolist()
    datetime = df.select_dtypes(include="datetime").columns.tolist()
    return {"numeric": numeric, "categorical": categorical, "datetime": datetime}
