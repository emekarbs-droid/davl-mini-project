"""
overview.py
-----------
Dataset overview: shape, dtypes, memory usage, unique values, target detection.
"""

import pandas as pd
import streamlit as st
import numpy as np


def detect_target_column(df: pd.DataFrame) -> str | None:
    """
    Heuristic target column detection:
    - Prefers columns named 'target', 'label', 'class', 'y', 'output', 'result'
    - Falls back to last column if it has low cardinality (< 20 unique values)
    """
    priority_names = {"target", "label", "class", "y", "output", "result",
                      "churn", "survived", "diagnosis", "outcome", "response",
                      "default", "fraud", "purchased", "converted"}

    for col in df.columns:
        if col.lower() in priority_names:
            return col

    # Fall back: last column with low cardinality
    last_col = df.columns[-1]
    if df[last_col].nunique() < 20:
        return last_col

    return None


def show_overview(df: pd.DataFrame) -> str:
    """Render dataset overview section. Returns detected target column name."""
    st.subheader("🗂️ Dataset Overview")

    # ── Shape & Memory ────────────────────────────────────────────────────────
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Rows", f"{df.shape[0]:,}")
    col2.metric("Columns", df.shape[1])
    mem_bytes = df.memory_usage(deep=True).sum()
    col3.metric("Memory Usage", _format_bytes(mem_bytes))
    col4.metric("Duplicates", int(df.duplicated().sum()))

    # ── Data Types ────────────────────────────────────────────────────────────
    st.markdown("#### 📊 Column Data Types & Unique Values")
    dtype_df = pd.DataFrame({
        "Column": df.columns,
        "Dtype": [str(df[c].dtype) for c in df.columns],
        "Non-Null Count": [df[c].notna().sum() for c in df.columns],
        "Null Count": [df[c].isna().sum() for c in df.columns],
        "Null %": [round(df[c].isna().mean() * 100, 2) for c in df.columns],
        "Unique Values": [df[c].nunique() for c in df.columns],
        "Sample Value": [str(df[c].dropna().iloc[0]) if df[c].notna().any() else "N/A"
                         for c in df.columns],
    })
    st.dataframe(dtype_df, use_container_width=True)

    # ── Column Type Summary ───────────────────────────────────────────────────
    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
    bool_cols = df.select_dtypes(include="bool").columns.tolist()
    datetime_cols = df.select_dtypes(include=["datetime", "datetimetz"]).columns.tolist()

    st.markdown("#### 🏷️ Column Type Breakdown")
    tc1, tc2, tc3, tc4 = st.columns(4)
    tc1.metric("Numeric", len(numeric_cols))
    tc2.metric("Categorical", len(cat_cols))
    tc3.metric("Boolean", len(bool_cols))
    tc4.metric("DateTime", len(datetime_cols))

    with st.expander("Numeric Columns"):
        st.write(numeric_cols if numeric_cols else "None")
    with st.expander("Categorical Columns"):
        st.write(cat_cols if cat_cols else "None")

    # ── Target Detection ──────────────────────────────────────────────────────
    target = detect_target_column(df)
    st.markdown("#### 🎯 Target Column Detection")
    if target:
        st.success(f"Detected target column: **`{target}`**  "
                   f"({df[target].nunique()} unique values)")
    else:
        st.info("No clear target column detected (unsupervised dataset).")

    return target


def _format_bytes(num: int) -> str:
    for unit in ["B", "KB", "MB", "GB"]:
        if num < 1024:
            return f"{num:.1f} {unit}"
        num /= 1024
    return f"{num:.1f} TB"
