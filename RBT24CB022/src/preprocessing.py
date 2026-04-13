"""
DAVL — Preprocessing Module
Handle missing values, duplicates, encoding, scaling, outlier handling, feature selection.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.feature_selection import VarianceThreshold


def handle_missing_values(df: pd.DataFrame, strategy: str = "auto") -> tuple[pd.DataFrame, list[str]]:
    """
    Handle missing values in the dataset.
    Strategies: 'auto', 'mean', 'median', 'mode', 'drop_rows', 'drop_cols'
    Returns: (processed DataFrame, list of changes made)
    """
    df_clean = df.copy()
    changes = []

    if strategy == "drop_rows":
        before = len(df_clean)
        df_clean = df_clean.dropna()
        changes.append(f"Dropped {before - len(df_clean)} rows with missing values")
        return df_clean, changes

    if strategy == "drop_cols":
        cols_with_missing = df_clean.columns[df_clean.isnull().any()].tolist()
        df_clean = df_clean.drop(columns=cols_with_missing)
        changes.append(f"Dropped {len(cols_with_missing)} columns with missing values: {cols_with_missing}")
        return df_clean, changes

    numeric_cols = df_clean.select_dtypes(include=np.number).columns
    cat_cols = df_clean.select_dtypes(include=["object", "category"]).columns

    for col in numeric_cols:
        if df_clean[col].isnull().any():
            missing_count = df_clean[col].isnull().sum()
            if strategy == "auto" or strategy == "median":
                fill_val = df_clean[col].median()
                df_clean[col].fillna(fill_val, inplace=True)
                changes.append(f"Filled {missing_count} missing values in '{col}' with median ({fill_val:.4f})")
            elif strategy == "mean":
                fill_val = df_clean[col].mean()
                df_clean[col].fillna(fill_val, inplace=True)
                changes.append(f"Filled {missing_count} missing values in '{col}' with mean ({fill_val:.4f})")
            elif strategy == "mode":
                fill_val = df_clean[col].mode()[0] if not df_clean[col].mode().empty else 0
                df_clean[col].fillna(fill_val, inplace=True)
                changes.append(f"Filled {missing_count} missing values in '{col}' with mode ({fill_val})")

    for col in cat_cols:
        if df_clean[col].isnull().any():
            missing_count = df_clean[col].isnull().sum()
            fill_val = df_clean[col].mode()[0] if not df_clean[col].mode().empty else "Unknown"
            df_clean[col].fillna(fill_val, inplace=True)
            changes.append(f"Filled {missing_count} missing values in '{col}' with mode ('{fill_val}')")

    if not changes:
        changes.append("No missing values found — no changes needed")

    return df_clean, changes


def remove_duplicates(df: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    """Remove duplicate rows."""
    changes = []
    dup_count = df.duplicated().sum()
    if dup_count > 0:
        df_clean = df.drop_duplicates().reset_index(drop=True)
        changes.append(f"Removed {dup_count} duplicate rows")
    else:
        df_clean = df.copy()
        changes.append("No duplicate rows found")
    return df_clean, changes


def encode_categoricals(df: pd.DataFrame, method: str = "label") -> tuple[pd.DataFrame, list[str], dict]:
    """
    Encode categorical columns.
    Methods: 'label' (Label Encoding), 'onehot' (One-Hot Encoding)
    Returns: (processed DataFrame, list of changes, encoder mapping)
    """
    df_encoded = df.copy()
    changes = []
    encoders = {}
    cat_cols = df_encoded.select_dtypes(include=["object", "category"]).columns.tolist()

    if not cat_cols:
        changes.append("No categorical columns to encode")
        return df_encoded, changes, encoders

    if method == "label":
        for col in cat_cols:
            le = LabelEncoder()
            df_encoded[col] = le.fit_transform(df_encoded[col].astype(str))
            encoders[col] = dict(zip(le.classes_, le.transform(le.classes_)))
            changes.append(f"Label-encoded '{col}' ({df[col].nunique()} categories)")

    elif method == "onehot":
        df_encoded = pd.get_dummies(df_encoded, columns=cat_cols, drop_first=True, dtype=int)
        new_cols = [c for c in df_encoded.columns if c not in df.columns]
        changes.append(f"One-hot encoded {len(cat_cols)} columns → {len(new_cols)} new columns")

    return df_encoded, changes, encoders


def scale_features(df: pd.DataFrame, columns: list = None) -> tuple[pd.DataFrame, list[str]]:
    """Apply StandardScaler to numeric columns."""
    df_scaled = df.copy()
    changes = []

    if columns is None:
        columns = df_scaled.select_dtypes(include=np.number).columns.tolist()

    if not columns:
        changes.append("No numeric columns to scale")
        return df_scaled, changes

    scaler = StandardScaler()
    df_scaled[columns] = scaler.fit_transform(df_scaled[columns])
    changes.append(f"StandardScaler applied to {len(columns)} numeric columns")

    return df_scaled, changes


def handle_outliers_iqr(df: pd.DataFrame, columns: list = None, method: str = "clip") -> tuple[pd.DataFrame, list[str]]:
    """
    Handle outliers using IQR method.
    Methods: 'clip' (cap at bounds), 'remove' (remove outlier rows)
    """
    df_clean = df.copy()
    changes = []

    if columns is None:
        columns = df_clean.select_dtypes(include=np.number).columns.tolist()

    total_affected = 0
    for col in columns:
        data = df_clean[col].dropna()
        Q1 = data.quantile(0.25)
        Q3 = data.quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR

        outlier_mask = (df_clean[col] < lower) | (df_clean[col] > upper)
        outlier_count = outlier_mask.sum()

        if outlier_count > 0:
            if method == "clip":
                df_clean[col] = df_clean[col].clip(lower=lower, upper=upper)
                changes.append(f"Clipped {outlier_count} outliers in '{col}' to [{lower:.2f}, {upper:.2f}]")
            elif method == "remove":
                df_clean = df_clean[~outlier_mask]
                changes.append(f"Removed {outlier_count} outlier rows from '{col}'")
            total_affected += outlier_count

    if total_affected == 0:
        changes.append("No outliers detected — no changes needed")

    if method == "remove":
        df_clean = df_clean.reset_index(drop=True)

    return df_clean, changes


def select_features(df: pd.DataFrame, target_col: str = None, corr_threshold: float = 0.05,
                    variance_threshold: float = 0.01) -> tuple[pd.DataFrame, list[str], list[str]]:
    """
    Feature selection based on variance threshold and correlation with target.
    Returns: (selected DataFrame, changes, dropped columns)
    """
    df_selected = df.copy()
    changes = []
    dropped = []

    numeric_cols = df_selected.select_dtypes(include=np.number).columns.tolist()
    if not numeric_cols:
        changes.append("No numeric columns for feature selection")
        return df_selected, changes, dropped

    # Variance threshold
    try:
        selector = VarianceThreshold(threshold=variance_threshold)
        numeric_data = df_selected[numeric_cols].fillna(0)
        selector.fit(numeric_data)
        low_var_mask = ~selector.get_support()
        low_var_cols = [numeric_cols[i] for i in range(len(numeric_cols)) if low_var_mask[i]]

        # Don't drop target
        if target_col in low_var_cols:
            low_var_cols.remove(target_col)

        if low_var_cols:
            df_selected = df_selected.drop(columns=low_var_cols)
            dropped.extend(low_var_cols)
            changes.append(f"Removed {len(low_var_cols)} low-variance columns: {low_var_cols}")
    except Exception:
        pass

    # Correlation with target
    if target_col and target_col in df_selected.columns:
        remaining_numeric = df_selected.select_dtypes(include=np.number).columns.tolist()
        if target_col in remaining_numeric:
            remaining_numeric.remove(target_col)

        if remaining_numeric:
            try:
                correlations = df_selected[remaining_numeric].corrwith(df_selected[target_col].astype(float)).abs()
                low_corr_cols = correlations[correlations < corr_threshold].index.tolist()
                if low_corr_cols:
                    df_selected = df_selected.drop(columns=low_corr_cols)
                    dropped.extend(low_corr_cols)
                    changes.append(
                        f"Removed {len(low_corr_cols)} columns with low correlation to target: {low_corr_cols}"
                    )
            except Exception:
                pass

    if not changes:
        changes.append("All features retained — no low-quality features detected")

    return df_selected, changes, dropped
