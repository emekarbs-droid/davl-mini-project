"""
stats.py — Descriptive statistics, Shapiro-Wilk test, stat matrices.
"""
import pandas as pd
import numpy as np
import streamlit as st
from scipy import stats as sp_stats


def show_descriptive_stats(df, name="Dataset"):
    """Show df.describe() for numeric and categorical columns."""
    st.subheader(f"📐 Descriptive Statistics — {name}")

    # Numeric
    num = df.select_dtypes(include="number")
    if len(num.columns) > 0:
        st.markdown("**Numeric Columns**")
        desc = num.describe().T
        desc["skew"] = num.skew()
        desc["kurtosis"] = num.kurtosis()
        desc["variance"] = num.var()
        desc["IQR"] = desc["75%"] - desc["25%"]
        st.dataframe(desc.round(3), use_container_width=True)

    # Categorical
    cat = df.select_dtypes(include="object")
    if len(cat.columns) > 0:
        st.markdown("**Categorical Columns**")
        cat_desc = cat.describe().T
        cat_desc["missing"] = cat.isnull().sum()
        st.dataframe(cat_desc, use_container_width=True)


def show_shapiro_test(df, name="Dataset"):
    """Run Shapiro-Wilk normality test on numeric columns."""
    st.subheader(f"🧪 Shapiro-Wilk Normality Test — {name}")

    num_cols = df.select_dtypes(include="number").columns.tolist()
    if not num_cols:
        st.info("No numeric columns for testing.")
        return

    results = []
    for col in num_cols:
        data = df[col].dropna()
        if len(data) > 5000:
            data = data.sample(5000, random_state=42)
        if len(data) < 3:
            continue
        try:
            stat, p = sp_stats.shapiro(data)
            results.append({
                "Column": col,
                "Statistic": round(stat, 6),
                "p-value": round(p, 6),
                "Normal (α=0.05)": "Yes ✅" if p > 0.05 else "No ❌",
            })
        except Exception:
            pass

    if results:
        st.dataframe(pd.DataFrame(results), use_container_width=True, hide_index=True)
        st.caption("H₀: Data is normally distributed. Reject if p < 0.05.")
    else:
        st.info("Could not run test on any column.")


def show_stat_matrices(df, name="Dataset"):
    """Show covariance and correlation matrices."""
    st.subheader(f"📊 Statistical Matrices — {name}")

    num = df.select_dtypes(include="number")
    if len(num.columns) < 2:
        st.info("Need at least 2 numeric columns.")
        return

    tab1, tab2 = st.tabs(["Correlation Matrix", "Covariance Matrix"])

    with tab1:
        corr = num.corr().round(3)
        st.dataframe(corr, use_container_width=True)

    with tab2:
        cov = num.cov().round(3)
        st.dataframe(cov, use_container_width=True)
