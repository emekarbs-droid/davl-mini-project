"""
DAVL — Exploratory Data Analysis Module
Univariate, bivariate, multivariate, correlation, and distribution analysis.
"""

import pandas as pd
import numpy as np
from scipy import stats


def univariate_numeric_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Compute univariate statistics for all numeric columns."""
    numeric_cols = df.select_dtypes(include=np.number).columns
    if len(numeric_cols) == 0:
        return pd.DataFrame()

    records = []
    for col in numeric_cols:
        data = df[col].dropna()
        if len(data) == 0:
            continue
        records.append({
            "Column": col,
            "Count": len(data),
            "Mean": round(data.mean(), 4),
            "Median": round(data.median(), 4),
            "Std Dev": round(data.std(), 4),
            "Min": round(data.min(), 4),
            "25%": round(data.quantile(0.25), 4),
            "50%": round(data.quantile(0.50), 4),
            "75%": round(data.quantile(0.75), 4),
            "Max": round(data.max(), 4),
            "Skewness": round(data.skew(), 4),
            "Kurtosis": round(data.kurtosis(), 4),
        })
    return pd.DataFrame(records)


def univariate_categorical_summary(df: pd.DataFrame) -> dict:
    """Compute value counts for all categorical columns."""
    cat_cols = df.select_dtypes(include=["object", "category"]).columns
    summaries = {}
    for col in cat_cols:
        vc = df[col].value_counts()
        summaries[col] = {
            "value_counts": vc,
            "num_unique": df[col].nunique(),
            "top_value": vc.index[0] if len(vc) > 0 else None,
            "top_frequency": vc.iloc[0] if len(vc) > 0 else 0,
            "missing": df[col].isnull().sum(),
        }
    return summaries


def correlation_analysis(df: pd.DataFrame, method: str = "pearson") -> pd.DataFrame:
    """Compute correlation matrix for numeric columns."""
    numeric_df = df.select_dtypes(include=np.number)
    if numeric_df.shape[1] < 2:
        return pd.DataFrame()
    return numeric_df.corr(method=method).round(4)


def highly_correlated_pairs(df: pd.DataFrame, threshold: float = 0.8) -> pd.DataFrame:
    """Find pairs of features with high absolute correlation."""
    corr = correlation_analysis(df)
    if corr.empty:
        return pd.DataFrame()

    pairs = []
    cols = corr.columns
    for i in range(len(cols)):
        for j in range(i + 1, len(cols)):
            val = corr.iloc[i, j]
            if abs(val) >= threshold:
                pairs.append({
                    "Feature 1": cols[i],
                    "Feature 2": cols[j],
                    "Correlation": round(val, 4),
                    "Abs Correlation": round(abs(val), 4),
                })

    result = pd.DataFrame(pairs)
    if not result.empty:
        result = result.sort_values("Abs Correlation", ascending=False).reset_index(drop=True)
    return result


def distribution_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """Analyze distributions of numeric columns (normality test, skewness)."""
    numeric_cols = df.select_dtypes(include=np.number).columns
    results = []

    for col in numeric_cols:
        data = df[col].dropna()
        if len(data) < 8:
            continue

        skew = data.skew()
        kurt = data.kurtosis()

        # Shapiro-Wilk test (sample if too large)
        sample = data.sample(min(5000, len(data)), random_state=42)
        try:
            stat, p_value = stats.shapiro(sample)
        except Exception:
            stat, p_value = None, None

        # Determine distribution type
        if p_value is not None and p_value > 0.05:
            dist_type = "Normal"
        elif abs(skew) > 1:
            dist_type = "Highly Skewed"
        elif abs(skew) > 0.5:
            dist_type = "Moderately Skewed"
        else:
            dist_type = "Approximately Symmetric"

        results.append({
            "Column": col,
            "Skewness": round(skew, 4),
            "Kurtosis": round(kurt, 4),
            "Shapiro Stat": round(stat, 4) if stat else None,
            "Shapiro p-value": round(p_value, 6) if p_value else None,
            "Distribution": dist_type,
            "Skew Direction": "Right" if skew > 0.5 else ("Left" if skew < -0.5 else "Symmetric"),
        })

    return pd.DataFrame(results)


def bivariate_analysis(df: pd.DataFrame, target_col: str = None) -> dict:
    """Generate bivariate analysis results."""
    results = {}

    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()

    # Numeric-Numeric correlations
    if len(numeric_cols) >= 2:
        results["numeric_correlations"] = correlation_analysis(df)

    # If target exists: numeric features vs target
    if target_col and target_col in df.columns:
        if target_col in cat_cols:
            # Group numeric features by target category
            group_stats = {}
            for col in numeric_cols:
                try:
                    group_stats[col] = df.groupby(target_col)[col].agg(
                        ["mean", "median", "std"]
                    ).round(4)
                except Exception:
                    pass
            results["numeric_by_target"] = group_stats
        elif target_col in numeric_cols:
            # Correlation with target
            other_numeric = [c for c in numeric_cols if c != target_col]
            if other_numeric:
                corr_with_target = df[other_numeric].corrwith(df[target_col]).round(4)
                results["correlation_with_target"] = corr_with_target.sort_values(
                    key=abs, ascending=False
                )

    return results
