"""
DAVL — Visualizations Module
All chart generation using Plotly (with Seaborn fallback for pair plots).
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import seaborn as sns
import io

# ---------- Plotly Theme ----------
PLOTLY_TEMPLATE = "plotly_dark"
COLOR_PALETTE = px.colors.qualitative.Set2
CONTINUOUS_SCALE = "Viridis"

CHART_LAYOUT = dict(
    template=PLOTLY_TEMPLATE,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", size=12, color="#e8ecf4"),
    margin=dict(l=40, r=40, t=50, b=40),
    hoverlabel=dict(
        bgcolor="#1a1f35",
        font_size=12,
        font_color="#e8ecf4",
        bordercolor="#3b82f6",
    ),
)


def _apply_layout(fig, title: str = "", height: int = 450):
    """Apply consistent styling to all Plotly figures."""
    fig.update_layout(
        **CHART_LAYOUT,
        title=dict(text=title, font=dict(size=16, color="#e8ecf4"), x=0.5),
        height=height,
    )
    fig.update_xaxes(gridcolor="rgba(42,48,80,0.5)", zerolinecolor="rgba(42,48,80,0.5)")
    fig.update_yaxes(gridcolor="rgba(42,48,80,0.5)", zerolinecolor="rgba(42,48,80,0.5)")
    return fig


# ---------- Chart Functions ----------

def histogram(df: pd.DataFrame, column: str, bins: int = 30, color_by: str = None):
    """Interactive histogram."""
    fig = px.histogram(
        df, x=column, nbins=bins, color=color_by,
        color_discrete_sequence=COLOR_PALETTE,
        opacity=0.85,
    )
    fig.update_traces(marker_line_width=0.5, marker_line_color="#2a3050")
    return _apply_layout(fig, f"Distribution of {column}")


def boxplot(df: pd.DataFrame, column: str, group_by: str = None):
    """Interactive boxplot."""
    fig = px.box(
        df, y=column, x=group_by,
        color=group_by,
        color_discrete_sequence=COLOR_PALETTE,
        points="outliers",
    )
    return _apply_layout(fig, f"Boxplot of {column}" + (f" by {group_by}" if group_by else ""))


def scatterplot(df: pd.DataFrame, x_col: str, y_col: str, color_by: str = None, size_by: str = None):
    """Interactive scatter plot."""
    fig = px.scatter(
        df, x=x_col, y=y_col, color=color_by, size=size_by,
        color_discrete_sequence=COLOR_PALETTE,
        opacity=0.7,
    )
    return _apply_layout(fig, f"{y_col} vs {x_col}")


def correlation_heatmap(corr_matrix: pd.DataFrame):
    """Interactive correlation heatmap."""
    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.index,
        colorscale="RdBu_r",
        zmin=-1, zmax=1,
        text=corr_matrix.round(2).values,
        texttemplate="%{text}",
        textfont={"size": 10},
        hovertemplate="<b>%{x}</b> vs <b>%{y}</b><br>Correlation: %{z:.3f}<extra></extra>",
    ))
    height = max(450, len(corr_matrix) * 35)
    return _apply_layout(fig, "Correlation Heatmap", height=height)


def count_plot(df: pd.DataFrame, column: str, top_n: int = 20):
    """Interactive count plot for categorical variables."""
    vc = df[column].value_counts().head(top_n)
    fig = px.bar(
        x=vc.index.astype(str), y=vc.values,
        color=vc.values,
        color_continuous_scale=CONTINUOUS_SCALE,
        labels={"x": column, "y": "Count", "color": "Count"},
    )
    fig.update_traces(
        marker_line_width=0.5, marker_line_color="#2a3050",
        hovertemplate="<b>%{x}</b><br>Count: %{y}<extra></extra>",
    )
    return _apply_layout(fig, f"Value Counts — {column}")


def bar_chart(df: pd.DataFrame, x_col: str, y_col: str, color_by: str = None):
    """Interactive bar chart."""
    fig = px.bar(
        df, x=x_col, y=y_col, color=color_by,
        color_discrete_sequence=COLOR_PALETTE,
        barmode="group",
    )
    return _apply_layout(fig, f"{y_col} by {x_col}")


def violin_plot(df: pd.DataFrame, column: str, group_by: str = None):
    """Interactive violin plot."""
    fig = px.violin(
        df, y=column, x=group_by, color=group_by,
        color_discrete_sequence=COLOR_PALETTE,
        box=True, points="outliers",
    )
    return _apply_layout(fig, f"Violin Plot — {column}" + (f" by {group_by}" if group_by else ""))


def missing_values_heatmap(df: pd.DataFrame):
    """Heatmap of missing values across all columns."""
    missing = df.isnull().astype(int)
    if missing.sum().sum() == 0:
        return None

    # Sample rows if too many
    if len(missing) > 200:
        missing = missing.sample(200, random_state=42).sort_index()

    fig = go.Figure(data=go.Heatmap(
        z=missing.values,
        x=missing.columns,
        y=[str(i) for i in missing.index],
        colorscale=[[0, "#1a1f35"], [1, "#f43f5e"]],
        showscale=True,
        colorbar=dict(
            title="Missing",
            tickvals=[0, 1],
            ticktext=["Present", "Missing"],
        ),
        hovertemplate="Col: <b>%{x}</b><br>Row: %{y}<br>%{z}<extra></extra>",
    ))
    height = max(400, min(len(missing) * 3, 600))
    return _apply_layout(fig, "Missing Values Heatmap", height=height)


def missing_bar_chart(df: pd.DataFrame):
    """Bar chart of missing value percentages."""
    missing_pct = (df.isnull().mean() * 100).round(2)
    missing_pct = missing_pct[missing_pct > 0].sort_values(ascending=True)

    if missing_pct.empty:
        return None

    fig = px.bar(
        x=missing_pct.values, y=missing_pct.index,
        orientation="h",
        color=missing_pct.values,
        color_continuous_scale=[[0, "#10b981"], [0.5, "#f59e0b"], [1, "#f43f5e"]],
        labels={"x": "Missing %", "y": "Column", "color": "Missing %"},
    )
    fig.update_traces(
        hovertemplate="<b>%{y}</b><br>Missing: %{x:.2f}%<extra></extra>",
    )
    height = max(350, len(missing_pct) * 30)
    return _apply_layout(fig, "Missing Values by Column", height=height)


def pairplot_matplotlib(df: pd.DataFrame, columns: list = None, hue: str = None, max_cols: int = 6):
    """Seaborn pair plot (returns matplotlib figure)."""
    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    if columns:
        numeric_cols = [c for c in columns if c in numeric_cols]
    numeric_cols = numeric_cols[:max_cols]

    if len(numeric_cols) < 2:
        return None

    plot_df = df[numeric_cols + ([hue] if hue and hue not in numeric_cols else [])].dropna()
    if len(plot_df) > 1000:
        plot_df = plot_df.sample(1000, random_state=42)

    sns.set_theme(style="dark", palette="Set2")
    fig = sns.pairplot(
        plot_df, hue=hue, diag_kind="kde",
        plot_kws={"alpha": 0.6, "s": 20},
        height=2.2,
    )
    fig.fig.patch.set_facecolor("#0a0e1a")
    for ax in fig.axes.flatten():
        ax.set_facecolor("#111827")
        ax.tick_params(colors="#8892a8", labelsize=8)
        ax.xaxis.label.set_color("#8892a8")
        ax.yaxis.label.set_color("#8892a8")

    plt.tight_layout()
    return fig.fig


def scree_plot(explained_variance: np.ndarray, title: str = "Scree Plot"):
    """Scree plot for PCA / Factor Analysis."""
    n = len(explained_variance)
    cumulative = np.cumsum(explained_variance)

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Bar(
            x=[f"PC{i+1}" for i in range(n)],
            y=explained_variance * 100,
            name="Individual",
            marker_color="#3b82f6",
            opacity=0.8,
        ),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(
            x=[f"PC{i+1}" for i in range(n)],
            y=cumulative * 100,
            name="Cumulative",
            mode="lines+markers",
            marker=dict(size=8, color="#f59e0b"),
            line=dict(width=2, color="#f59e0b"),
        ),
        secondary_y=True,
    )

    fig.update_yaxes(title_text="Individual Variance %", secondary_y=False)
    fig.update_yaxes(title_text="Cumulative Variance %", secondary_y=True)

    return _apply_layout(fig, title, height=450)


def scatter_2d(x, y, labels=None, title: str = "2D Scatter"):
    """Generic 2D scatter for PCA/LDA projections."""
    fig = px.scatter(
        x=x, y=y, color=labels,
        color_discrete_sequence=COLOR_PALETTE,
        labels={"x": "Component 1", "y": "Component 2", "color": "Class"},
        opacity=0.75,
    )
    fig.update_traces(marker=dict(size=7, line=dict(width=0.5, color="#2a3050")))
    return _apply_layout(fig, title)


def scatter_3d(x, y, z, labels=None, title: str = "3D Scatter"):
    """3D scatter for PCA/LDA projections."""
    fig = px.scatter_3d(
        x=x, y=y, z=z, color=labels,
        color_discrete_sequence=COLOR_PALETTE,
        labels={"x": "Comp 1", "y": "Comp 2", "z": "Comp 3", "color": "Class"},
        opacity=0.75,
    )
    fig.update_traces(marker=dict(size=4))
    fig.update_layout(
        scene=dict(
            xaxis=dict(backgroundcolor="#111827", gridcolor="#2a3050"),
            yaxis=dict(backgroundcolor="#111827", gridcolor="#2a3050"),
            zaxis=dict(backgroundcolor="#111827", gridcolor="#2a3050"),
        )
    )
    return _apply_layout(fig, title, height=550)


def loadings_heatmap(loadings: pd.DataFrame, title: str = "Component Loadings"):
    """Heatmap for PCA/Factor loadings."""
    fig = go.Figure(data=go.Heatmap(
        z=loadings.values,
        x=loadings.columns,
        y=loadings.index,
        colorscale="RdBu_r",
        text=loadings.round(3).values,
        texttemplate="%{text}",
        textfont={"size": 9},
    ))
    height = max(400, len(loadings) * 28)
    return _apply_layout(fig, title, height=height)
