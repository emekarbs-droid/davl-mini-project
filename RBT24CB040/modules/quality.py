"""
quality.py
----------
Data Quality Analysis: missing values, duplicates, constant columns,
high cardinality, outliers, class imbalance.
"""

import pandas as pd
import numpy as np
import streamlit as st
from scipy import stats


def show_quality(df: pd.DataFrame, target: str = None):
    """Render full data quality analysis."""
    st.subheader("🔍 Data Quality Analysis")

    _missing_values(df)
    _duplicates(df)
    _constant_columns(df)
    _high_cardinality(df)
    _outlier_detection(df)
    if target and target in df.columns:
        _class_imbalance(df, target)


# ── Missing Values ────────────────────────────────────────────────────────────

def _missing_values(df: pd.DataFrame):
    st.markdown("#### 🕳️ Missing Values")
    null_counts = df.isnull().sum()
    null_pct = (null_counts / len(df) * 100).round(2)
    miss_df = pd.DataFrame({
        "Column": null_counts.index,
        "Missing Count": null_counts.values,
        "Missing %": null_pct.values,
        "Dtype": [str(df[c].dtype) for c in null_counts.index],
    })
    miss_df = miss_df[miss_df["Missing Count"] > 0].sort_values("Missing %", ascending=False)

    total_missing = df.isnull().sum().sum()
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Missing Cells", f"{total_missing:,}")
    col2.metric("Columns with Nulls", len(miss_df))
    col3.metric("Overall Missing %", f"{(total_missing / df.size * 100):.2f}%")

    if miss_df.empty:
        st.success("✅ No missing values found!")
    else:
        st.dataframe(miss_df.reset_index(drop=True), use_container_width=True)

        # Severity tags
        for _, row in miss_df.iterrows():
            pct = row["Missing %"]
            if pct > 50:
                st.warning(f"⚠️ **{row['Column']}** has {pct}% missing — consider dropping this column.")
            elif pct > 20:
                st.info(f"ℹ️ **{row['Column']}** has {pct}% missing — imputation recommended.")


# ── Duplicates ────────────────────────────────────────────────────────────────

def _duplicates(df: pd.DataFrame):
    st.markdown("#### 🔄 Duplicate Rows")
    dup_count = df.duplicated().sum()
    dup_pct = round(dup_count / len(df) * 100, 2)

    col1, col2 = st.columns(2)
    col1.metric("Duplicate Rows", f"{dup_count:,}")
    col2.metric("Duplicate %", f"{dup_pct}%")

    if dup_count > 0:
        st.warning(f"⚠️ {dup_count} duplicate rows detected ({dup_pct}% of data).")
        with st.expander("View Duplicate Rows"):
            st.dataframe(df[df.duplicated(keep=False)].head(50), use_container_width=True)
    else:
        st.success("✅ No duplicate rows found!")


# ── Constant Columns ──────────────────────────────────────────────────────────

def _constant_columns(df: pd.DataFrame):
    st.markdown("#### 📌 Constant / Near-Constant Columns")
    const_cols = [c for c in df.columns if df[c].nunique() <= 1]
    near_const = [c for c in df.columns
                  if 1 < df[c].nunique() <= max(2, int(len(df) * 0.01))]

    if const_cols:
        st.error(f"🔴 Constant columns (0 variance): **{const_cols}**")
    else:
        st.success("✅ No constant columns found.")

    if near_const:
        st.warning(f"🟡 Near-constant columns (< 1% unique): **{near_const}**")


# ── High Cardinality ──────────────────────────────────────────────────────────

def _high_cardinality(df: pd.DataFrame):
    st.markdown("#### 🔢 High Cardinality Columns")
    cat_cols = df.select_dtypes(include=["object", "category"]).columns
    hc_data = []
    for col in cat_cols:
        n_unique = df[col].nunique()
        pct = round(n_unique / len(df) * 100, 2)
        if n_unique > 50:
            hc_data.append({"Column": col, "Unique Values": n_unique, "Unique %": pct})

    if hc_data:
        hc_df = pd.DataFrame(hc_data).sort_values("Unique Values", ascending=False)
        st.warning("⚠️ High cardinality categorical columns detected:")
        st.dataframe(hc_df, use_container_width=True)
    else:
        st.success("✅ No high cardinality categorical columns (> 50 unique values).")


# ── Outlier Detection ─────────────────────────────────────────────────────────

def _outlier_detection(df: pd.DataFrame):
    st.markdown("#### 📊 Outlier Detection")
    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    if not numeric_cols:
        st.info("No numeric columns for outlier detection.")
        return

    outlier_data = []
    for col in numeric_cols:
        series = df[col].dropna()
        if len(series) == 0:
            continue

        # IQR method
        Q1, Q3 = series.quantile(0.25), series.quantile(0.75)
        IQR = Q3 - Q1
        iqr_outliers = int(((series < Q1 - 1.5 * IQR) | (series > Q3 + 1.5 * IQR)).sum())

        # Z-score method
        z_scores = np.abs(stats.zscore(series))
        z_outliers = int((z_scores > 3).sum())

        outlier_data.append({
            "Column": col,
            "IQR Outliers": iqr_outliers,
            "IQR Outlier %": round(iqr_outliers / len(df) * 100, 2),
            "Z-score Outliers (|z|>3)": z_outliers,
            "Z-score Outlier %": round(z_outliers / len(df) * 100, 2),
            "Skewness": round(float(series.skew()), 3),
        })

    out_df = pd.DataFrame(outlier_data)
    high_out = out_df[out_df["IQR Outlier %"] > 5]

    col1, col2 = st.columns(2)
    col1.metric("Columns with Outliers (IQR)", int((out_df["IQR Outliers"] > 0).sum()))
    col2.metric("High Outlier Columns (>5%)", len(high_out))

    st.dataframe(out_df, use_container_width=True)

    if not high_out.empty:
        st.warning(f"⚠️ High outlier columns: **{high_out['Column'].tolist()}** — consider capping or removal.")


# ── Class Imbalance ───────────────────────────────────────────────────────────

def _class_imbalance(df: pd.DataFrame, target: str):
    st.markdown(f"#### ⚖️ Class Imbalance — `{target}`")
    vc = df[target].value_counts()
    vc_pct = (vc / len(df) * 100).round(2)

    imb_df = pd.DataFrame({
        "Class": vc.index,
        "Count": vc.values,
        "Percentage %": vc_pct.values,
    })
    st.dataframe(imb_df, use_container_width=True)

    if len(vc) >= 2:
        ratio = vc.iloc[0] / vc.iloc[-1]
        if ratio > 3:
            st.warning(f"⚠️ Imbalance ratio {ratio:.1f}:1 — consider SMOTE or class weights.")
        else:
            st.success(f"✅ Classes are reasonably balanced (ratio {ratio:.1f}:1).")


def get_quality_summary(df: pd.DataFrame) -> dict:
    """Return a dict summary of quality metrics for the Insights module."""
    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    outlier_cols = []
    for col in numeric_cols:
        s = df[col].dropna()
        if len(s) == 0:
            continue
        Q1, Q3 = s.quantile(0.25), s.quantile(0.75)
        IQR = Q3 - Q1
        if ((s < Q1 - 1.5 * IQR) | (s > Q3 + 1.5 * IQR)).sum() / len(df) > 0.05:
            outlier_cols.append(col)

    return {
        "total_missing": int(df.isnull().sum().sum()),
        "missing_pct": round(df.isnull().sum().sum() / df.size * 100, 2),
        "duplicate_rows": int(df.duplicated().sum()),
        "constant_cols": [c for c in df.columns if df[c].nunique() <= 1],
        "high_cardinality_cols": [
            c for c in df.select_dtypes(include=["object", "category"]).columns
            if df[c].nunique() > 50
        ],
        "outlier_cols": outlier_cols,
        "cols_with_nulls": [c for c in df.columns if df[c].isnull().any()],
    }
