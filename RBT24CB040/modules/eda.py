"""
eda.py
------
Exploratory Data Analysis:
 - Univariate analysis
 - Bivariate analysis
 - Multivariate analysis
 - Correlation analysis
 - Distribution analysis
"""

import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats as scipy_stats


def show_eda(df: pd.DataFrame, target: str = None):
    """Render EDA tabs."""
    st.subheader("🔭 Exploratory Data Analysis")

    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()

    tab1, tab2, tab3, tab4 = st.tabs([
        "Univariate", "Bivariate", "Multivariate", "Distribution"
    ])

    with tab1:
        _univariate(df, numeric_cols, cat_cols)

    with tab2:
        _bivariate(df, numeric_cols, cat_cols, target)

    with tab3:
        _multivariate(df, numeric_cols, target)

    with tab4:
        _distribution_analysis(df, numeric_cols)


# ── Univariate ────────────────────────────────────────────────────────────────

def _univariate(df, numeric_cols, cat_cols):
    st.markdown("#### 📊 Univariate Analysis")

    if numeric_cols:
        st.markdown("**Numeric Columns**")
        selected = st.selectbox("Select numeric column", numeric_cols,
                                key="uni_num_col")
        series = df[selected].dropna()

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Mean", f"{series.mean():.4f}")
        col2.metric("Median", f"{series.median():.4f}")
        col3.metric("Std Dev", f"{series.std():.4f}")
        col4.metric("Skewness", f"{series.skew():.4f}")

        fig = make_subplots(rows=1, cols=2,
                            subplot_titles=["Histogram + KDE", "Box Plot"])
        fig.add_trace(go.Histogram(x=series, nbinsx=30, name="Histogram",
                                   marker_color="#6366f1", opacity=0.8), row=1, col=1)
        fig.add_trace(go.Box(y=series, name="Boxplot",
                             marker_color="#f59e0b", boxmean=True), row=1, col=2)
        fig.update_layout(template="plotly_dark", height=400,
                          showlegend=False, margin=dict(t=40, b=20))
        st.plotly_chart(fig, use_container_width=True)

    if cat_cols:
        st.markdown("**Categorical Columns**")
        sel_cat = st.selectbox("Select categorical column", cat_cols,
                               key="uni_cat_col")
        vc = df[sel_cat].value_counts().head(20)
        fig2 = px.bar(x=vc.index, y=vc.values, labels={"x": sel_cat, "y": "Count"},
                      title=f"Value Counts: {sel_cat}",
                      color=vc.values, color_continuous_scale="Viridis",
                      template="plotly_dark")
        st.plotly_chart(fig2, use_container_width=True)


# ── Bivariate ─────────────────────────────────────────────────────────────────

def _bivariate(df, numeric_cols, cat_cols, target):
    st.markdown("#### 📊 Bivariate Analysis")

    if len(numeric_cols) >= 2:
        st.markdown("**Numeric vs Numeric (Scatter)**")
        c1, c2 = st.columns(2)
        x_col = c1.selectbox("X axis", numeric_cols, key="biv_x")
        y_col = c2.selectbox("Y axis", numeric_cols,
                             index=min(1, len(numeric_cols) - 1), key="biv_y")

        color_arg = target if target and target in df.columns else None
        fig = px.scatter(df, x=x_col, y=y_col, color=color_arg,
                         trendline="ols",
                         template="plotly_dark",
                         title=f"{x_col} vs {y_col}",
                         opacity=0.7,
                         color_continuous_scale="Viridis")
        st.plotly_chart(fig, use_container_width=True)

        # Pearson r
        r, p = scipy_stats.pearsonr(df[x_col].dropna(), df[y_col].dropna())
        st.info(f"Pearson r = **{r:.4f}** | p-value = **{p:.4f}**  "
                f"({'Significant' if p < 0.05 else 'Not significant'} at α=0.05)")

    if target and target in df.columns and numeric_cols:
        st.markdown(f"**Numeric Features vs Target (`{target}`)**")
        sel_feat = st.selectbox("Feature vs target", numeric_cols, key="biv_target")
        if df[target].nunique() <= 15:
            fig2 = px.violin(df, x=target, y=sel_feat,
                             box=True, color=target,
                             template="plotly_dark",
                             title=f"{sel_feat} by {target}")
        else:
            fig2 = px.scatter(df, x=target, y=sel_feat, template="plotly_dark",
                              title=f"{sel_feat} vs {target}", opacity=0.6)
        st.plotly_chart(fig2, use_container_width=True)

    if cat_cols and numeric_cols:
        st.markdown("**Categorical vs Numeric (Bar / Violin)**")
        cc1, cc2 = st.columns(2)
        cat_sel = cc1.selectbox("Categorical column", cat_cols, key="biv_cat")
        num_sel = cc2.selectbox("Numeric column", numeric_cols, key="biv_num")
        top_cats = df[cat_sel].value_counts().head(15).index
        filtered = df[df[cat_sel].isin(top_cats)]
        fig3 = px.violin(filtered, x=cat_sel, y=num_sel, box=True,
                         color=cat_sel, template="plotly_dark",
                         title=f"{num_sel} by {cat_sel}")
        st.plotly_chart(fig3, use_container_width=True)


# ── Multivariate ──────────────────────────────────────────────────────────────

def _multivariate(df, numeric_cols, target):
    st.markdown("#### 📊 Multivariate Analysis")

    if len(numeric_cols) < 2:
        st.info("Need at least 2 numeric columns for multivariate analysis.")
        return

    # Pairplot (limited to 6 columns for performance)
    st.markdown("**Pair Plot (up to 6 numeric features)**")
    n_cols = min(6, len(numeric_cols))
    selected_cols = st.multiselect(
        "Select columns for pair plot",
        numeric_cols,
        default=numeric_cols[:n_cols],
        max_selections=6,
        key="mv_pairplot"
    )

    if len(selected_cols) >= 2:
        color_col = target if target and target in df.columns else None
        fig_pair = px.scatter_matrix(
            df,
            dimensions=selected_cols,
            color=color_col,
            template="plotly_dark",
            title="Pair Plot",
            opacity=0.5,
        )
        fig_pair.update_traces(diagonal_visible=True, showupperhalf=False)
        fig_pair.update_layout(height=700)
        st.plotly_chart(fig_pair, use_container_width=True)

    # 3D scatter
    if len(numeric_cols) >= 3:
        st.markdown("**3D Scatter Plot**")
        cols3 = st.columns(3)
        ax1 = cols3[0].selectbox("X", numeric_cols, index=0, key="3d_x")
        ax2 = cols3[1].selectbox("Y", numeric_cols, index=1, key="3d_y")
        ax3 = cols3[2].selectbox("Z", numeric_cols, index=2, key="3d_z")
        color_col = target if target and target in df.columns else None
        fig3d = px.scatter_3d(df, x=ax1, y=ax2, z=ax3, color=color_col,
                              opacity=0.7, template="plotly_dark",
                              title="3D Scatter Plot")
        st.plotly_chart(fig3d, use_container_width=True)


# ── Distribution Analysis ─────────────────────────────────────────────────────

def _distribution_analysis(df, numeric_cols):
    st.markdown("#### 📈 Distribution Analysis")
    if not numeric_cols:
        st.info("No numeric columns available.")
        return

    n = len(numeric_cols)
    n_cols_grid = min(3, n)
    n_rows_grid = (n + n_cols_grid - 1) // n_cols_grid

    fig = make_subplots(
        rows=n_rows_grid, cols=n_cols_grid,
        subplot_titles=numeric_cols[:n_rows_grid * n_cols_grid],
    )

    colors = px.colors.qualitative.Plotly
    for idx, col in enumerate(numeric_cols[:n_rows_grid * n_cols_grid]):
        row = idx // n_cols_grid + 1
        col_pos = idx % n_cols_grid + 1
        series = df[col].dropna()
        fig.add_trace(
            go.Histogram(x=series, nbinsx=25,
                         marker_color=colors[idx % len(colors)],
                         name=col, opacity=0.8),
            row=row, col=col_pos
        )

    fig.update_layout(
        template="plotly_dark",
        height=300 * n_rows_grid,
        showlegend=False,
        title_text="Distribution of All Numeric Columns",
        margin=dict(t=60, b=20),
    )
    st.plotly_chart(fig, use_container_width=True)
