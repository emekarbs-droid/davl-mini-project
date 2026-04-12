"""
lda_analysis.py
---------------
Linear Discriminant Analysis (applied only when target variable exists):
 - LDA projection
 - Class separation visualization
 - LDA component weights
"""

import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.preprocessing import StandardScaler, LabelEncoder


def show_lda(df: pd.DataFrame, target: str = None):
    """Render LDA analysis section."""
    st.subheader("📐 Linear Discriminant Analysis (LDA)")

    if not target or target not in df.columns:
        st.info("ℹ️ LDA requires a target column. No target detected for this dataset.")
        return

    numeric_df = df.select_dtypes(include=np.number)
    feature_cols = [c for c in numeric_df.columns if c != target]

    if len(feature_cols) < 1:
        st.warning("Need at least 1 numeric feature column for LDA.")
        return

    X = df[feature_cols].dropna()
    y_raw = df[target].iloc[X.index]

    # Encode target if needed
    if not pd.api.types.is_numeric_dtype(y_raw):
        le = LabelEncoder()
        y = le.fit_transform(y_raw.astype(str))
        class_names = le.classes_
    else:
        y = y_raw.values
        class_names = np.unique(y).astype(str)

    n_classes = len(np.unique(y))
    if n_classes < 2:
        st.warning("LDA requires at least 2 classes in the target column.")
        return

    # Standardize
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # LDA
    n_components = min(n_classes - 1, len(feature_cols), 3)
    lda = LinearDiscriminantAnalysis(n_components=n_components)
    try:
        X_lda = lda.fit_transform(X_scaled, y)
    except Exception as e:
        st.error(f"LDA failed: {e}")
        return

    explained = lda.explained_variance_ratio_ if hasattr(lda, "explained_variance_ratio_") else None

    # ── Metrics ───────────────────────────────────────────────────────────────
    c1, c2, c3 = st.columns(3)
    c1.metric("LDA Components", n_components)
    c2.metric("Classes", n_classes)
    c3.metric("Features Used", len(feature_cols))

    if explained is not None:
        st.markdown("#### 📋 Explained Variance Ratio")
        ev_df = pd.DataFrame({
            "Component": [f"LD{i+1}" for i in range(len(explained))],
            "Explained Variance %": (explained * 100).round(2),
            "Cumulative %": (np.cumsum(explained) * 100).round(2),
        })
        st.dataframe(ev_df, use_container_width=True)

    # ── 1D LDA Distribution ───────────────────────────────────────────────────
    st.markdown("#### 📊 LDA Class Separation — LD1 Distribution")
    lda_df = pd.DataFrame({"LD1": X_lda[:, 0],
                           target: [class_names[int(yi)] if yi < len(class_names)
                                    else str(yi) for yi in y]})
    fig1 = px.histogram(lda_df, x="LD1", color=target,
                        barmode="overlay",
                        template="plotly_dark",
                        title="LDA: Class Distribution on LD1",
                        opacity=0.75,
                        nbins=40)
    st.plotly_chart(fig1, use_container_width=True)

    # ── 2D LDA Scatter ────────────────────────────────────────────────────────
    if n_components >= 2:
        st.markdown("#### 🌐 2D LDA Projection")
        lda_df["LD2"] = X_lda[:, 1]
        fig2 = px.scatter(lda_df, x="LD1", y="LD2", color=target,
                          template="plotly_dark",
                          title="LDA: LD1 vs LD2 Class Separation",
                          opacity=0.75,
                          labels={"LD1": f"LD1 ({explained[0]*100:.1f}%)" if explained is not None else "LD1",
                                  "LD2": f"LD2 ({explained[1]*100:.1f}%)" if explained is not None else "LD2"})
        st.plotly_chart(fig2, use_container_width=True)

    # ── 3D LDA Scatter ────────────────────────────────────────────────────────
    if n_components >= 3:
        st.markdown("#### 🌐 3D LDA Projection")
        lda_df["LD3"] = X_lda[:, 2]
        fig3d = px.scatter_3d(lda_df, x="LD1", y="LD2", z="LD3",
                              color=target, opacity=0.7,
                              template="plotly_dark",
                              title="3D LDA Projection")
        st.plotly_chart(fig3d, use_container_width=True)

    # ── LDA Coefficients Heatmap ──────────────────────────────────────────────
    st.markdown("#### 🗺️ LDA Component Coefficients")
    coef_df = pd.DataFrame(
        lda.coef_,
        columns=feature_cols,
        index=[f"LD{i+1}" for i in range(len(lda.coef_))],
    ).T.round(4)

    fig_coef = go.Figure(data=go.Heatmap(
        z=coef_df.values,
        x=coef_df.columns.tolist(),
        y=coef_df.index.tolist(),
        colorscale="RdBu",
        zmid=0,
        text=coef_df.values.round(3),
        texttemplate="%{text}",
        textfont={"size": 9},
    ))
    fig_coef.update_layout(
        template="plotly_dark",
        title="LDA Discriminant Coefficients",
        height=max(400, len(feature_cols) * 22),
    )
    st.plotly_chart(fig_coef, use_container_width=True)
    st.dataframe(coef_df, use_container_width=True)

    # ── Between-Class Variance ────────────────────────────────────────────────
    st.markdown("#### 📊 Class Means in LDA Space")
    class_mean_df = lda_df.groupby(target)[["LD1"] + (["LD2"] if "LD2" in lda_df.columns else [])].mean().reset_index()
    st.dataframe(class_mean_df.round(4), use_container_width=True)
