"""
pca_analysis.py — sklearn PCA: scree plot, scatter, loadings.
"""
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


def show_pca(df, name="Dataset"):
    """Run PCA on numeric columns and display results."""
    st.subheader(f"🔬 PCA — {name}")

    num = df.select_dtypes(include="number").dropna()
    if len(num.columns) < 2:
        st.info("Need at least 2 numeric columns for PCA.")
        return
    if len(num) < 3:
        st.warning("Not enough rows for PCA.")
        return

    # Standardize
    scaler = StandardScaler()
    scaled = scaler.fit_transform(num)

    n_components = min(len(num.columns), len(num), 10)
    pca = PCA(n_components=n_components)
    components = pca.fit_transform(scaled)

    # Explained variance
    st.markdown("**Explained Variance Ratio**")
    var_df = pd.DataFrame({
        "Component": [f"PC{i+1}" for i in range(n_components)],
        "Explained Variance %": (pca.explained_variance_ratio_ * 100).round(2),
        "Cumulative %": (np.cumsum(pca.explained_variance_ratio_) * 100).round(2),
    })
    st.dataframe(var_df, use_container_width=True, hide_index=True)

    # Scree plot
    fig = go.Figure()
    fig.add_trace(go.Bar(x=var_df["Component"],
                         y=var_df["Explained Variance %"],
                         name="Individual"))
    fig.add_trace(go.Scatter(x=var_df["Component"],
                             y=var_df["Cumulative %"],
                             name="Cumulative", mode="lines+markers"))
    fig.update_layout(title="Scree Plot", yaxis_title="%", height=400)
    st.plotly_chart(fig, use_container_width=True)

    # PC1 vs PC2 scatter
    if n_components >= 2:
        st.markdown("**PC1 vs PC2 Scatter**")
        cat_cols = df.select_dtypes(include="object").columns.tolist()
        color_col = st.selectbox("Color by", ["None"] + cat_cols,
                                 key=f"pca_scatter_color_{name}")

        scatter_df = pd.DataFrame({"PC1": components[:, 0], "PC2": components[:, 1]})
        if color_col != "None" and color_col in df.columns:
            # Align index
            scatter_df[color_col] = df[color_col].iloc[num.index].values
            fig = px.scatter(scatter_df, x="PC1", y="PC2", color=color_col,
                             title="PCA Scatter", opacity=0.5)
        else:
            fig = px.scatter(scatter_df, x="PC1", y="PC2",
                             title="PCA Scatter", opacity=0.5)
        st.plotly_chart(fig, use_container_width=True)

    # Loadings
    with st.expander("PCA Loadings"):
        loadings = pd.DataFrame(
            pca.components_.T,
            columns=[f"PC{i+1}" for i in range(n_components)],
            index=num.columns,
        ).round(4)
        st.dataframe(loadings, use_container_width=True)
