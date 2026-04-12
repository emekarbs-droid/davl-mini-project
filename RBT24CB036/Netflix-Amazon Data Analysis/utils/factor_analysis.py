"""
factor_analysis.py — Factor Analysis: KMO, loadings, communalities.
Uses sklearn FactorAnalysis as primary (avoids factor-analyzer compat issues)
and factor_analyzer library for KMO/Bartlett tests when available.
"""
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
from sklearn.decomposition import FactorAnalysis as SKFactorAnalysis
from sklearn.preprocessing import StandardScaler


def show_factor_analysis(df, name="Dataset"):
    """Run Factor Analysis on numeric columns."""
    st.subheader(f"🧩 Factor Analysis — {name}")

    num_cols = df.select_dtypes(include="number").columns.tolist()
    if len(num_cols) < 3:
        st.info("Need at least 3 numeric columns for Factor Analysis.")
        return

    num = df[num_cols].dropna()
    if len(num) < 10:
        st.warning("Not enough data rows.")
        return

    # KMO test (optional — may fail due to library version)
    try:
        from factor_analyzer.factor_analyzer import calculate_kmo
        kmo_all, kmo_model = calculate_kmo(num)
        st.metric("KMO Measure", f"{kmo_model:.4f}")
        if kmo_model < 0.5:
            st.warning("KMO < 0.5 — data may not be suitable for factor analysis.")
        elif kmo_model < 0.7:
            st.info("KMO is mediocre. Interpret with caution.")
        else:
            st.success("KMO ≥ 0.7 — good for factor analysis.")
    except Exception:
        st.info("KMO test not available (library compatibility).")

    # Bartlett's test (optional)
    try:
        from factor_analyzer.factor_analyzer import calculate_bartlett_sphericity
        chi2, p = calculate_bartlett_sphericity(num)
        c1, c2 = st.columns(2)
        c1.metric("Bartlett's Chi²", f"{chi2:.2f}")
        c2.metric("p-value", f"{p:.6f}")
        if p < 0.05:
            st.success("Bartlett's test significant — correlation structure exists.")
        else:
            st.warning("Bartlett's test not significant.")
    except Exception:
        st.info("Bartlett's test not available (library compatibility).")

    # Factor Analysis using sklearn (always works)
    max_factors = min(len(num_cols) - 1, 10)
    if max_factors < 2:
        max_factors = 2
    n_factors = st.slider("Number of factors", 2, max_factors,
                          min(3, max_factors), key=f"fa_nfactors_{name}")

    try:
        # Standardize
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(num)

        fa = SKFactorAnalysis(n_components=n_factors, random_state=42)
        fa.fit(X_scaled)

        # Loadings (components_ transposed)
        loadings = pd.DataFrame(
            fa.components_.T,
            index=num_cols,
            columns=[f"Factor {i+1}" for i in range(n_factors)],
        ).round(4)

        st.markdown("**Factor Loadings**")
        st.dataframe(loadings, use_container_width=True)

        # Heatmap
        fig = px.imshow(loadings, text_auto=".2f",
                        title="Factor Loadings Heatmap",
                        color_continuous_scale="RdBu_r", aspect="auto")
        st.plotly_chart(fig, use_container_width=True)

        # Communalities (sum of squared loadings per variable)
        communalities = (loadings ** 2).sum(axis=1).round(4)
        comm = pd.DataFrame({
            "Variable": num_cols,
            "Communality": communalities.values,
        })
        st.markdown("**Communalities**")
        st.dataframe(comm, use_container_width=True, hide_index=True)

        # Variance explained (sum of squared loadings per factor)
        ss_loadings = (loadings ** 2).sum(axis=0)
        prop_var = ss_loadings / len(num_cols)
        cum_var = prop_var.cumsum()

        var_df = pd.DataFrame({
            "Factor": [f"Factor {i+1}" for i in range(n_factors)],
            "SS Loadings": ss_loadings.round(4).values,
            "Proportion Var": prop_var.round(4).values,
            "Cumulative Var": cum_var.round(4).values,
        })
        st.markdown("**Variance Explained**")
        st.dataframe(var_df, use_container_width=True, hide_index=True)

        # Noise variance
        st.markdown("**Noise Variance (Uniqueness)**")
        noise = pd.DataFrame({
            "Variable": num_cols,
            "Noise Variance": np.round(fa.noise_variance_, 4),
        })
        st.dataframe(noise, use_container_width=True, hide_index=True)

    except Exception as e:
        st.error(f"Factor Analysis failed: {e}")
