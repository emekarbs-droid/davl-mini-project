"""
DAVL — Data Quality Analysis Module
Missing values, duplicates, outliers, constant columns, class imbalance.
"""

import pandas as pd
import numpy as np


def missing_value_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """Compute missing value counts and percentages per column."""
    missing_count = df.isnull().sum()
    missing_pct = (df.isnull().mean() * 100).round(2)
    result = pd.DataFrame({
        "Column": df.columns,
        "Missing Count": missing_count.values,
        "Missing %": missing_pct.values,
        "Present Count": (df.shape[0] - missing_count).values,
        "Data Type": df.dtypes.values.astype(str),
    })
    result = result.sort_values("Missing Count", ascending=False).reset_index(drop=True)
    return result


def duplicate_analysis(df: pd.DataFrame) -> dict:
    """Detect and summarize duplicate rows."""
    dup_count = df.duplicated().sum()
    dup_pct = round((dup_count / len(df)) * 100, 2) if len(df) > 0 else 0
    return {
        "duplicate_count": dup_count,
        "duplicate_percentage": dup_pct,
        "total_rows": len(df),
        "unique_rows": len(df) - dup_count,
        "duplicate_rows": df[df.duplicated(keep=False)] if dup_count > 0 else pd.DataFrame(),
    }


def constant_columns(df: pd.DataFrame) -> list:
    """Find columns with zero variance (only one unique value)."""
    return [col for col in df.columns if df[col].nunique() <= 1]


def high_cardinality_columns(df: pd.DataFrame, threshold: int = 50) -> list:
    """Find categorical columns with high cardinality."""
    cat_cols = df.select_dtypes(include=["object", "category"]).columns
    return [col for col in cat_cols if df[col].nunique() > threshold]


def detect_outliers_iqr(df: pd.DataFrame) -> pd.DataFrame:
    """Detect outliers using the IQR method for numeric columns."""
    numeric_cols = df.select_dtypes(include=np.number).columns
    outlier_info = []

    for col in numeric_cols:
        data = df[col].dropna()
        if len(data) == 0:
            continue

        Q1 = data.quantile(0.25)
        Q3 = data.quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        outlier_count = ((data < lower_bound) | (data > upper_bound)).sum()
        outlier_pct = round((outlier_count / len(data)) * 100, 2)

        outlier_info.append({
            "Column": col,
            "Q1": round(Q1, 4),
            "Q3": round(Q3, 4),
            "IQR": round(IQR, 4),
            "Lower Bound": round(lower_bound, 4),
            "Upper Bound": round(upper_bound, 4),
            "Outlier Count": outlier_count,
            "Outlier %": outlier_pct,
        })

    return pd.DataFrame(outlier_info)


def class_imbalance_check(df: pd.DataFrame, target_col: str) -> dict | None:
    """Check for class imbalance in the target column."""
    if target_col is None or target_col not in df.columns:
        return None

    value_counts = df[target_col].value_counts()
    total = len(df[target_col].dropna())

    if total == 0:
        return None

    proportions = (value_counts / total * 100).round(2)
    min_class_pct = proportions.min()
    max_class_pct = proportions.max()
    imbalance_ratio = round(max_class_pct / min_class_pct, 2) if min_class_pct > 0 else float("inf")

    is_imbalanced = imbalance_ratio > 3  # Ratio > 3:1 considered imbalanced

    return {
        "target_column": target_col,
        "class_distribution": value_counts.to_dict(),
        "class_percentages": proportions.to_dict(),
        "num_classes": len(value_counts),
        "min_class_percentage": min_class_pct,
        "max_class_percentage": max_class_pct,
        "imbalance_ratio": imbalance_ratio,
        "is_imbalanced": is_imbalanced,
    }


def data_quality_summary(df: pd.DataFrame, target_col: str = None) -> dict:
    """Generate a comprehensive data quality summary."""
    missing = missing_value_analysis(df)
    duplicates = duplicate_analysis(df)
    constants = constant_columns(df)
    high_card = high_cardinality_columns(df)
    outliers = detect_outliers_iqr(df)
    imbalance = class_imbalance_check(df, target_col)

    total_issues = 0
    total_issues += (missing["Missing Count"] > 0).sum()
    total_issues += duplicates["duplicate_count"]
    total_issues += len(constants)
    total_issues += len(high_card)
    total_issues += (outliers["Outlier Count"] > 0).sum() if not outliers.empty else 0

    return {
        "missing_values": missing,
        "duplicates": duplicates,
        "constant_columns": constants,
        "high_cardinality": high_card,
        "outliers": outliers,
        "class_imbalance": imbalance,
        "total_issues": total_issues,
    }
