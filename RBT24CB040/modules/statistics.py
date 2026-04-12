"""
statistics.py
-------------
Statistical summary: descriptive stats, skewness, kurtosis, correlation matrix,
covariance matrix.
"""

import pandas as pd
import numpy as np
import streamlit as st
from scipy import stats as scipy_stats


def show_statistics(df: pd.DataFrame):
    """Render full statistical summary section."""
    st.subheader("📐 Statistical Summary")

    numeric_df = df.select_dtypes(include=np.number)

    if numeric_df.empty:
        st.warning("No numeric columns found for statistical analysis.")
        return

    _descriptive_stats(numeric_df)
    _skewness_kurtosis(numeric_df)
    _correlation_matrix(numeric_df)
    _covariance_matrix(numeric_df)
    _normality_tests(numeric_df)


def _descriptive_stats(numeric_df: pd.DataFrame):
    st.markdown("#### 📊 Descriptive Statistics")
    desc = numeric_df.describe().T
    desc["mode"] = numeric_df.mode().iloc[0]
    desc["variance"] = numeric_df.var()
    desc["median"] = numeric_df.median()

    # Reorder columns
    cols_order = ["count", "mean", "median", "mode", "std", "variance",
                  "min", "25%", "50%", "75%", "max"]
    cols_order = [c for c in cols_order if c in desc.columns]
    desc = desc[cols_order].round(4)

    st.dataframe(desc, use_container_width=True)


def _skewness_kurtosis(numeric_df: pd.DataFrame):
    st.markdown("#### 📈 Skewness & Kurtosis")
    sk_df = pd.DataFrame({
        "Column": numeric_df.columns,
        "Skewness": numeric_df.skew().round(4).values,
        "Kurtosis": numeric_df.kurtosis().round(4).values,
    })

    def skew_label(s):
        if abs(s) < 0.5:
            return "✅ Approx. Normal"
        elif abs(s) < 1.0:
            return "🟡 Moderate Skew"
        else:
            return "🔴 High Skew"

    def kurt_label(k):
        if abs(k) < 1:
            return "✅ Mesokurtic"
        elif k > 1:
            return "🔼 Leptokurtic (heavy tails)"
        else:
            return "🔽 Platykurtic (light tails)"

    sk_df["Skew Interpretation"] = sk_df["Skewness"].apply(skew_label)
    sk_df["Kurt Interpretation"] = sk_df["Kurtosis"].apply(kurt_label)

    st.dataframe(sk_df, use_container_width=True)


def _correlation_matrix(numeric_df: pd.DataFrame):
    st.markdown("#### 🔗 Correlation Matrix (Pearson)")
    corr = numeric_df.corr(method="pearson").round(3)
    st.dataframe(corr.style.background_gradient(cmap="RdYlGn", axis=None,
                                                vmin=-1, vmax=1),
                 use_container_width=True)

    # Highly correlated pairs
    st.markdown("##### 🔥 Highly Correlated Pairs (|r| ≥ 0.8)")
    high_corr = []
    for i in range(len(corr.columns)):
        for j in range(i + 1, len(corr.columns)):
            val = corr.iloc[i, j]
            if abs(val) >= 0.8:
                high_corr.append({
                    "Feature 1": corr.columns[i],
                    "Feature 2": corr.columns[j],
                    "Correlation": round(val, 4),
                })
    if high_corr:
        st.dataframe(pd.DataFrame(high_corr), use_container_width=True)
    else:
        st.success("✅ No pairs with |r| ≥ 0.8 found.")


def _covariance_matrix(numeric_df: pd.DataFrame):
    st.markdown("#### 📐 Covariance Matrix")
    with st.expander("Show Covariance Matrix"):
        cov = numeric_df.cov().round(4)
        st.dataframe(cov, use_container_width=True)


def _normality_tests(numeric_df: pd.DataFrame):
    st.markdown("#### 🔬 Normality Tests (Shapiro-Wilk, n ≤ 5000)")
    sample_df = numeric_df.dropna()
    if len(sample_df) > 5000:
        sample_df = sample_df.sample(5000, random_state=42)

    results = []
    for col in sample_df.columns:
        series = sample_df[col].dropna()
        if len(series) < 3:
            continue
        try:
            stat, p = scipy_stats.shapiro(series)
            results.append({
                "Column": col,
                "W Statistic": round(float(stat), 5),
                "p-value": round(float(p), 5),
                "Normal (α=0.05)": "✅ Yes" if p > 0.05 else "❌ No",
            })
        except Exception:
            pass

    if results:
        st.dataframe(pd.DataFrame(results), use_container_width=True)


def get_correlation_pairs(df: pd.DataFrame, threshold: float = 0.8) -> list:
    """Helper: return list of (col1, col2, corr) for high correlation pairs."""
    numeric_df = df.select_dtypes(include=np.number)
    corr = numeric_df.corr().abs()
    pairs = []
    cols = corr.columns.tolist()
    for i in range(len(cols)):
        for j in range(i + 1, len(cols)):
            val = corr.iloc[i, j]
            if val >= threshold:
                pairs.append((cols[i], cols[j], round(float(val), 4)))
    return pairs
