"""
pca_analysis.py
---------------
Principal Component Analysis:
 - Standardize data
 - Compute PCA
 - Explained variance ratio
 - Scree plot
 - PCA scatter plot (2D)
 - Cumulative variance graph
 - Component loadings heatmap
"""

import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA


def show_pca(df: pd.DataFrame, target: str = None):
    """Render full PCA analysis section."""
    st.subheader("🔬 Principal Component Analysis (PCA)")

    numeric_df = df.select_dtypes(include=np.number)
    if target and target in numeric_df.columns:
        feature_cols = [c for c in numeric_df.columns if c != target]
    else:
        feature_cols = numeric_df.columns.tolist()

    if len(feature_cols) < 2:
        st.warning("Need at least 2 numeric feature columns for PCA.")
        return

    X = numeric_df[feature_cols].dropna()

    if X.shape[0] < 2:
        st.warning("Not enough valid rows for PCA after dropping NaNs.")
        return

    # Standardize
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # PCA
    n_components = min(len(feature_cols), X.shape[0], 20)
    pca = PCA(n_components=n_components, random_state=42)
    pca.fit(X_scaled)
    X_pca = pca.transform(X_scaled)

    explained = pca.explained_variance_ratio_
    cumulative = np.cumsum(explained)

    # ── Summary metrics ───────────────────────────────────────────────────────
    n95 = int(np.searchsorted(cumulative, 0.95)) + 1
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Components", n_components)
    c2.metric("Components for 95% Variance", n95)
    c3.metric("PC1 Explained Variance", f"{explained[0]*100:.2f}%")

    # ── Explained Variance Table ──────────────────────────────────────────────
    st.markdown("#### 📋 Explained Variance Ratio")
    ev_df = pd.DataFrame({
        "Component": [f"PC{i+1}" for i in range(n_components)],
        "Explained Variance Ratio": explained.round(4),
        "Explained Variance %": (explained * 100).round(2),
        "Cumulative Variance %": (cumulative * 100).round(2),
    })
    st.dataframe(ev_df, use_container_width=True)

    # ── Scree Plot + Cumulative Variance ──────────────────────────────────────
    st.markdown("#### 📈 Scree Plot & Cumulative Variance")
    fig = make_subplots(rows=1, cols=2,
                        subplot_titles=["Scree Plot", "Cumulative Explained Variance"])

    pc_labels = [f"PC{i+1}" for i in range(n_components)]

    fig.add_trace(go.Bar(x=pc_labels, y=(explained * 100).round(2),
                         name="Variance %", marker_color="#6366f1"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pc_labels, y=(explained * 100).round(2),
                             mode="lines+markers", name="Variance %",
                             line=dict(color="#a78bfa")), row=1, col=1)

    fig.add_trace(go.Scatter(x=pc_labels, y=(cumulative * 100).round(2),
                             mode="lines+markers+text",
                             name="Cumulative %",
                             line=dict(color="#34d399", width=2),
                             marker=dict(size=6)), row=1, col=2)
    fig.add_hline(y=95, line_dash="dash", line_color="#f59e0b",
                  annotation_text="95%", row=1, col=2)
    fig.add_hline(y=90, line_dash="dot", line_color="#fb923c",
                  annotation_text="90%", row=1, col=2)

    fig.update_layout(template="plotly_dark", height=420,
                      showlegend=False, margin=dict(t=60, b=20))
    st.plotly_chart(fig, use_container_width=True)

    # ── 2D PCA Scatter Plot ───────────────────────────────────────────────────
    st.markdown("#### 🌐 2D PCA Scatter Plot")
    pca_plot_df = pd.DataFrame(X_pca[:, :2], columns=["PC1", "PC2"])
    if target and target in df.columns:
        pca_plot_df[target] = df[target].iloc[X.index].values

    color_col = target if target and target in pca_plot_df.columns else None
    fig2 = px.scatter(pca_plot_df, x="PC1", y="PC2", color=color_col,
                      template="plotly_dark",
                      title="PCA: PC1 vs PC2",
                      opacity=0.7,
                      color_continuous_scale="Plasma",
                      labels={"PC1": f"PC1 ({explained[0]*100:.1f}%)",
                              "PC2": f"PC2 ({explained[1]*100:.1f}%)"})
    st.plotly_chart(fig2, use_container_width=True)

    # ── 3D PCA Scatter (if enough components) ────────────────────────────────
    if n_components >= 3:
        st.markdown("#### 🌐 3D PCA Scatter Plot")
        pca_3d = pd.DataFrame(X_pca[:, :3], columns=["PC1", "PC2", "PC3"])
        if target and target in df.columns:
            pca_3d[target] = df[target].iloc[X.index].values
        c_col = target if target and target in pca_3d.columns else None
        fig3d = px.scatter_3d(pca_3d, x="PC1", y="PC2", z="PC3",
                              color=c_col, opacity=0.65,
                              template="plotly_dark",
                              title="3D PCA Projection")
        st.plotly_chart(fig3d, use_container_width=True)

    # ── Component Loadings Heatmap ────────────────────────────────────────────
    st.markdown("#### 🗺️ PCA Component Loadings")
    n_show = min(10, n_components)
    loadings = pd.DataFrame(
        pca.components_[:n_show].T,
        index=feature_cols,
        columns=[f"PC{i+1}" for i in range(n_show)],
    ).round(3)

    fig_load = go.Figure(data=go.Heatmap(
        z=loadings.values,
        x=loadings.columns.tolist(),
        y=loadings.index.tolist(),
        colorscale="RdBu",
        zmid=0,
        text=loadings.values.round(2),
        texttemplate="%{text}",
        textfont={"size": 9},
    ))
    fig_load.update_layout(
        template="plotly_dark",
        title=f"PCA Component Loadings (Top {n_show} PCs)",
        height=max(400, len(feature_cols) * 22),
        xaxis_title="Principal Component",
        yaxis_title="Feature",
    )
    st.plotly_chart(fig_load, use_container_width=True)
    st.dataframe(loadings, use_container_width=True)
