"""
lda_analysis.py — sklearn LDA: class separation, explained variance.
"""
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.preprocessing import StandardScaler, LabelEncoder


def show_lda(df, name="Dataset"):
    """Run LDA on numeric columns with a categorical target."""
    st.subheader(f"🎯 LDA — {name}")

    num_cols = df.select_dtypes(include="number").columns.tolist()
    cat_cols = df.select_dtypes(include="object").columns.tolist()

    if len(num_cols) < 2:
        st.info("Need at least 2 numeric columns for LDA.")
        return
    if not cat_cols:
        st.info("Need at least one categorical column as target.")
        return

    target = st.selectbox("Target column", cat_cols,
                          key=f"lda_target_col_{name}")

    # Filter to top classes
    top_classes = df[target].value_counts().head(10).index
    subset = df[df[target].isin(top_classes)].dropna(subset=num_cols + [target])

    if len(subset) < 10:
        st.warning("Not enough data after filtering.")
        return

    X = subset[num_cols].values
    le = LabelEncoder()
    y = le.fit_transform(subset[target])
    n_classes = len(np.unique(y))

    if n_classes < 2:
        st.warning("Need at least 2 classes.")
        return

    n_components = min(n_classes - 1, len(num_cols), 2)
    if n_components < 1:
        st.warning("Cannot compute LDA with these parameters.")
        return

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    try:
        lda = LinearDiscriminantAnalysis(n_components=n_components)
        X_lda = lda.fit_transform(X_scaled, y)
    except Exception as e:
        st.error(f"LDA failed: {e}")
        return

    # Explained variance
    if hasattr(lda, "explained_variance_ratio_"):
        st.markdown("**Explained Variance Ratio**")
        var_df = pd.DataFrame({
            "Component": [f"LD{i+1}" for i in range(n_components)],
            "Variance %": (lda.explained_variance_ratio_ * 100).round(2),
        })
        st.dataframe(var_df, use_container_width=True, hide_index=True)

    # Scatter / histogram
    if n_components >= 2:
        scatter_df = pd.DataFrame({
            "LD1": X_lda[:, 0],
            "LD2": X_lda[:, 1],
            target: subset[target].values,
        })
        fig = px.scatter(scatter_df, x="LD1", y="LD2", color=target,
                         title="LDA Projection", opacity=0.5)
        st.plotly_chart(fig, use_container_width=True)
    elif n_components == 1:
        scatter_df = pd.DataFrame({
            "LD1": X_lda[:, 0],
            target: subset[target].values,
        })
        fig = px.histogram(scatter_df, x="LD1", color=target,
                           title="LDA Projection (1D)", barmode="overlay",
                           opacity=0.7)
        st.plotly_chart(fig, use_container_width=True)

    # Coefficients
    with st.expander("LDA Coefficients"):
        coef_df = pd.DataFrame(
            lda.scalings_[:, :n_components],
            index=num_cols,
            columns=[f"LD{i+1}" for i in range(n_components)],
        ).round(4)
        st.dataframe(coef_df, use_container_width=True)
