"""
overview.py — Dataset overview & KPI cards.
"""
import pandas as pd
import streamlit as st


def show_overview(df, name="Dataset"):
    """Display dataset overview with KPI cards and basic info."""
    st.subheader(f"📋 {name} — Overview")

    # KPI row
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Rows", f"{len(df):,}")
    c2.metric("Columns", len(df.columns))
    c3.metric("Numeric", len(df.select_dtypes(include='number').columns))
    c4.metric("Categorical", len(df.select_dtypes(include='object').columns))
    c5.metric("Missing Cells", f"{df.isnull().sum().sum():,}")

    # More metrics
    c1, c2, c3 = st.columns(3)
    c1.metric("Duplicated Rows", f"{df.duplicated().sum():,}")
    total_cells = df.shape[0] * df.shape[1]
    missing_pct = round(df.isnull().sum().sum() / total_cells * 100, 2)
    c2.metric("Missing %", f"{missing_pct}%")
    mem = df.memory_usage(deep=True).sum()
    c3.metric("Memory", f"{mem / 1024:.1f} KB" if mem < 1_048_576 else f"{mem / 1_048_576:.1f} MB")

    # Shape
    st.info(f"**Shape:** {df.shape[0]} rows × {df.shape[1]} columns")

    # Columns & types
    with st.expander("Column Names & Data Types"):
        type_df = pd.DataFrame({
            "Column": df.columns,
            "Dtype": df.dtypes.astype(str).values,
            "Non-Null": df.notnull().sum().values,
            "Null": df.isnull().sum().values,
            "Unique": df.nunique().values,
        })
        st.dataframe(type_df, use_container_width=True, hide_index=True)

    # Head & tail
    with st.expander("First 5 Rows (head)"):
        st.dataframe(df.head(), use_container_width=True)

    with st.expander("Last 5 Rows (tail)"):
        st.dataframe(df.tail(), use_container_width=True)

    # df.info() style
    with st.expander("df.info() Summary"):
        import io
        buf = io.StringIO()
        df.info(buf=buf)
        st.code(buf.getvalue(), language="text")
