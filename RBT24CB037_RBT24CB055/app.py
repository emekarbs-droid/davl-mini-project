"""
ML Analytics Dashboard — A comprehensive web application for
Exploratory Data Analysis, PCA, LDA, and Factor Analysis on CSV datasets.
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from io import StringIO

# Scikit-learn imports
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.decomposition import PCA, FactorAnalysis
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.impute import SimpleImputer
from sklearn.model_selection import cross_val_score

from scipy import stats

# ─────────────────────────────────────────────────────────────
# Page config
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ML Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────
# Custom CSS for premium look
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* ── Global ── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    /* ── Header banner ── */
    .main-header {
        background: linear-gradient(135deg, #6C63FF 0%, #3F3D9E 50%, #1A1F2E 100%);
        padding: 2rem 2.5rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(108, 99, 255, 0.25);
    }
    .main-header h1 {
        color: #FFFFFF;
        font-weight: 700;
        font-size: 2.2rem;
        margin: 0;
    }
    .main-header p {
        color: #C5C3FF;
        font-size: 1.05rem;
        margin: .4rem 0 0 0;
    }

    /* ── Metric cards ── */
    .metric-card {
        background: linear-gradient(145deg, #1E2433 0%, #161B26 100%);
        padding: 1.4rem;
        border-radius: 14px;
        border: 1px solid rgba(108, 99, 255, 0.15);
        text-align: center;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 24px rgba(108, 99, 255, 0.18);
    }
    .metric-card h3 {
        color: #6C63FF;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.4rem;
    }
    .metric-card p {
        color: #FAFAFA;
        font-size: 1.8rem;
        font-weight: 700;
        margin: 0;
    }

    /* ── Section headers ── */
    .section-header {
        background: linear-gradient(90deg, rgba(108,99,255,0.12) 0%, transparent 100%);
        padding: 0.8rem 1.2rem;
        border-left: 4px solid #6C63FF;
        border-radius: 0 10px 10px 0;
        margin: 1.8rem 0 1rem 0;
    }
    .section-header h2 {
        color: #FAFAFA;
        font-size: 1.3rem;
        margin: 0;
    }

    /* ── Tabs ── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 8px 20px;
        font-weight: 500;
    }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #12151E 0%, #0E1117 100%);
    }

    /* ── Hide default header/footer ── */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* ── Expander ── */
    .streamlit-expanderHeader {
        font-weight: 600;
        font-size: 1rem;
    }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# Helper utilities
# ─────────────────────────────────────────────────────────────

def get_numeric_df(df: pd.DataFrame) -> pd.DataFrame:
    """Return only numeric columns."""
    return df.select_dtypes(include=[np.number])


def get_categorical_df(df: pd.DataFrame) -> pd.DataFrame:
    """Return only categorical / object columns."""
    return df.select_dtypes(include=["object", "category", "str"])


def clean_numeric(df: pd.DataFrame) -> pd.DataFrame:
    """Replace inf/-inf with NaN, then drop columns that are entirely NaN."""
    cleaned = df.replace([np.inf, -np.inf], np.nan)
    # Drop columns where every value is NaN (no useful data)
    cleaned = cleaned.dropna(axis=1, how="all")
    return cleaned


def impute_numeric(df: pd.DataFrame) -> pd.DataFrame:
    """Impute missing values in numeric columns with the median.
    Handles inf values by converting them to NaN first."""
    num_df = get_numeric_df(df)
    num_df = clean_numeric(num_df)
    if num_df.empty:
        return num_df
    if num_df.isnull().sum().sum() == 0:
        return num_df
    imputer = SimpleImputer(strategy="median")
    imputed = pd.DataFrame(
        imputer.fit_transform(num_df), columns=num_df.columns, index=num_df.index
    )
    return imputed


def scale_data(df: pd.DataFrame):
    """Standardise numeric data; return (scaled_array, scaler, column_names).
    Cleans inf values and drops constant columns before scaling."""
    cleaned = clean_numeric(df)
    # Drop columns with zero variance (constant columns cause div-by-zero)
    non_const = cleaned.loc[:, cleaned.nunique() > 1]
    if non_const.empty:
        raise ValueError("No valid numeric columns remaining after cleaning.")
    scaler = StandardScaler()
    scaled = scaler.fit_transform(non_const)
    return scaled, scaler, non_const.columns.tolist()


# ─────────────────────────────────────────────────────────────
# Header
# ─────────────────────────────────────────────────────────────

st.markdown("""
<div class="main-header">
    <h1>📊 ML Analytics Dashboard</h1>
    <p>Upload a CSV dataset &bull; Explore &bull; Analyse &bull; Visualise — EDA, PCA, LDA &amp; Factor Analysis</p>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# Sidebar – File upload & settings
# ─────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("## 📁 Upload Dataset")
    uploaded_file = st.file_uploader(
        "Choose a CSV file", type=["csv"], help="Max 200 MB"
    )

    st.markdown("---")
    st.markdown("### ⚙️ Settings")
    max_cat_unique = st.slider(
        "Max unique values for categorical plots",
        5, 50, 20,
        help="Columns with more unique values are skipped in categorical charts.",
    )
    sample_size = st.slider(
        "Pair-plot sample size",
        100, 5000, 1000, step=100,
        help="Large datasets are sampled for pair plots to stay responsive.",
    )

    st.markdown("---")
    st.markdown(
        "<small style='color:#888'>Built with Streamlit &bull; scikit-learn &bull; Plotly</small>",
        unsafe_allow_html=True,
    )

# ─────────────────────────────────────────────────────────────
# Load data
# ─────────────────────────────────────────────────────────────

if uploaded_file is None:
    st.info("👈 **Upload a CSV file** from the sidebar to get started.")
    st.stop()

# Cache the dataframe so it isn't re-read on every interaction
@st.cache_data
def load_csv(file_bytes: bytes) -> pd.DataFrame:
    return pd.read_csv(StringIO(file_bytes.decode("utf-8")))


df = load_csv(uploaded_file.getvalue())
numeric_df = get_numeric_df(df)
cat_df = get_categorical_df(df)

# ─────────────────────────────────────────────────────────────
# Quick metrics
# ─────────────────────────────────────────────────────────────

c1, c2, c3, c4, c5 = st.columns(5)
metrics = [
    ("Rows", f"{df.shape[0]:,}"),
    ("Columns", f"{df.shape[1]}"),
    ("Numeric", f"{numeric_df.shape[1]}"),
    ("Categorical", f"{cat_df.shape[1]}"),
    ("Missing %", f"{(df.isnull().sum().sum() / (df.shape[0]*df.shape[1]) * 100):.1f}%"),
]
for col, (title, value) in zip([c1, c2, c3, c4, c5], metrics):
    col.markdown(
        f'<div class="metric-card"><h3>{title}</h3><p>{value}</p></div>',
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# Main tabs
# ─────────────────────────────────────────────────────────────

tab_eda, tab_pca, tab_lda, tab_fa = st.tabs([
    "🔍 Exploratory Data Analysis",
    "📐 PCA",
    "🎯 LDA",
    "🧩 Factor Analysis",
])

# =============================================================
# TAB 1 — EDA
# =============================================================
with tab_eda:
    st.markdown('<div class="section-header"><h2>Data Preview</h2></div>', unsafe_allow_html=True)
    st.dataframe(df.head(50), width="stretch")

    # ── Data types & info ──
    with st.expander("📋 Column Info & Data Types", expanded=False):
        info_df = pd.DataFrame({
            "Column": df.columns,
            "Type": df.dtypes.astype(str).values,
            "Non-Null Count": df.notnull().sum().values,
            "Null Count": df.isnull().sum().values,
            "Null %": (df.isnull().sum() / len(df) * 100).round(2).values,
            "Unique": df.nunique().values,
        })
        st.dataframe(info_df, width="stretch", hide_index=True)

    # ── Descriptive statistics ──
    st.markdown('<div class="section-header"><h2>Descriptive Statistics</h2></div>', unsafe_allow_html=True)
    desc_tab1, desc_tab2 = st.tabs(["Numeric", "Categorical"])
    with desc_tab1:
        if not numeric_df.empty:
            desc = numeric_df.describe().T
            desc["skew"] = numeric_df.skew()
            desc["kurtosis"] = numeric_df.kurtosis()
            st.dataframe(desc.style.format("{:.3f}"), width="stretch")
        else:
            st.warning("No numeric columns found.")
    with desc_tab2:
        if not cat_df.empty:
            st.dataframe(cat_df.describe().T, width="stretch")
        else:
            st.warning("No categorical columns found.")

    # ── Missing values heatmap ──
    if df.isnull().sum().sum() > 0:
        st.markdown('<div class="section-header"><h2>Missing Values Heatmap</h2></div>', unsafe_allow_html=True)
        fig_miss = px.imshow(
            df.isnull().astype(int).T,
            color_continuous_scale=["#1A1F2E", "#FF6B6B"],
            labels=dict(x="Row Index", y="Column", color="Missing"),
            aspect="auto",
        )
        fig_miss.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=max(300, 20 * len(df.columns)),
        )
        st.plotly_chart(fig_miss, width="stretch")

    # ── Correlation matrix ──
    if not numeric_df.empty and numeric_df.shape[1] > 1:
        st.markdown('<div class="section-header"><h2>Correlation Matrix</h2></div>', unsafe_allow_html=True)
        corr_method = st.radio("Method", ["pearson", "spearman", "kendall"], horizontal=True, key="corr_method")
        corr = numeric_df.corr(method=corr_method)
        fig_corr = px.imshow(
            corr,
            text_auto=".2f",
            color_continuous_scale="RdBu_r",
            zmin=-1, zmax=1,
            aspect="auto",
        )
        fig_corr.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=max(500, 30 * len(corr.columns)),
        )
        st.plotly_chart(fig_corr, width="stretch")

    # ── Distribution plots ──
    if not numeric_df.empty:
        st.markdown('<div class="section-header"><h2>Distribution Plots</h2></div>', unsafe_allow_html=True)
        sel_dist_cols = st.multiselect(
            "Select numeric columns",
            numeric_df.columns.tolist(),
            default=numeric_df.columns[:4].tolist(),
            key="dist_cols",
        )
        if sel_dist_cols:
            n = len(sel_dist_cols)
            cols_per_row = min(n, 3)
            rows = (n + cols_per_row - 1) // cols_per_row
            fig_dist = make_subplots(rows=rows, cols=cols_per_row, subplot_titles=sel_dist_cols)
            for idx, col_name in enumerate(sel_dist_cols):
                r = idx // cols_per_row + 1
                c = idx % cols_per_row + 1
                data = numeric_df[col_name].dropna()
                fig_dist.add_trace(
                    go.Histogram(x=data, name=col_name, marker_color="#6C63FF", opacity=0.8,
                                 nbinsx=40, showlegend=False),
                    row=r, col=c,
                )
            fig_dist.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                height=350 * rows,
            )
            st.plotly_chart(fig_dist, width="stretch")

    # ── Box plots ──
    if not numeric_df.empty:
        st.markdown('<div class="section-header"><h2>Box Plots (Outlier Detection)</h2></div>', unsafe_allow_html=True)
        sel_box_cols = st.multiselect(
            "Select numeric columns",
            numeric_df.columns.tolist(),
            default=numeric_df.columns[:6].tolist(),
            key="box_cols",
        )
        if sel_box_cols:
            box_data = numeric_df[sel_box_cols].melt(var_name="Feature", value_name="Value")
            fig_box = px.box(
                box_data, x="Feature", y="Value", color="Feature",
                color_discrete_sequence=px.colors.qualitative.Prism,
            )
            fig_box.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                showlegend=False,
                height=500,
            )
            st.plotly_chart(fig_box, width="stretch")

    # ── Scatter / pair plot ──
    if not numeric_df.empty and numeric_df.shape[1] >= 2:
        st.markdown('<div class="section-header"><h2>Scatter Matrix</h2></div>', unsafe_allow_html=True)
        pair_cols = st.multiselect(
            "Choose columns (2-6 recommended)",
            numeric_df.columns.tolist(),
            default=numeric_df.columns[:min(4, numeric_df.shape[1])].tolist(),
            key="pair_cols",
        )
        color_col = st.selectbox(
            "Color by (optional)",
            [None] + df.columns.tolist(),
            key="pair_color",
        )
        if len(pair_cols) >= 2:
            sample = df[pair_cols + ([color_col] if color_col else [])].dropna()
            if len(sample) > sample_size:
                sample = sample.sample(sample_size, random_state=42)
            fig_pair = px.scatter_matrix(
                sample,
                dimensions=pair_cols,
                color=color_col,
                color_discrete_sequence=px.colors.qualitative.Vivid,
                opacity=0.6,
            )
            fig_pair.update_traces(diagonal_visible=False, marker=dict(size=3))
            fig_pair.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                height=700,
            )
            st.plotly_chart(fig_pair, width="stretch")

    # ── Categorical bar charts ──
    if not cat_df.empty:
        st.markdown('<div class="section-header"><h2>Categorical Feature Counts</h2></div>', unsafe_allow_html=True)
        valid_cats = [c for c in cat_df.columns if cat_df[c].nunique() <= max_cat_unique]
        if valid_cats:
            sel_cat = st.selectbox("Select categorical column", valid_cats, key="cat_bar")
            vc = df[sel_cat].value_counts().head(30)
            fig_cat = px.bar(
                x=vc.index.astype(str), y=vc.values,
                labels={"x": sel_cat, "y": "Count"},
                color=vc.values,
                color_continuous_scale="Viridis",
            )
            fig_cat.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                height=450,
            )
            st.plotly_chart(fig_cat, width="stretch")
        else:
            st.info("No categorical columns with ≤ {} unique values.".format(max_cat_unique))


# =============================================================
# TAB 2 — PCA
# =============================================================
with tab_pca:
    st.markdown('<div class="section-header"><h2>Principal Component Analysis (PCA)</h2></div>', unsafe_allow_html=True)

    if numeric_df.shape[1] < 2:
        st.error("PCA requires at least 2 numeric columns.")
    else:
        pca_cols = st.multiselect(
            "Select features for PCA",
            numeric_df.columns.tolist(),
            default=numeric_df.columns.tolist(),
            key="pca_features",
        )
        n_components_max = min(len(pca_cols), numeric_df.shape[0]) if pca_cols else 2
        n_components = st.slider(
            "Number of components",
            2, max(2, n_components_max), min(n_components_max, 5),
            key="pca_n",
        )
        pca_color = st.selectbox(
            "Color by (optional label column)",
            [None] + df.columns.tolist(),
            key="pca_color",
        )

        if len(pca_cols) >= 2 and st.button("▶ Run PCA", key="run_pca", type="primary"):
          try:
            imputed = impute_numeric(df[pca_cols])
            scaled, _, col_names = scale_data(imputed)

            pca = PCA(n_components=min(n_components, scaled.shape[1], scaled.shape[0]))
            components = pca.fit_transform(scaled)
            exp_var = pca.explained_variance_ratio_

            st.success(f"Total explained variance ({n_components} components): **{exp_var.sum()*100:.2f}%**")

            # ── Scree plot ──
            st.markdown("#### 📉 Scree Plot (Explained Variance)")
            scree_df = pd.DataFrame({
                "Component": [f"PC{i+1}" for i in range(n_components)],
                "Explained Variance %": exp_var * 100,
                "Cumulative %": np.cumsum(exp_var) * 100,
            })
            fig_scree = go.Figure()
            fig_scree.add_trace(go.Bar(
                x=scree_df["Component"], y=scree_df["Explained Variance %"],
                name="Individual", marker_color="#6C63FF",
            ))
            fig_scree.add_trace(go.Scatter(
                x=scree_df["Component"], y=scree_df["Cumulative %"],
                name="Cumulative", mode="lines+markers",
                marker_color="#FF6B6B", line=dict(width=3),
            ))
            fig_scree.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                yaxis_title="Variance %",
                height=420,
                legend=dict(orientation="h", yanchor="bottom", y=1.02),
            )
            st.plotly_chart(fig_scree, width="stretch")

            # ── 2D scatter ──
            st.markdown("#### 🗺 PCA 2D Projection")
            pc_df = pd.DataFrame(components[:, :2], columns=["PC1", "PC2"])
            if pca_color and pca_color in df.columns:
                pc_df["Label"] = df[pca_color].values
            else:
                pc_df["Label"] = "All"
            fig_2d = px.scatter(
                pc_df, x="PC1", y="PC2", color="Label",
                color_discrete_sequence=px.colors.qualitative.Bold,
                opacity=0.7,
                labels={"PC1": f"PC1 ({exp_var[0]*100:.1f}%)", "PC2": f"PC2 ({exp_var[1]*100:.1f}%)"},
            )
            fig_2d.update_traces(marker=dict(size=6))
            fig_2d.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                height=520,
            )
            st.plotly_chart(fig_2d, width="stretch")

            # ── 3D scatter (if ≥3 components) ──
            if n_components >= 3:
                st.markdown("#### 🌐 PCA 3D Projection")
                pc3_df = pd.DataFrame(components[:, :3], columns=["PC1", "PC2", "PC3"])
                if pca_color and pca_color in df.columns:
                    pc3_df["Label"] = df[pca_color].values
                else:
                    pc3_df["Label"] = "All"
                fig_3d = px.scatter_3d(
                    pc3_df, x="PC1", y="PC2", z="PC3", color="Label",
                    color_discrete_sequence=px.colors.qualitative.Bold,
                    opacity=0.7,
                )
                fig_3d.update_traces(marker=dict(size=3))
                fig_3d.update_layout(
                    template="plotly_dark",
                    paper_bgcolor="rgba(0,0,0,0)",
                    height=600,
                )
                st.plotly_chart(fig_3d, width="stretch")

            # ── Loadings heatmap ──
            st.markdown("#### 🔥 Component Loadings Heatmap")
            loadings = pd.DataFrame(
                pca.components_.T,
                index=col_names,
                columns=[f"PC{i+1}" for i in range(n_components)],
            )
            fig_load = px.imshow(
                loadings,
                text_auto=".2f",
                color_continuous_scale="RdBu_r",
                aspect="auto",
            )
            fig_load.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                height=max(400, 28 * len(col_names)),
            )
            st.plotly_chart(fig_load, width="stretch")

            # ── Biplot ──
            st.markdown("#### 🧭 Biplot (PC1 vs PC2)")
            fig_bi = go.Figure()
            fig_bi.add_trace(go.Scatter(
                x=components[:, 0], y=components[:, 1],
                mode="markers", marker=dict(size=4, opacity=0.5, color="#6C63FF"),
                name="Data Points",
            ))
            coeff = pca.components_[:2, :].T
            scale_factor = max(np.abs(components[:, :2]).max(), 1) * 0.8
            for i, feat in enumerate(col_names):
                fig_bi.add_annotation(
                    ax=0, ay=0,
                    x=coeff[i, 0] * scale_factor,
                    y=coeff[i, 1] * scale_factor,
                    arrowhead=3, arrowwidth=2, arrowcolor="#FF6B6B",
                    text=feat, font=dict(size=11, color="#FF6B6B"),
                    showarrow=True,
                )
            fig_bi.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                xaxis_title=f"PC1 ({exp_var[0]*100:.1f}%)",
                yaxis_title=f"PC2 ({exp_var[1]*100:.1f}%)",
                height=550,
            )
            st.plotly_chart(fig_bi, width="stretch")

            # ── Eigenvalues table ──
            with st.expander("📊 Eigenvalues & Explained Variance Table"):
                n_actual = len(pca.explained_variance_)
                eigen_df = pd.DataFrame({
                    "Component": [f"PC{i+1}" for i in range(n_actual)],
                    "Eigenvalue": pca.explained_variance_,
                    "Variance %": exp_var * 100,
                    "Cumulative %": np.cumsum(exp_var) * 100,
                })
                st.dataframe(eigen_df.style.format({
                    "Eigenvalue": "{:.4f}",
                    "Variance %": "{:.2f}",
                    "Cumulative %": "{:.2f}",
                }), width="stretch", hide_index=True)
          except Exception as e:
            st.error(f"⚠️ PCA failed: {e}")
            st.info("💡 Try removing columns with too many missing/infinite values.")


# =============================================================
# TAB 3 — LDA
# =============================================================
with tab_lda:
    st.markdown('<div class="section-header"><h2>Linear Discriminant Analysis (LDA)</h2></div>', unsafe_allow_html=True)
    st.info("LDA is a **supervised** method — you must select a **categorical target** column.")

    cat_candidates = [c for c in df.columns if df[c].nunique() <= 50 and df[c].nunique() >= 2]
    if not cat_candidates:
        st.error("No suitable categorical target column found (need 2–50 unique values).")
    else:
        lda_target = st.selectbox("Target column (class label)", cat_candidates, key="lda_target")
        lda_features = st.multiselect(
            "Feature columns (numeric)",
            numeric_df.columns.tolist(),
            default=[c for c in numeric_df.columns if c != lda_target],
            key="lda_features",
        )

        if lda_features and st.button("▶ Run LDA", key="run_lda", type="primary"):
          try:
            # Prepare data
            work = df[lda_features + [lda_target]].dropna()
            X = work[lda_features]
            y = work[lda_target]

            le = LabelEncoder()
            y_enc = le.fit_transform(y.astype(str))
            n_classes = len(le.classes_)

            # Impute + scale
            X_imp = impute_numeric(X)
            X_scaled, _, feat_names = scale_data(X_imp)

            n_lda = min(len(lda_features), n_classes - 1)
            if n_lda < 1:
                st.error("Need at least 2 classes and 1 feature.")
            else:
                lda = LinearDiscriminantAnalysis(n_components=n_lda)
                X_lda = lda.fit_transform(X_scaled, y_enc)
                exp_ratio = lda.explained_variance_ratio_

                # Cross-validation accuracy
                cv_scores = cross_val_score(
                    LinearDiscriminantAnalysis(), X_scaled, y_enc, cv=min(5, n_classes), scoring="accuracy"
                )

                c1, c2, c3 = st.columns(3)
                c1.metric("Components", n_lda)
                c2.metric("Classes", n_classes)
                c3.metric("CV Accuracy", f"{cv_scores.mean()*100:.1f}%")

                # ── Explained variance ──
                st.markdown("#### 📉 Explained Variance per Discriminant")
                ev_df = pd.DataFrame({
                    "LD": [f"LD{i+1}" for i in range(n_lda)],
                    "Variance %": exp_ratio * 100,
                })
                fig_ev = px.bar(
                    ev_df, x="LD", y="Variance %",
                    text="Variance %",
                    color="Variance %",
                    color_continuous_scale="Viridis",
                )
                fig_ev.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
                fig_ev.update_layout(
                    template="plotly_dark",
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    height=400,
                )
                st.plotly_chart(fig_ev, width="stretch")

                # ── 2D projection ──
                if n_lda >= 2:
                    st.markdown("#### 🗺 LDA 2D Projection")
                    lda_df = pd.DataFrame(X_lda[:, :2], columns=["LD1", "LD2"])
                    lda_df["Class"] = le.inverse_transform(y_enc)
                    fig_lda2 = px.scatter(
                        lda_df, x="LD1", y="LD2", color="Class",
                        color_discrete_sequence=px.colors.qualitative.Bold,
                        opacity=0.75,
                        labels={
                            "LD1": f"LD1 ({exp_ratio[0]*100:.1f}%)",
                            "LD2": f"LD2 ({exp_ratio[1]*100:.1f}%)",
                        },
                    )
                    fig_lda2.update_traces(marker=dict(size=6))
                    fig_lda2.update_layout(
                        template="plotly_dark",
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)",
                        height=520,
                    )
                    st.plotly_chart(fig_lda2, width="stretch")
                elif n_lda == 1:
                    st.markdown("#### 📊 LDA 1D Projection")
                    lda1_df = pd.DataFrame({"LD1": X_lda[:, 0], "Class": le.inverse_transform(y_enc)})
                    fig_lda1 = px.histogram(
                        lda1_df, x="LD1", color="Class",
                        barmode="overlay", opacity=0.7,
                        color_discrete_sequence=px.colors.qualitative.Bold,
                    )
                    fig_lda1.update_layout(
                        template="plotly_dark",
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)",
                        height=420,
                    )
                    st.plotly_chart(fig_lda1, width="stretch")

                # ── Coefficients ──
                st.markdown("#### 🔥 LDA Coefficients Heatmap")
                coef_df = pd.DataFrame(
                    lda.scalings_[:, :n_lda],
                    index=feat_names,
                    columns=[f"LD{i+1}" for i in range(n_lda)],
                )
                fig_coef = px.imshow(
                    coef_df,
                    text_auto=".2f",
                    color_continuous_scale="RdBu_r",
                    aspect="auto",
                )
                fig_coef.update_layout(
                    template="plotly_dark",
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    height=max(350, 28 * len(feat_names)),
                )
                st.plotly_chart(fig_coef, width="stretch")

                # ── Class means ──
                with st.expander("📊 Class Means Table"):
                    means_df = pd.DataFrame(
                        lda.means_,
                        index=le.classes_,
                        columns=feat_names,
                    )
                    st.dataframe(means_df.style.format("{:.4f}"), width="stretch")
          except Exception as e:
            st.error(f"⚠️ LDA failed: {e}")
            st.info("💡 Ensure you have valid numeric features and a categorical target.")


# =============================================================
# TAB 4 — Factor Analysis
# =============================================================
with tab_fa:
    st.markdown('<div class="section-header"><h2>Factor Analysis (FA)</h2></div>', unsafe_allow_html=True)

    if numeric_df.shape[1] < 2:
        st.error("Factor Analysis requires at least 2 numeric columns.")
    else:
        fa_cols = st.multiselect(
            "Select features for FA",
            numeric_df.columns.tolist(),
            default=numeric_df.columns.tolist(),
            key="fa_features",
        )
        fa_n = st.slider(
            "Number of factors",
            1, max(1, len(fa_cols) - 1) if fa_cols else 1,
            min(3, max(1, len(fa_cols) - 1)) if fa_cols else 1,
            key="fa_n",
        )
        fa_rotation = st.selectbox(
            "Rotation method",
            ["varimax", "quartimax", None],
            index=0,
            key="fa_rotation",
        )

        if len(fa_cols) >= 2 and st.button("▶ Run Factor Analysis", key="run_fa", type="primary"):
          try:
            fa_imputed = impute_numeric(df[fa_cols])
            fa_scaled, _, fa_feat_names = scale_data(fa_imputed)

            fa = FactorAnalysis(n_components=fa_n, rotation=fa_rotation, random_state=42)
            fa_scores = fa.fit_transform(fa_scaled)

            loadings_mat = fa.components_.T  # shape (features, factors)
            communalities = np.sum(loadings_mat ** 2, axis=1)
            noise_var = fa.noise_variance_

            st.success(f"Factor Analysis completed — {fa_n} factor(s) extracted.")

            # ── Factor loadings heatmap ──
            st.markdown("#### 🔥 Factor Loadings")
            load_df = pd.DataFrame(
                loadings_mat,
                index=fa_feat_names,
                columns=[f"Factor {i+1}" for i in range(fa_n)],
            )
            fig_fl = px.imshow(
                load_df,
                text_auto=".2f",
                color_continuous_scale="RdBu_r",
                zmin=-1, zmax=1,
                aspect="auto",
            )
            fig_fl.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                height=max(400, 30 * len(fa_feat_names)),
            )
            st.plotly_chart(fig_fl, width="stretch")

            # ── Communalities ──
            st.markdown("#### 📊 Communalities")
            comm_df = pd.DataFrame({
                "Feature": fa_feat_names,
                "Communality": communalities,
                "Specific Variance": noise_var,
            }).sort_values("Communality", ascending=True)
            fig_comm = px.bar(
                comm_df, y="Feature", x="Communality",
                orientation="h",
                color="Communality",
                color_continuous_scale="Viridis",
            )
            fig_comm.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                height=max(350, 28 * len(fa_feat_names)),
            )
            st.plotly_chart(fig_comm, width="stretch")

            # ── Scree plot (eigenvalues of correlation matrix) ──
            st.markdown("#### 📉 Scree Plot (Eigenvalues of Correlation Matrix)")
            corr_for_eigen = np.corrcoef(fa_scaled.T)
            eigenvalues = np.linalg.eigvalsh(corr_for_eigen)[::-1]
            scree_fa_df = pd.DataFrame({
                "Component": [f"C{i+1}" for i in range(len(eigenvalues))],
                "Eigenvalue": eigenvalues,
            })
            fig_scree_fa = go.Figure()
            fig_scree_fa.add_trace(go.Scatter(
                x=scree_fa_df["Component"], y=scree_fa_df["Eigenvalue"],
                mode="lines+markers",
                marker=dict(size=10, color="#6C63FF"),
                line=dict(width=3, color="#6C63FF"),
                name="Eigenvalue",
            ))
            fig_scree_fa.add_hline(y=1, line_dash="dash", line_color="#FF6B6B",
                                   annotation_text="Kaiser Criterion (λ = 1)")
            fig_scree_fa.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                yaxis_title="Eigenvalue",
                height=420,
            )
            st.plotly_chart(fig_scree_fa, width="stretch")

            # ── Factor scores 2D ──
            if fa_n >= 2:
                st.markdown("#### 🗺 Factor Scores (2D)")
                fa_color = st.selectbox(
                    "Color by (optional)",
                    [None] + df.columns.tolist(),
                    key="fa_color",
                )
                fs_df = pd.DataFrame(fa_scores[:, :2], columns=["Factor 1", "Factor 2"])
                if fa_color and fa_color in df.columns:
                    fs_df["Label"] = df[fa_color].values
                else:
                    fs_df["Label"] = "All"
                fig_fs = px.scatter(
                    fs_df, x="Factor 1", y="Factor 2", color="Label",
                    color_discrete_sequence=px.colors.qualitative.Bold,
                    opacity=0.7,
                )
                fig_fs.update_traces(marker=dict(size=5))
                fig_fs.update_layout(
                    template="plotly_dark",
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    height=520,
                )
                st.plotly_chart(fig_fs, width="stretch")

            # ── Tables ──
            with st.expander("📋 Factor Loadings Table"):
                styled_load = load_df.style.format("{:.4f}").background_gradient(
                    cmap="RdBu_r", vmin=-1, vmax=1, axis=None
                )
                st.dataframe(styled_load, width="stretch")

            with st.expander("📋 Communalities & Specific Variance Table"):
                full_comm = pd.DataFrame({
                    "Feature": fa_feat_names,
                    "Communality": communalities,
                    "Specific Variance": noise_var,
                })
                st.dataframe(
                    full_comm.style.format({"Communality": "{:.4f}", "Specific Variance": "{:.4f}"}),
                    width="stretch",
                    hide_index=True,
                )
          except Exception as e:
            st.error(f"⚠️ Factor Analysis failed: {e}")
            st.info("💡 Try removing columns with too many missing/infinite values.")

