"""
DAVL — Statistics Module
Comprehensive statistical summaries: mean, median, mode, std, variance, skewness, kurtosis,
correlation matrix, covariance matrix.
"""

import pandas as pd
import numpy as np
from scipy import stats as sp_stats


def descriptive_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """Compute comprehensive descriptive statistics for numeric columns."""
    numeric_df = df.select_dtypes(include=np.number)
    if numeric_df.empty:
        return pd.DataFrame()

    records = []
    for col in numeric_df.columns:
        data = numeric_df[col].dropna()
        if len(data) == 0:
            continue

        mode_val = data.mode()
        mode_str = str(round(mode_val.iloc[0], 4)) if not mode_val.empty else "N/A"

        records.append({
            "Column": col,
            "Count": len(data),
            "Mean": round(data.mean(), 4),
            "Median": round(data.median(), 4),
            "Mode": mode_str,
            "Std Dev": round(data.std(), 4),
            "Variance": round(data.var(), 4),
            "Min": round(data.min(), 4),
            "Max": round(data.max(), 4),
            "Range": round(data.max() - data.min(), 4),
            "IQR": round(data.quantile(0.75) - data.quantile(0.25), 4),
            "Skewness": round(data.skew(), 4),
            "Kurtosis": round(data.kurtosis(), 4),
            "Coeff of Variation": round(data.std() / data.mean() * 100, 2) if data.mean() != 0 else None,
        })

    return pd.DataFrame(records)


def correlation_matrix(df: pd.DataFrame, method: str = "pearson") -> pd.DataFrame:
    """Compute correlation matrix."""
    numeric_df = df.select_dtypes(include=np.number)
    if numeric_df.shape[1] < 2:
        return pd.DataFrame()
    return numeric_df.corr(method=method).round(4)


def covariance_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """Compute covariance matrix."""
    numeric_df = df.select_dtypes(include=np.number)
    if numeric_df.shape[1] < 2:
        return pd.DataFrame()
    return numeric_df.cov().round(4)


def normality_tests(df: pd.DataFrame) -> pd.DataFrame:
    """Perform normality tests on numeric columns."""
    numeric_df = df.select_dtypes(include=np.number)
    results = []

    for col in numeric_df.columns:
        data = numeric_df[col].dropna()
        if len(data) < 8:
            continue

        sample = data.sample(min(5000, len(data)), random_state=42)

        # Shapiro-Wilk
        try:
            sw_stat, sw_p = sp_stats.shapiro(sample)
        except Exception:
            sw_stat, sw_p = None, None

        # D'Agostino-Pearson
        try:
            dp_stat, dp_p = sp_stats.normaltest(sample)
        except Exception:
            dp_stat, dp_p = None, None

        is_normal = (sw_p is not None and sw_p > 0.05) or (dp_p is not None and dp_p > 0.05)

        results.append({
            "Column": col,
            "Shapiro-Wilk Stat": round(sw_stat, 4) if sw_stat else None,
            "Shapiro p-value": round(sw_p, 6) if sw_p else None,
            "D'Agostino Stat": round(dp_stat, 4) if dp_stat else None,
            "D'Agostino p-value": round(dp_p, 6) if dp_p else None,
            "Likely Normal": "Yes" if is_normal else "No",
        })

    return pd.DataFrame(results)


def feature_importance_by_correlation(df: pd.DataFrame, target_col: str) -> pd.DataFrame:
    """Rank features by absolute correlation with target."""
    numeric_df = df.select_dtypes(include=np.number)
    if target_col not in numeric_df.columns or numeric_df.shape[1] < 2:
        return pd.DataFrame()

    correlations = numeric_df.drop(columns=[target_col]).corrwith(numeric_df[target_col])
    result = pd.DataFrame({
        "Feature": correlations.index,
        "Correlation": correlations.values.round(4),
        "Abs Correlation": np.abs(correlations.values).round(4),
    }).sort_values("Abs Correlation", ascending=False).reset_index(drop=True)

    return result
