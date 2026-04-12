"""
insights.py — Auto-generated text insights from the data.
"""
import pandas as pd
import numpy as np
import streamlit as st


def generate_insights(df, name="Dataset"):
    """Auto-generate text-based insights about the dataset."""
    st.subheader(f"💡 Insights — {name}")

    insights = []

    # Shape
    insights.append(f"The dataset contains **{len(df):,}** rows and **{len(df.columns)}** columns.")

    # Missing data
    total_missing = df.isnull().sum().sum()
    total_cells = df.shape[0] * df.shape[1]
    pct = round(total_missing / total_cells * 100, 2)
    insights.append(f"**{total_missing:,}** cells are missing ({pct}% of all data).")

    # Most missing column
    miss_col = df.isnull().sum().idxmax()
    miss_val = df.isnull().sum().max()
    if miss_val > 0:
        insights.append(f"The column with the most missing values is **'{miss_col}'** with {miss_val:,} nulls ({round(miss_val/len(df)*100,1)}%).")

    # Duplicates
    dup = df.duplicated().sum()
    insights.append(f"There are **{dup}** duplicate rows.")

    # Numeric stats
    num_cols = df.select_dtypes(include="number").columns.tolist()
    if num_cols:
        # Most variable column
        stds = df[num_cols].std()
        most_var = stds.idxmax()
        insights.append(f"The most variable numeric column is **'{most_var}'** (std = {stds.max():.2f}).")

        # Skewness
        skews = df[num_cols].skew()
        highly_skewed = skews[skews.abs() > 1]
        if len(highly_skewed) > 0:
            cols = ", ".join([f"'{c}'" for c in highly_skewed.index])
            insights.append(f"Highly skewed columns (|skew| > 1): {cols}.")

    # Categorical
    cat_cols = df.select_dtypes(include="object").columns.tolist()
    if cat_cols:
        for col in cat_cols[:3]:
            top = df[col].value_counts().head(1)
            if len(top) > 0:
                insights.append(f"Most common value in **'{col}'**: '{top.index[0]}' ({top.values[0]:,} occurrences, {round(top.values[0]/len(df)*100,1)}%).")

    # Unique counts
    high_cardinality = [(col, df[col].nunique()) for col in cat_cols if df[col].nunique() > 100]
    if high_cardinality:
        for col, n in high_cardinality:
            insights.append(f"**'{col}'** has high cardinality: {n} unique values.")

    # Display
    for i, insight in enumerate(insights, 1):
        st.markdown(f"{i}. {insight}")
