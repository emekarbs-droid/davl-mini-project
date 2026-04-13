"""
DAVL — LDA Analysis Module
Linear Discriminant Analysis: projection, class separation, components.
Only applicable when a categorical target variable exists.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis


def can_apply_lda(df: pd.DataFrame, target_col: str) -> tuple[bool, str]:
    """Check if LDA can be applied."""
    if target_col is None:
        return False, "No target column detected — LDA requires a categorical target variable."

    if target_col not in df.columns:
        return False, f"Target column '{target_col}' not found in dataset."

    n_classes = df[target_col].nunique()
    if n_classes < 2:
        return False, f"Target has only {n_classes} class — LDA requires at least 2 classes."

    if n_classes > 200:
        return False, f"Target has {n_classes} classes — too many for LDA visualization (max 200)."

    numeric_cols = df.select_dtypes(include=np.number).columns
    feature_cols = [c for c in numeric_cols if c != target_col]
    if len(feature_cols) < 1:
        return False, "No numeric features available for LDA."

    return True, "LDA can be applied."


def run_lda(df: pd.DataFrame, target_col: str) -> dict:
    """
    Run LDA analysis.
    Returns dict with projection, components, and class separation info.
    """
    can_run, message = can_apply_lda(df, target_col)
    if not can_run:
        return {"error": message}

    # Prepare features and target
    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    feature_cols = [c for c in numeric_cols if c != target_col]

    feature_df = df[feature_cols].fillna(df[feature_cols].median())
    target = df[target_col].copy()

    # Encode target if needed
    le = LabelEncoder()
    target_encoded = le.fit_transform(target.astype(str))
    class_names = le.classes_

    n_classes = len(class_names)
    n_components = min(n_classes - 1, len(feature_cols))

    if n_components < 1:
        return {"error": "Cannot compute LDA — insufficient components."}

    # Standardize features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(feature_df)

    # Fit LDA
    lda = LinearDiscriminantAnalysis(n_components=n_components)
    try:
        X_lda = lda.fit_transform(X_scaled, target_encoded)
    except Exception as e:
        return {"error": f"LDA failed: {str(e)}"}

    # Explained variance ratio
    explained_var_ratio = lda.explained_variance_ratio_

    # Class means in LDA space
    class_means = {}
    for i, cls in enumerate(class_names):
        mask = target_encoded == i
        if mask.any():
            class_means[cls] = X_lda[mask].mean(axis=0).round(4).tolist()

    # LDA weights/coefficients
    coef_df = pd.DataFrame(
        lda.scalings_[:, :n_components],
        index=feature_cols,
        columns=[f"LD{i+1}" for i in range(n_components)],
    ).round(4)

    return {
        "transformed": X_lda,
        "labels": target.values,
        "class_names": class_names.tolist(),
        "n_components": n_components,
        "explained_variance_ratio": explained_var_ratio,
        "class_means": class_means,
        "coefficients": coef_df,
        "feature_names": feature_cols,
    }
