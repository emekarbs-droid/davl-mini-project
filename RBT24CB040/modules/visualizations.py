"""
visualizations.py
-----------------
Auto-generate all required visualizations:
 - Histogram, Boxplot, Scatterplot
 - Pairplot, Correlation heatmap
 - Count plot, Bar chart, Violin plot
 - Missing values heatmap
"""

import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import seaborn as sns
import io


sns.set_theme(style="darkgrid")


def show_visualizations(df: pd.DataFrame, target: str = None):
    """Render all auto-generated visualizations in organized sections."""
    st.subheader("📊 Visualizations")

    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()

    tabs = st.tabs([
        "📦 Histograms", "📦 Boxplots", "🔵 Scatter",
        "🟣 Violin", "🌡️ Heatmaps", "📊 Count / Bar",
        "🕳️ Missing Heatmap"
    ])

    with tabs[0]:
        _histograms(df, numeric_cols)

    with tabs[1]:
        _boxplots(df, numeric_cols)

    with tabs[2]:
        _scatterplots(df, numeric_cols, target)

    with tabs[3]:
        _violin_plots(df, numeric_cols, cat_cols, target)

    with tabs[4]:
        _correlation_heatmap(df, numeric_cols)

    with tabs[5]:
        _count_bar_charts(df, cat_cols, numeric_cols, target)

    with tabs[6]:
        _missing_heatmap(df)


# ── Histograms ────────────────────────────────────────────────────────────────

def _histograms(df, numeric_cols):
    st.markdown("#### 📦 Histograms")
    if not numeric_cols:
        st.info("No numeric columns.")
        return

    n = len(numeric_cols)
    n_cols = min(3, n)
    n_rows = (n + n_cols - 1) // n_cols
    display_cols = numeric_cols[:min(n, 12)]  # cap at 12

    fig = make_subplots(rows=n_rows, cols=n_cols,
                        subplot_titles=display_cols)
    colors = px.colors.qualitative.Vivid

    for idx, col in enumerate(display_cols):
        r, c = divmod(idx, n_cols)
        series = df[col].dropna()
        fig.add_trace(
            go.Histogram(x=series, nbinsx=30,
                         marker_color=colors[idx % len(colors)],
                         name=col, opacity=0.85),
            row=r + 1, col=c + 1
        )

    fig.update_layout(
        template="plotly_dark", height=350 * n_rows,
        showlegend=False, title_text="Histograms – All Numeric Features",
        margin=dict(t=60, b=20),
    )
    st.plotly_chart(fig, use_container_width=True)


# ── Boxplots ──────────────────────────────────────────────────────────────────

def _boxplots(df, numeric_cols):
    st.markdown("#### 📦 Boxplots")
    if not numeric_cols:
        st.info("No numeric columns.")
        return

    fig = go.Figure()
    colors = px.colors.qualitative.Pastel
    for idx, col in enumerate(numeric_cols):
        fig.add_trace(go.Box(
            y=df[col].dropna(),
            name=col,
            boxmean=True,
            marker_color=colors[idx % len(colors)],
        ))
    fig.update_layout(
        template="plotly_dark",
        title="Boxplots – All Numeric Features",
        height=500,
        xaxis_tickangle=-30,
    )
    st.plotly_chart(fig, use_container_width=True)


# ── Scatter Plots ─────────────────────────────────────────────────────────────

def _scatterplots(df, numeric_cols, target):
    st.markdown("#### 🔵 Scatter Plots")
    if len(numeric_cols) < 2:
        st.info("Need at least 2 numeric columns.")
        return

    c1, c2 = st.columns(2)
    x_sel = c1.selectbox("X Axis", numeric_cols, key="viz_scatter_x")
    y_sel = c2.selectbox("Y Axis", numeric_cols,
                         index=min(1, len(numeric_cols) - 1), key="viz_scatter_y")

    color_col = target if target and target in df.columns else None

    fig = px.scatter(df, x=x_sel, y=y_sel, color=color_col,
                     trendline="ols",
                     marginal_x="histogram", marginal_y="violin",
                     template="plotly_dark",
                     title=f"Scatter: {x_sel} vs {y_sel}",
                     opacity=0.6,
                     color_continuous_scale="Plasma")
    st.plotly_chart(fig, use_container_width=True)


# ── Violin Plots ──────────────────────────────────────────────────────────────

def _violin_plots(df, numeric_cols, cat_cols, target):
    st.markdown("#### 🟣 Violin Plots")
    if not numeric_cols:
        st.info("No numeric columns.")
        return

    group_col = target if target and target in df.columns and df[target].nunique() <= 15 else None
    if not group_col and cat_cols:
        candidates = [c for c in cat_cols if df[c].nunique() <= 10]
        if candidates:
            group_col = candidates[0]

    sel_num = st.selectbox("Numeric column for violin", numeric_cols, key="viz_violin")

    if group_col:
        fig = px.violin(df, y=sel_num, x=group_col, color=group_col,
                        box=True, points="outliers",
                        template="plotly_dark",
                        title=f"Violin: {sel_num} by {group_col}")
    else:
        fig = px.violin(df, y=sel_num, box=True, points="outliers",
                        template="plotly_dark",
                        title=f"Violin: {sel_num}")

    st.plotly_chart(fig, use_container_width=True)


# ── Correlation Heatmap ───────────────────────────────────────────────────────

def _correlation_heatmap(df, numeric_cols):
    st.markdown("#### 🌡️ Correlation Heatmap")
    if len(numeric_cols) < 2:
        st.info("Need at least 2 numeric columns.")
        return

    corr = df[numeric_cols].corr().round(2)

    fig = go.Figure(data=go.Heatmap(
        z=corr.values,
        x=corr.columns.tolist(),
        y=corr.index.tolist(),
        colorscale="RdYlGn",
        zmid=0,
        text=corr.values.round(2),
        texttemplate="%{text}",
        textfont={"size": 10},
        hoverongaps=False,
    ))
    fig.update_layout(
        template="plotly_dark",
        title="Pearson Correlation Heatmap",
        height=max(450, len(numeric_cols) * 35),
        xaxis_tickangle=-35,
    )
    st.plotly_chart(fig, use_container_width=True)

    # Seaborn static version for download
    st.markdown("**Seaborn Heatmap (downloadable)**")
    fig_sea, ax = plt.subplots(figsize=(max(8, len(numeric_cols)), max(6, len(numeric_cols) - 1)))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", ax=ax,
                linewidths=0.5, square=True)
    ax.set_title("Correlation Heatmap", fontsize=14, pad=12)
    plt.tight_layout()
    buf = io.BytesIO()
    fig_sea.savefig(buf, format="png", dpi=120, bbox_inches="tight")
    buf.seek(0)
    st.download_button("⬇️ Download Heatmap (PNG)", buf, file_name="correlation_heatmap.png",
                       mime="image/png")
    st.pyplot(fig_sea)
    plt.close(fig_sea)


# ── Count / Bar Charts ────────────────────────────────────────────────────────

def _count_bar_charts(df, cat_cols, numeric_cols, target):
    st.markdown("#### 📊 Count & Bar Charts")

    if cat_cols:
        st.markdown("**Count Plots (Categorical)**")
        n = len(cat_cols)
        n_cols = min(2, n)
        n_rows = (n + n_cols - 1) // n_cols
        display = cat_cols[:min(n, 8)]   # cap at 8

        fig = make_subplots(rows=(len(display) + 1) // 2,
                            cols=2,
                            subplot_titles=display)
        colors = px.colors.qualitative.Bold
        for idx, col in enumerate(display):
            vc = df[col].value_counts().head(15)
            r, c = divmod(idx, 2)
            fig.add_trace(
                go.Bar(x=vc.index.astype(str), y=vc.values,
                       name=col, marker_color=colors[idx % len(colors)]),
                row=r + 1, col=c + 1
            )
        fig.update_layout(template="plotly_dark",
                          height=350 * ((len(display) + 1) // 2),
                          showlegend=False,
                          title_text="Count Plots – Categorical Features")
        st.plotly_chart(fig, use_container_width=True)

    if target and target in df.columns and numeric_cols:
        st.markdown(f"**Mean of Numeric Features grouped by `{target}`**")
        if df[target].nunique() <= 20:
            agg = df.groupby(target)[numeric_cols[:5]].mean().reset_index()
            fig2 = px.bar(agg.melt(id_vars=target),
                          x=target, y="value", color="variable",
                          barmode="group", template="plotly_dark",
                          title=f"Mean Feature Values by {target}")
            st.plotly_chart(fig2, use_container_width=True)


# ── Missing Values Heatmap ────────────────────────────────────────────────────

def _missing_heatmap(df):
    st.markdown("#### 🕳️ Missing Values Heatmap")
    missing = df.isnull()

    if missing.sum().sum() == 0:
        st.success("✅ No missing values — heatmap not required.")
        return

    # Plotly heatmap
    z = missing.astype(int).values
    fig = go.Figure(data=go.Heatmap(
        z=z,
        x=df.columns.tolist(),
        y=list(range(len(df))),
        colorscale=[[0, "#1e293b"], [1, "#f43f5e"]],
        showscale=True,
        colorbar=dict(title="Missing", tickvals=[0, 1],
                      ticktext=["Present", "Missing"]),
    ))
    fig.update_layout(
        template="plotly_dark",
        title="Missing Values Heatmap (red = missing)",
        height=400,
        xaxis_tickangle=-35,
        yaxis_title="Row Index",
    )
    st.plotly_chart(fig, use_container_width=True)

    # Seaborn version
    cols_with_missing = [c for c in df.columns if df[c].isnull().any()]
    if cols_with_missing:
        fig_sea, ax = plt.subplots(figsize=(max(8, len(cols_with_missing) * 0.8), 5))
        sns.heatmap(df[cols_with_missing].isnull(), cbar=True, yticklabels=False,
                    cmap="magma_r", ax=ax)
        ax.set_title("Missing Value Pattern (Seaborn)", fontsize=13)
        plt.tight_layout()
        buf = io.BytesIO()
        fig_sea.savefig(buf, format="png", dpi=100, bbox_inches="tight")
        buf.seek(0)
        st.download_button("⬇️ Download Missing Heatmap", buf,
                           file_name="missing_heatmap.png", mime="image/png")
        st.pyplot(fig_sea)
        plt.close(fig_sea)
