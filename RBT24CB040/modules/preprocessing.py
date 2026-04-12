"""
preprocessing.py
----------------
Automated preprocessing pipeline:
 - Missing value imputation
 - Duplicate removal
 - Categorical encoding
 - Feature scaling (StandardScaler)
 - IQR-based outlier capping
 - Feature selection (correlation + variance threshold)
"""

import pandas as pd
import numpy as np
import streamlit as st
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.feature_selection import VarianceThreshold


def run_preprocessing(df: pd.DataFrame, target: str = None,
                      options: dict = None) -> pd.DataFrame:
    """
    Run the full preprocessing pipeline with user-selected options.
    Returns the cleaned DataFrame.
    """
    if options is None:
        options = {}

    df = df.copy()
    steps_log = []

    # 1. Remove duplicates
    if options.get("remove_duplicates", True):
        before = len(df)
        df = df.drop_duplicates()
        removed = before - len(df)
        if removed:
            steps_log.append(f"✅ Removed **{removed}** duplicate rows.")

    # 2. Drop constant columns
    if options.get("drop_constant", True):
        const_cols = [c for c in df.columns if df[c].nunique() <= 1
                      and c != target]
        if const_cols:
            df.drop(columns=const_cols, inplace=True)
            steps_log.append(f"✅ Dropped constant columns: **{const_cols}**")

    # 3. Impute missing values
    if options.get("impute_missing", True):
        strategy = options.get("impute_strategy", "median")
        for col in df.columns:
            if df[col].isnull().any():
                if pd.api.types.is_numeric_dtype(df[col]):
                    if strategy == "mean":
                        fill_val = df[col].mean()
                    elif strategy == "mode":
                        fill_val = df[col].mode()[0]
                    else:
                        fill_val = df[col].median()
                    df[col].fillna(fill_val, inplace=True)
                else:
                    df[col].fillna(df[col].mode()[0] if not df[col].mode().empty
                                   else "Unknown", inplace=True)
        steps_log.append(f"✅ Imputed missing values using **{strategy}** strategy.")

    # 4. Cap outliers using IQR
    if options.get("cap_outliers", True):
        numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
        if target and target in numeric_cols:
            # Don't cap target
            numeric_cols = [c for c in numeric_cols if c != target]
        for col in numeric_cols:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower = Q1 - 1.5 * IQR
            upper = Q3 + 1.5 * IQR
            df[col] = df[col].clip(lower, upper)
        steps_log.append(f"✅ Outliers capped using IQR method on {len(numeric_cols)} numeric columns.")

    # 5. Encode categoricals
    if options.get("encode_categoricals", True):
        cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
        if target and target in cat_cols:
            # Encode target separately with label encoder
            le = LabelEncoder()
            df[target] = le.fit_transform(df[target].astype(str))
            cat_cols = [c for c in cat_cols if c != target]

        low_card = [c for c in cat_cols if df[c].nunique() <= 10]
        high_card = [c for c in cat_cols if df[c].nunique() > 10]

        if low_card:
            df = pd.get_dummies(df, columns=low_card, drop_first=False)
            steps_log.append(f"✅ One-hot encoded low-cardinality columns: **{low_card}**")

        if high_card:
            le = LabelEncoder()
            for col in high_card:
                df[col] = le.fit_transform(df[col].astype(str))
            steps_log.append(f"✅ Label encoded high-cardinality columns: **{high_card}**")

    # 6. Variance threshold feature selection
    if options.get("variance_threshold", False):
        numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
        feat_cols = [c for c in numeric_cols if c != target]
        if feat_cols:
            selector = VarianceThreshold(threshold=0.01)
            selector.fit(df[feat_cols])
            low_var = [c for c, s in zip(feat_cols, selector.get_support()) if not s]
            if low_var:
                df.drop(columns=low_var, inplace=True)
                steps_log.append(f"✅ Removed low-variance features: **{low_var}**")

    # 7. Standard scaling
    if options.get("scale_features", True):
        numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
        scale_cols = [c for c in numeric_cols if c != target]
        if scale_cols:
            scaler = StandardScaler()
            df[scale_cols] = scaler.fit_transform(df[scale_cols])
            steps_log.append(f"✅ StandardScaler applied to {len(scale_cols)} numeric columns.")

    return df, steps_log


def show_preprocessing(df: pd.DataFrame, target: str = None) -> pd.DataFrame:
    """
    Render preprocessing UI and return processed DataFrame.
    """
    st.subheader("⚙️ Preprocessing Pipeline")
    st.markdown("Configure and run automated preprocessing on your dataset.")

    with st.expander("⚙️ Preprocessing Options", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            remove_dups = st.checkbox("Remove Duplicate Rows", value=True)
            drop_const = st.checkbox("Drop Constant Columns", value=True)
            impute_miss = st.checkbox("Impute Missing Values", value=True)
            impute_strat = st.selectbox("Imputation Strategy",
                                        ["median", "mean", "mode"], index=0)
        with col2:
            cap_out = st.checkbox("Cap Outliers (IQR)", value=True)
            encode_cat = st.checkbox("Encode Categorical Features", value=True)
            scale_feat = st.checkbox("Scale Features (StandardScaler)", value=True)
            var_thresh = st.checkbox("Remove Low-Variance Features", value=False)

    options = {
        "remove_duplicates": remove_dups,
        "drop_constant": drop_const,
        "impute_missing": impute_miss,
        "impute_strategy": impute_strat,
        "cap_outliers": cap_out,
        "encode_categoricals": encode_cat,
        "scale_features": scale_feat,
        "variance_threshold": var_thresh,
    }

    processed_df, steps_log = run_preprocessing(df, target=target, options=options)

    st.markdown("#### 📋 Pipeline Steps Applied")
    for step in steps_log:
        st.markdown(f"- {step}")

    st.markdown("#### 📐 Processed Dataset Shape")
    c1, c2 = st.columns(2)
    c1.metric("Rows", processed_df.shape[0])
    c2.metric("Columns", processed_df.shape[1])

    st.markdown("#### 👁️ Processed Data Preview")
    st.dataframe(processed_df.head(10), use_container_width=True)

    return processed_df
