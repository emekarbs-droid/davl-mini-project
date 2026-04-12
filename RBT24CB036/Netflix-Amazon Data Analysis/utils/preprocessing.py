"""
preprocessing.py — sklearn Pipeline: impute, encode, scale, feature selection.
"""
import pandas as pd
import numpy as np
import streamlit as st
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder, StandardScaler, MinMaxScaler
from sklearn.feature_selection import VarianceThreshold


def show_preprocessing(df, name="Dataset"):
    """Interactive preprocessing pipeline with before/after display."""
    st.subheader(f"⚙️ Preprocessing — {name}")

    df_processed = df.copy()
    steps_log = []

    # ── Step 1: Handle Duplicates ──
    st.markdown("**Step 1 — Remove Duplicates**")
    dup_count = df_processed.duplicated().sum()
    if dup_count > 0:
        df_processed = df_processed.drop_duplicates()
        steps_log.append(f"Removed {dup_count} duplicate rows.")
        st.success(f"✅ Removed {dup_count} duplicate rows. Shape: {df_processed.shape}")
    else:
        steps_log.append("No duplicates found.")
        st.info("No duplicates found.")

    # ── Step 2: Handle Missing Values ──
    st.markdown("**Step 2 — Impute Missing Values**")
    missing_before = df_processed.isnull().sum()
    cols_with_missing = missing_before[missing_before > 0].index.tolist()

    if cols_with_missing:
        num_missing = df_processed[cols_with_missing].select_dtypes(include="number").columns.tolist()
        cat_missing = df_processed[cols_with_missing].select_dtypes(include="object").columns.tolist()

        if num_missing:
            strategy = st.selectbox("Numeric imputation strategy",
                                    ["mean", "median", "most_frequent"],
                                    key=f"preproc_num_imp_{name}")
            imputer = SimpleImputer(strategy=strategy)
            df_processed[num_missing] = imputer.fit_transform(df_processed[num_missing])
            steps_log.append(f"Imputed {len(num_missing)} numeric columns with {strategy}: {', '.join(num_missing)}.")
            st.success(f"✅ Imputed numeric columns ({', '.join(num_missing)}) with {strategy}.")

        if cat_missing:
            fill_val = st.text_input("Fill categorical NaNs with",
                                     value="Unknown", key=f"preproc_cat_fill_{name}")
            df_processed[cat_missing] = df_processed[cat_missing].fillna(fill_val)
            steps_log.append(f"Filled {len(cat_missing)} categorical columns with '{fill_val}': {', '.join(cat_missing)}.")
            st.success(f"✅ Filled categorical columns ({', '.join(cat_missing)}) with '{fill_val}'.")
    else:
        st.info("No missing values to impute.")
        steps_log.append("No missing values.")

    # ── Step 3: Encode Categorical ──
    st.markdown("**Step 3 — Encode Categorical Columns**")
    cat_cols_all = df_processed.select_dtypes(include="object").columns.tolist()

    if cat_cols_all:
        encode_cols = st.multiselect("Select columns to label-encode",
                                     cat_cols_all, default=[],
                                     key=f"preproc_encode_{name}")
        if encode_cols:
            le = LabelEncoder()
            for col in encode_cols:
                df_processed[col] = le.fit_transform(df_processed[col].astype(str))
            steps_log.append(f"Label-encoded: {', '.join(encode_cols)}.")
            st.success(f"✅ Label-encoded {len(encode_cols)} columns.")
        else:
            st.info("No columns selected for encoding.")
    else:
        st.info("No categorical columns to encode.")

    # ── Step 4: Scale Numeric ──
    st.markdown("**Step 4 — Scale Numeric Columns**")
    num_cols_all = df_processed.select_dtypes(include="number").columns.tolist()

    if num_cols_all:
        scaler_type = st.selectbox("Scaler", ["None", "StandardScaler", "MinMaxScaler"],
                                   key=f"preproc_scaler_{name}")
        if scaler_type != "None":
            scale_cols = st.multiselect("Columns to scale", num_cols_all,
                                        default=num_cols_all, key=f"preproc_scale_cols_{name}")
            if scale_cols:
                scaler = StandardScaler() if scaler_type == "StandardScaler" else MinMaxScaler()
                df_processed[scale_cols] = scaler.fit_transform(df_processed[scale_cols])
                steps_log.append(f"Applied {scaler_type} to {len(scale_cols)} columns.")
                st.success(f"✅ Applied {scaler_type} to {len(scale_cols)} columns.")
    else:
        st.info("No numeric columns to scale.")

    # ── Step 5: Feature Selection (Variance Threshold) ──
    st.markdown("**Step 5 — Low Variance Filter**")
    num_only = df_processed.select_dtypes(include="number")
    if len(num_only.columns) > 1:
        threshold = st.slider("Variance threshold", 0.0, 1.0, 0.0,
                              step=0.01, key=f"preproc_var_thresh_{name}")
        if threshold > 0:
            selector = VarianceThreshold(threshold=threshold)
            try:
                selector.fit(num_only)
                kept = num_only.columns[selector.get_support()].tolist()
                removed = [c for c in num_only.columns if c not in kept]
                if removed:
                    df_processed = df_processed.drop(columns=removed)
                    steps_log.append(f"Removed low-variance columns: {', '.join(removed)}.")
                    st.warning(f"Removed: {', '.join(removed)}")
                else:
                    st.info("No columns removed.")
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.info("Threshold set to 0 — no columns removed.")

    # ── Summary ──
    st.markdown("---")
    st.markdown("**📋 Preprocessing Log:**")
    for i, step in enumerate(steps_log, 1):
        st.write(f"{i}. {step}")

    st.info(f"Final shape: **{df_processed.shape[0]}** rows × **{df_processed.shape[1]}** columns")

    with st.expander("Preview Preprocessed Data"):
        st.dataframe(df_processed.head(10), use_container_width=True)

    return df_processed
