"""
insights.py
-----------
Automatically generate analyst insights:
 - Important features (by variance & correlation with target)
 - Highly correlated variable pairs
 - Redundant / constant columns
 - Data quality issues
 - Suggested preprocessing steps
 - Key observations
"""

import pandas as pd
import numpy as np
import streamlit as st
from scipy import stats as scipy_stats


def show_insights(df: pd.DataFrame, target: str = None,
                  quality_summary: dict = None):
    """Generate and display all analyst insights."""
    st.subheader("💡 Analyst Insights & Recommendations")

    numeric_df = df.select_dtypes(include=np.number)
    feature_cols = [c for c in numeric_df.columns if c != target]

    insights = []
    warnings = []
    suggestions = []

    _data_quality_insights(df, quality_summary, insights, warnings, suggestions)
    _correlation_insights(numeric_df, feature_cols, target, insights, suggestions)
    _feature_importance_insights(df, numeric_df, feature_cols, target, insights)
    _distribution_insights(numeric_df, feature_cols, insights, suggestions)
    _cardinality_insights(df, insights, suggestions)

    # ── Display sections ──────────────────────────────────────────────────────
    _render_section("🔍 Key Observations", insights, "info")
    _render_section("⚠️ Data Warnings", warnings, "warning")
    _render_section("🛠️ Suggested Preprocessing", suggestions, "success")

    # ── Feature Importance (variance-based) ──────────────────────────────────
    _show_feature_importance(df, numeric_df, feature_cols, target)

    # ── Correlation summary ───────────────────────────────────────────────────
    _show_correlation_summary(numeric_df)

    # ── Full report download ──────────────────────────────────────────────────
    _download_report(df, insights, warnings, suggestions, target, quality_summary)


def _data_quality_insights(df, quality_summary, insights, warnings, suggestions):
    qs = quality_summary or {}

    total_missing = qs.get("total_missing", df.isnull().sum().sum())
    missing_pct = qs.get("missing_pct", total_missing / df.size * 100)
    dup_rows = qs.get("duplicate_rows", df.duplicated().sum())
    const_cols = qs.get("constant_cols", [c for c in df.columns if df[c].nunique() <= 1])
    outlier_cols = qs.get("outlier_cols", [])

    if total_missing == 0:
        insights.append("✅ Dataset has **no missing values** — excellent data completeness.")
    elif missing_pct < 5:
        warnings.append(f"🕳️ {total_missing:,} missing cells ({missing_pct:.1f}%) detected — low impact.")
        suggestions.append("Use median/mode imputation for columns with < 5% missing.")
    elif missing_pct < 20:
        warnings.append(f"🕳️ {total_missing:,} missing cells ({missing_pct:.1f}%) — moderate impact.")
        suggestions.append("Apply iterative imputation or KNN imputer for columns with 5–20% missing.")
    else:
        warnings.append(f"🔴 {total_missing:,} missing cells ({missing_pct:.1f}%) — high impact on model quality.")
        suggestions.append("Consider dropping columns with > 50% missing; use advanced imputation for rest.")

    if dup_rows > 0:
        warnings.append(f"🔄 {dup_rows:,} duplicate rows detected ({dup_rows/len(df)*100:.1f}% of data).")
        suggestions.append("Remove duplicate rows before training any model.")

    if const_cols:
        warnings.append(f"📌 Constant columns (zero variance): **{const_cols}** — provide no information.")
        suggestions.append(f"Drop constant columns: {const_cols}")

    if outlier_cols:
        warnings.append(f"📊 Columns with >5% IQR outliers: **{outlier_cols}**")
        suggestions.append("Cap outliers using IQR or Winsorization; or use robust scalers (RobustScaler).")

    insights.append(f"📐 Dataset shape: **{df.shape[0]:,} rows × {df.shape[1]} columns**.")
    insights.append(f"🗂️ Numeric columns: **{len(df.select_dtypes(include=np.number).columns)}** | "
                    f"Categorical: **{len(df.select_dtypes(include=['object', 'category']).columns)}**")


def _correlation_insights(numeric_df, feature_cols, target, insights, suggestions):
    if len(feature_cols) < 2:
        return

    corr = numeric_df[feature_cols].corr().abs()
    high_pairs = []
    for i in range(len(feature_cols)):
        for j in range(i + 1, len(feature_cols)):
            val = corr.iloc[i, j]
            if val >= 0.8:
                high_pairs.append((feature_cols[i], feature_cols[j], round(float(val), 4)))

    if high_pairs:
        insights.append(f"🔗 **{len(high_pairs)} highly correlated feature pair(s)** (|r| ≥ 0.8) found:")
        for f1, f2, r in high_pairs[:5]:
            insights.append(f"   • `{f1}` ↔ `{f2}` (r = {r})")
        if len(high_pairs) > 5:
            insights.append(f"   • ...and {len(high_pairs) - 5} more pairs.")
        suggestions.append("Consider dropping one column from each highly correlated pair to reduce multicollinearity.")
    else:
        insights.append("🔗 No feature pairs with |r| ≥ 0.8 — **low multicollinearity**.")

    if target and target in numeric_df.columns:
        target_corr = numeric_df.corr()[target].drop(target).abs().sort_values(ascending=False)
        top3 = target_corr.head(3)
        if len(top3) > 0:
            insights.append(f"🎯 Top features correlated with **`{target}`**:")
            for feat, r in top3.items():
                insights.append(f"   • `{feat}` (|r| = {r:.4f})")


def _feature_importance_insights(df, numeric_df, feature_cols, target, insights):
    if not feature_cols:
        return

    variances = numeric_df[feature_cols].var().sort_values(ascending=False)
    top_var = variances.head(3).index.tolist()
    insights.append(f"📊 Highest variance features (most informative): **{top_var}**")

    low_var = variances[variances < 0.01].index.tolist()
    if low_var:
        insights.append(f"📉 Near-zero variance features (potentially redundant): **{low_var}**")


def _distribution_insights(numeric_df, feature_cols, insights, suggestions):
    if not feature_cols:
        return

    skewness = numeric_df[feature_cols].skew()
    high_skew = skewness[skewness.abs() > 1].index.tolist()
    if high_skew:
        insights.append(f"📈 Highly skewed features (|skew| > 1): **{high_skew}**")
        suggestions.append(f"Apply log, sqrt, or Box-Cox transform to: {high_skew}")
    else:
        insights.append("📈 No severely skewed features detected — distributions are approximately normal.")


def _cardinality_insights(df, insights, suggestions):
    cat_cols = df.select_dtypes(include=["object", "category"]).columns
    for col in cat_cols:
        n = df[col].nunique()
        if n > 100:
            insights.append(f"🔢 `{col}` has **{n} unique values** — very high cardinality.")
            suggestions.append(f"Use target encoding or embeddings for `{col}` instead of one-hot encoding.")
        elif n == 1:
            insights.append(f"📌 `{col}` has only **1 unique value** — constant categorical, drop it.")


def _render_section(title: str, items: list, style: str = "info"):
    st.markdown(f"#### {title}")
    if not items:
        st.success("Nothing to report.")
        return
    fn = {"info": st.info, "warning": st.warning, "success": st.success}.get(style, st.info)
    for item in items:
        fn(item)


def _show_feature_importance(df, numeric_df, feature_cols, target):
    st.markdown("#### 🏆 Feature Importance (Variance-Based Ranking)")
    if not feature_cols:
        return

    var_series = numeric_df[feature_cols].var().sort_values(ascending=False)
    fi_df = pd.DataFrame({
        "Feature": var_series.index,
        "Variance": var_series.values.round(4),
        "Std Dev": numeric_df[feature_cols].std()[var_series.index].values.round(4),
    })

    if target and target in numeric_df.columns:
        corr_with_target = numeric_df.corr()[target].drop(target, errors="ignore")
        fi_df["Correlation with Target"] = fi_df["Feature"].map(
            lambda f: round(float(abs(corr_with_target.get(f, np.nan))), 4)
        )

    import plotly.express as px
    fig = px.bar(fi_df, x="Variance", y="Feature", orientation="h",
                 color="Variance", color_continuous_scale="Viridis",
                 template="plotly_dark", title="Feature Variance Ranking")
    fig.update_layout(height=max(400, len(feature_cols) * 28), yaxis_categoryorder="total ascending")
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(fi_df, use_container_width=True)


def _show_correlation_summary(numeric_df):
    st.markdown("#### 🔗 Top Correlated Feature Pairs")
    if len(numeric_df.columns) < 2:
        return
    corr = numeric_df.corr().abs()
    pairs = []
    cols = corr.columns.tolist()
    for i in range(len(cols)):
        for j in range(i + 1, len(cols)):
            pairs.append({"Feature A": cols[i], "Feature B": cols[j],
                          "Correlation": round(float(corr.iloc[i, j]), 4)})
    pairs_df = pd.DataFrame(pairs).sort_values("Correlation", ascending=False).head(20)
    st.dataframe(pairs_df.reset_index(drop=True), use_container_width=True)


def _download_report(df, insights, warnings, suggestions, target, quality_summary):
    st.markdown("---")
    st.markdown("#### 📥 Download Analysis Report")

    qs = quality_summary or {}
    lines = [
        "# Data Analysis Report",
        f"\nGenerated by DAVL — Data Analysis & Visualization Lab",
        f"\n## Dataset Summary",
        f"- Rows: {df.shape[0]:,}",
        f"- Columns: {df.shape[1]}",
        f"- Target Column: {target or 'Not detected'}",
        f"- Total Missing: {qs.get('total_missing', df.isnull().sum().sum()):,}",
        f"- Duplicate Rows: {qs.get('duplicate_rows', df.duplicated().sum()):,}",
        "\n## Key Observations",
    ]
    for obs in insights:
        lines.append(f"- {obs}")
    lines.append("\n## Data Warnings")
    for w in warnings:
        lines.append(f"- {w}")
    lines.append("\n## Suggested Preprocessing")
    for s in suggestions:
        lines.append(f"- {s}")
    lines.append("\n## Descriptive Statistics")
    lines.append(df.describe().to_string())

    report_text = "\n".join(lines)
    st.download_button(
        "⬇️ Download Report (.txt)",
        data=report_text.encode("utf-8"),
        file_name="analysis_report.txt",
        mime="text/plain",
    )
