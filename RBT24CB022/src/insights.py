"""
DAVL — Insights Module
Automatically generates data analyst insights and recommendations.
"""

import pandas as pd
import numpy as np
from src.eda import correlation_analysis, highly_correlated_pairs, distribution_analysis
from src.data_quality import data_quality_summary


def generate_insights(df: pd.DataFrame, target_col: str = None) -> dict:
    """
    Generate comprehensive analyst insights from the dataset.
    Returns a dict of categorized insights.
    """
    insights = {
        "data_quality": [],
        "important_features": [],
        "correlations": [],
        "redundant_columns": [],
        "preprocessing_suggestions": [],
        "key_observations": [],
    }

    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
    n_rows, n_cols = df.shape

    # ---------- Data Quality Insights ----------
    missing_total = df.isnull().sum().sum()
    missing_cols = df.columns[df.isnull().any()].tolist()
    if missing_total > 0:
        pct = round(missing_total / (n_rows * n_cols) * 100, 2)
        insights["data_quality"].append(
            f"⚠️ Dataset has **{missing_total}** missing values ({pct}% of all cells) across **{len(missing_cols)}** columns."
        )
        # Columns with >50% missing
        high_missing = [col for col in missing_cols if df[col].isnull().mean() > 0.5]
        if high_missing:
            insights["data_quality"].append(
                f"🔴 Columns with >50% missing: **{', '.join(high_missing)}** — consider dropping."
            )
    else:
        insights["data_quality"].append("✅ No missing values detected — dataset is complete.")

    dup_count = df.duplicated().sum()
    if dup_count > 0:
        insights["data_quality"].append(
            f"⚠️ **{dup_count}** duplicate rows found ({round(dup_count/n_rows*100, 2)}% of data)."
        )
    else:
        insights["data_quality"].append("✅ No duplicate rows.")

    # Constant columns
    const_cols = [col for col in df.columns if df[col].nunique() <= 1]
    if const_cols:
        insights["data_quality"].append(
            f"🔴 Constant columns (zero information): **{', '.join(const_cols)}** — remove them."
        )

    # High cardinality
    high_card = [col for col in cat_cols if df[col].nunique() > 50]
    if high_card:
        insights["data_quality"].append(
            f"⚠️ High cardinality columns: **{', '.join(high_card)}** — may need special encoding."
        )

    # ---------- Important Features (by correlation to target) ----------
    if target_col and target_col in df.columns and target_col in numeric_cols:
        other_numeric = [c for c in numeric_cols if c != target_col]
        if other_numeric:
            corrs = df[other_numeric].corrwith(df[target_col]).abs().sort_values(ascending=False)
            top_features = corrs.head(5)
            for feat, val in top_features.items():
                strength = "strong" if val > 0.7 else ("moderate" if val > 0.4 else "weak")
                insights["important_features"].append(
                    f"📊 **{feat}** has {strength} correlation ({val:.3f}) with target '{target_col}'."
                )
    elif target_col and target_col in cat_cols:
        insights["important_features"].append(
            f"📌 Target '{target_col}' is categorical with **{df[target_col].nunique()}** classes."
        )
        value_pcts = df[target_col].value_counts(normalize=True) * 100
        if value_pcts.max() > 70:
            insights["important_features"].append(
                f"⚠️ Class imbalance detected — dominant class is **{value_pcts.idxmax()}** ({value_pcts.max():.1f}%)."
            )

    # ---------- Correlation Insights ----------
    high_corr = highly_correlated_pairs(df, threshold=0.8)
    if not high_corr.empty:
        for _, row in high_corr.iterrows():
            insights["correlations"].append(
                f"🔗 **{row['Feature 1']}** and **{row['Feature 2']}** are highly correlated (r={row['Correlation']:.3f})."
            )

        # Redundant columns
        redundant = set()
        for _, row in high_corr.iterrows():
            redundant.add(row["Feature 2"])  # Keep Feature 1, mark Feature 2 as redundant
        insights["redundant_columns"].append(
            f"🗑️ Potentially redundant columns: **{', '.join(redundant)}** — consider removing to reduce multicollinearity."
        )
    else:
        insights["correlations"].append("✅ No highly correlated feature pairs (|r| > 0.8) found.")

    # ---------- Preprocessing Suggestions ----------
    if missing_total > 0:
        insights["preprocessing_suggestions"].append(
            "🔧 Handle missing values: use median imputation for numeric, mode for categorical."
        )
    if dup_count > 0:
        insights["preprocessing_suggestions"].append("🔧 Remove duplicate rows before analysis.")
    if const_cols:
        insights["preprocessing_suggestions"].append(
            f"🔧 Remove constant columns: {', '.join(const_cols)}"
        )

    # Check for skewed distributions
    dist = distribution_analysis(df)
    if not dist.empty:
        highly_skewed = dist[dist["Distribution"] == "Highly Skewed"]["Column"].tolist()
        if highly_skewed:
            insights["preprocessing_suggestions"].append(
                f"🔧 Highly skewed columns: **{', '.join(highly_skewed[:5])}** — consider log/sqrt transformation."
            )

    # Outlier suggestion
    for col in numeric_cols:
        data = df[col].dropna()
        if len(data) == 0:
            continue
        Q1, Q3 = data.quantile(0.25), data.quantile(0.75)
        IQR = Q3 - Q1
        outlier_pct = ((data < Q1 - 1.5 * IQR) | (data > Q3 + 1.5 * IQR)).mean() * 100
        if outlier_pct > 5:
            insights["preprocessing_suggestions"].append(
                f"🔧 **{col}** has {outlier_pct:.1f}% outliers — consider IQR clipping."
            )

    if cat_cols:
        insights["preprocessing_suggestions"].append(
            f"🔧 Encode {len(cat_cols)} categorical columns before modeling."
        )

    # Scaling suggestion
    if len(numeric_cols) >= 2:
        ranges = df[numeric_cols].max() - df[numeric_cols].min()
        if ranges.max() / (ranges.min() + 1e-10) > 100:
            insights["preprocessing_suggestions"].append(
                "🔧 Feature scales vary significantly — apply StandardScaler normalization."
            )

    # ---------- Key Observations ----------
    insights["key_observations"].append(f"📋 Dataset has **{n_rows:,}** rows and **{n_cols}** columns.")
    insights["key_observations"].append(
        f"📋 Column types: **{len(numeric_cols)}** numeric, **{len(cat_cols)}** categorical."
    )

    if len(numeric_cols) >= 2:
        corr_matrix = correlation_analysis(df)
        if not corr_matrix.empty:
            avg_corr = corr_matrix.values[np.triu_indices_from(corr_matrix.values, k=1)].mean()
            insights["key_observations"].append(
                f"📋 Average inter-feature correlation: **{avg_corr:.3f}**."
            )

    if target_col:
        insights["key_observations"].append(f"🎯 Detected target column: **{target_col}**")

    # Dataset size recommendation
    if n_rows < 100:
        insights["key_observations"].append(
            "⚠️ Small dataset (<100 rows) — results may not be statistically robust."
        )
    elif n_rows > 100000:
        insights["key_observations"].append(
            "💡 Large dataset (>100K rows) — sampling may be used for some visualizations."
        )

    return insights


def format_insights_markdown(insights: dict) -> str:
    """Format insights as a markdown string for export."""
    sections = {
        "data_quality": "## 🔍 Data Quality Issues",
        "important_features": "## ⭐ Important Features",
        "correlations": "## 🔗 Correlation Insights",
        "redundant_columns": "## 🗑️ Redundant Columns",
        "preprocessing_suggestions": "## 🔧 Preprocessing Suggestions",
        "key_observations": "## 📋 Key Observations",
    }

    md = "# DAVL — Analyst Insights Report\n\n"
    for key, title in sections.items():
        items = insights.get(key, [])
        if items:
            md += f"{title}\n\n"
            for item in items:
                md += f"- {item}\n"
            md += "\n"

    return md
