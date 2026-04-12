"""
factor_analysis.py
------------------
Factor Analysis:
 - Optimal factor count (scree plot)
 - Factor loadings
 - Rotated factor matrix (varimax)
 - Communalities
"""

import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from sklearn.preprocessing import StandardScaler

try:
    from factor_analyzer import FactorAnalyzer
    from factor_analyzer.factor_analyzer import calculate_kmo, calculate_bartlett_sphericity
    FACTOR_ANALYZER_AVAILABLE = True
except ImportError:
    FACTOR_ANALYZER_AVAILABLE = False


def show_factor_analysis(df: pd.DataFrame):
    """Render factor analysis section."""
    st.subheader("🔮 Factor Analysis")

    if not FACTOR_ANALYZER_AVAILABLE:
        st.error("❌ `factor_analyzer` package not installed. Run: `pip install factor_analyzer`")
        return

    numeric_df = df.select_dtypes(include=np.number).dropna()

    if numeric_df.shape[1] < 3:
        st.warning("Factor analysis requires at least 3 numeric columns.")
        return

    if numeric_df.shape[0] < numeric_df.shape[1]:
        st.warning("Factor analysis requires more rows than columns.")
        return

    feature_cols = numeric_df.columns.tolist()
    X = numeric_df.values

    # Standardize
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # ── KMO & Bartlett Tests ──────────────────────────────────────────────────
    st.markdown("#### 🧪 Adequacy Tests")
    try:
        kmo_all, kmo_model = calculate_kmo(X_scaled)
        chi_sq, p_val = calculate_bartlett_sphericity(X_scaled)

        c1, c2, c3 = st.columns(3)
        c1.metric("KMO Score", f"{kmo_model:.4f}",
                  help="KMO > 0.6 suggests FA is appropriate.")
        c2.metric("Bartlett χ²", f"{chi_sq:.2f}")
        c3.metric("Bartlett p-value", f"{p_val:.4e}")

        if kmo_model >= 0.8:
            st.success(f"✅ KMO = {kmo_model:.4f} — **Meritorious** (excellent for FA)")
        elif kmo_model >= 0.7:
            st.success(f"✅ KMO = {kmo_model:.4f} — **Middling** (acceptable for FA)")
        elif kmo_model >= 0.6:
            st.warning(f"🟡 KMO = {kmo_model:.4f} — **Mediocre** (marginal)")
        else:
            st.error(f"🔴 KMO = {kmo_model:.4f} — **Unacceptable** for Factor Analysis")

        if p_val < 0.05:
            st.success("✅ Bartlett's test: p < 0.05 — data is suitable for FA.")
        else:
            st.error("❌ Bartlett's test: p ≥ 0.05 — data may NOT be suitable for FA.")
    except Exception as e:
        st.warning(f"Could not compute adequacy tests: {e}")

    # ── Scree Plot (Eigenvalues) ──────────────────────────────────────────────
    st.markdown("#### 📈 Scree Plot — Eigenvalues")
    try:
        fa_full = FactorAnalyzer(n_factors=min(len(feature_cols), X_scaled.shape[0] - 1),
                                 rotation=None)
        fa_full.fit(X_scaled)
        eigenvalues, _ = fa_full.get_eigenvalues()

        n_factors_kaiser = int((eigenvalues > 1).sum())
        n_factors_use = max(2, min(n_factors_kaiser, len(feature_cols) - 1))

        fig_scree = go.Figure()
        fig_scree.add_trace(go.Scatter(
            x=list(range(1, len(eigenvalues) + 1)),
            y=eigenvalues,
            mode="lines+markers",
            name="Eigenvalue",
            line=dict(color="#6366f1", width=2),
            marker=dict(size=7),
        ))
        fig_scree.add_hline(y=1, line_dash="dash", line_color="#f59e0b",
                            annotation_text="Kaiser Criterion (λ=1)")
        fig_scree.update_layout(
            template="plotly_dark",
            title=f"Scree Plot — {n_factors_kaiser} factors with λ > 1",
            xaxis_title="Factor Number",
            yaxis_title="Eigenvalue",
            height=400,
        )
        st.plotly_chart(fig_scree, use_container_width=True)

        st.info(f"📌 Suggested number of factors (Kaiser criterion): **{n_factors_kaiser}**")

    except Exception as e:
        st.error(f"Eigenvalue computation failed: {e}")
        return

    # ── User factor selection ─────────────────────────────────────────────────
    n_factors_use = st.slider(
        "Select number of factors", min_value=2,
        max_value=min(len(feature_cols) - 1, 15),
        value=n_factors_use
    )

    # ── Factor Analysis with Varimax Rotation ─────────────────────────────────
    st.markdown(f"#### 📊 Factor Loadings ({n_factors_use} factors, Varimax Rotation)")
    try:
        fa = FactorAnalyzer(n_factors=n_factors_use, rotation="varimax")
        fa.fit(X_scaled)

        loadings = fa.loadings_
        loadings_df = pd.DataFrame(
            loadings,
            index=feature_cols,
            columns=[f"Factor{i+1}" for i in range(n_factors_use)],
        ).round(4)

        # Loadings heatmap
        fig_load = go.Figure(data=go.Heatmap(
            z=loadings_df.values,
            x=loadings_df.columns.tolist(),
            y=loadings_df.index.tolist(),
            colorscale="RdBu",
            zmid=0,
            text=loadings_df.values.round(2),
            texttemplate="%{text}",
            textfont={"size": 9},
        ))
        fig_load.update_layout(
            template="plotly_dark",
            title="Factor Loadings Heatmap (Varimax Rotation)",
            height=max(400, len(feature_cols) * 22),
        )
        st.plotly_chart(fig_load, use_container_width=True)

        st.markdown("**Factor Loadings Table** (|loading| ≥ 0.3 highlighted)")
        styled = loadings_df.style.applymap(
            lambda v: "background-color: #6366f1; color: white;"
            if abs(v) >= 0.5 else (
                "background-color: #7c3aed; color: white;"
                if abs(v) >= 0.3 else ""
            )
        ).format("{:.4f}")
        st.dataframe(styled, use_container_width=True)

    except Exception as e:
        st.error(f"Factor loadings computation failed: {e}")
        return

    # ── Communalities ─────────────────────────────────────────────────────────
    st.markdown("#### 📋 Communalities")
    try:
        comm = fa.get_communalities()
        comm_df = pd.DataFrame({
            "Feature": feature_cols,
            "Communality": comm.round(4),
            "Uniqueness": (1 - comm).round(4),
            "Interpretation": [
                "✅ Well explained" if c >= 0.6 else
                "🟡 Moderate" if c >= 0.4 else
                "🔴 Poorly explained" for c in comm
            ],
        }).sort_values("Communality", ascending=False)
        st.dataframe(comm_df.reset_index(drop=True), use_container_width=True)

        fig_comm = px.bar(comm_df, x="Feature", y="Communality",
                          color="Communality",
                          color_continuous_scale="Viridis",
                          template="plotly_dark",
                          title="Feature Communalities")
        fig_comm.add_hline(y=0.6, line_dash="dash", line_color="#f59e0b",
                           annotation_text="0.6 threshold")
        st.plotly_chart(fig_comm, use_container_width=True)

    except Exception as e:
        st.error(f"Communality computation failed: {e}")

    # ── Variance Explained per Factor ─────────────────────────────────────────
    st.markdown("#### 📐 Variance Explained by Each Factor")
    try:
        var_df = fa.get_factor_variance()
        var_table = pd.DataFrame(
            var_df,
            index=["SS Loadings", "Proportion Var", "Cumulative Var"],
            columns=[f"Factor{i+1}" for i in range(n_factors_use)],
        ).T.round(4)
        var_table["Proportion Var %"] = (var_table["Proportion Var"] * 100).round(2)
        var_table["Cumulative Var %"] = (var_table["Cumulative Var"] * 100).round(2)
        st.dataframe(var_table, use_container_width=True)

        fig_var = px.bar(var_table.reset_index(),
                         x="index", y="Proportion Var %",
                         title="Proportion of Variance Explained",
                         template="plotly_dark",
                         color="Proportion Var %",
                         color_continuous_scale="Plasma")
        st.plotly_chart(fig_var, use_container_width=True)
    except Exception as e:
        st.warning(f"Variance table unavailable: {e}")
