"""
DAVL — PCA Analysis Module
Standardize data, compute PCA, explained variance, scree plot, scatter plots, loadings.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA


def run_pca(df: pd.DataFrame, target_col: str = None, n_components: int = None) -> dict:
    """
    Run complete PCA analysis on numeric columns.
    Returns a dict with all PCA results.
    """
    numeric_df = df.select_dtypes(include=np.number)

    # Remove target column from features if present
    if target_col and target_col in numeric_df.columns:
        feature_df = numeric_df.drop(columns=[target_col])
        labels = df[target_col].values if target_col in df.columns else None
    else:
        feature_df = numeric_df
        labels = None

    # Drop columns with all NaN
    feature_df = feature_df.dropna(axis=1, how="all")
    # Fill remaining NaN with column medians
    feature_df = feature_df.fillna(feature_df.median())

    if feature_df.shape[1] < 2:
        return {"error": "Need at least 2 numeric features for PCA"}

    # Standardize
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(feature_df)

    # PCA
    max_components = min(feature_df.shape[0], feature_df.shape[1])
    if n_components is None:
        n_components = max_components

    n_components = min(n_components, max_components)
    pca = PCA(n_components=n_components)
    transformed = pca.fit_transform(scaled_data)

    # Explained variance
    explained_var = pca.explained_variance_ratio_
    cumulative_var = np.cumsum(explained_var)

    # Component loadings
    loadings = pd.DataFrame(
        pca.components_.T,
        index=feature_df.columns,
        columns=[f"PC{i+1}" for i in range(n_components)],
    )

    # Optimal components (>= 95% variance)
    optimal_n = np.argmax(cumulative_var >= 0.95) + 1 if np.any(cumulative_var >= 0.95) else n_components

    # Variance table
    var_table = pd.DataFrame({
        "Component": [f"PC{i+1}" for i in range(n_components)],
        "Eigenvalue": pca.explained_variance_.round(4),
        "Variance Ratio": (explained_var * 100).round(2),
        "Cumulative %": (cumulative_var * 100).round(2),
    })

    return {
        "transformed": transformed,
        "explained_variance": explained_var,
        "cumulative_variance": cumulative_var,
        "loadings": loadings,
        "variance_table": var_table,
        "n_components": n_components,
        "optimal_components": optimal_n,
        "labels": labels,
        "feature_names": feature_df.columns.tolist(),
        "pca_object": pca,
    }
