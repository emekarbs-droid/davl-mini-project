"""
data_loader.py
--------------
Handles CSV and Excel file loading, preview, and basic metadata.
"""

import pandas as pd
import streamlit as st
import io


SUPPORTED_EXTENSIONS = ["csv", "xlsx", "xls"]


def load_dataset(uploaded_file) -> pd.DataFrame:
    """Load a CSV or Excel file into a pandas DataFrame. Falls back to healthcare_dataset.csv if it exists."""
    import os
    
    # If explicitly passed a string filename
    if isinstance(uploaded_file, str):
        filename = uploaded_file.lower()
        file_to_read = uploaded_file
    elif uploaded_file is not None:
        filename = uploaded_file.name.lower()
        file_to_read = uploaded_file
    else:
        # Fall back to dataset if it exists locally
        if os.path.exists("healthcare_dataset.csv"):
            filename = "healthcare_dataset.csv"
            file_to_read = "healthcare_dataset.csv"
        else:
            return None

    try:
        if filename.endswith(".csv"):
            df = pd.read_csv(file_to_read)
        elif filename.endswith(".xlsx"):
            df = pd.read_excel(file_to_read, engine="openpyxl")
        elif filename.endswith(".xls"):
            df = pd.read_excel(file_to_read, engine="xlrd")
        else:
            st.error("Unsupported file format. Please upload a CSV or Excel file.")
            return None
        return df
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None


def show_preview(df: pd.DataFrame, n_rows: int = 5):
    """Display dataset head, tail, shape and column list."""
    st.subheader("📋 Dataset Preview")

    col1, col2, col3 = st.columns(3)
    col1.metric("Rows", df.shape[0])
    col2.metric("Columns", df.shape[1])
    col3.metric("Total Cells", df.shape[0] * df.shape[1])

    tab_head, tab_tail = st.tabs(["First Rows", "Last Rows"])
    with tab_head:
        st.dataframe(df.head(n_rows), use_container_width=True)
    with tab_tail:
        st.dataframe(df.tail(n_rows), use_container_width=True)

    with st.expander("Column Names"):
        st.write(list(df.columns))


def get_csv_download(df: pd.DataFrame, label: str = "processed_data.csv") -> bytes:
    """Return CSV bytes for download."""
    return df.to_csv(index=False).encode("utf-8")
