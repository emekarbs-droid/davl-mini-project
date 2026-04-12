"""
app.py — Main Streamlit Application (Single Scrollable Page)
Netflix vs Amazon Prime EDA Dashboard
"""
import os
import streamlit as st
import pandas as pd

from utils.data_loader import load_csv, load_uploaded, detect_target, get_column_types, engineer_features
from utils.overview import show_overview
from utils.quality import show_missing_values, show_duplicates, show_outliers, show_class_imbalance
from utils.preprocessing import show_preprocessing
from utils.eda import show_univariate, show_bivariate, show_multivariate, show_correlation
from utils.visualization import show_visualization
from utils.stats import show_descriptive_stats, show_shapiro_test, show_stat_matrices
from utils.pca_analysis import show_pca
from utils.lda_analysis import show_lda
from utils.factor_analysis import show_factor_analysis
from utils.insights import generate_insights
from utils.comparison import show_comparison

# ── Page Config ──
st.set_page_config(
    page_title="EDA — Netflix vs Amazon Prime",
    page_icon="📊",
    layout="wide",
)

# ── Title ──
st.title("📊 Data Analysis & Visualization Lab")
st.caption("Netflix vs Amazon Prime — Exploratory Data Analysis")

# ── Sidebar — Minimal controls only ──
st.sidebar.title("⚙️ Settings")

data_source = st.sidebar.radio("📁 Data Source", ["Default (Netflix & Amazon)", "Upload CSV/Excel"])

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, "data")

if data_source == "Default (Netflix & Amazon)":
    df_a_raw = load_csv(os.path.join(DATA, "netflix_titles.csv"))
    df_b_raw = load_csv(os.path.join(DATA, "amazon_prime_titles.csv"))
    name_a, name_b = "Netflix", "Amazon Prime"
else:
    file_a = st.sidebar.file_uploader("Upload Dataset A", type=["csv", "xlsx"], key="file_a")
    file_b = st.sidebar.file_uploader("Upload Dataset B", type=["csv", "xlsx"], key="file_b")
    if file_a is None or file_b is None:
        st.info("⬅️ Please upload both datasets from the sidebar.")
        st.stop()
    df_a_raw = load_uploaded(file_a)
    df_b_raw = load_uploaded(file_b)
    name_a = file_a.name.rsplit(".", 1)[0]
    name_b = file_b.name.rsplit(".", 1)[0]
    if df_a_raw is None or df_b_raw is None:
        st.stop()

# Engineer features for richer analysis
df_a = engineer_features(df_a_raw.copy())
df_b = engineer_features(df_b_raw.copy())

target_a = detect_target(df_a)
target_b = detect_target(df_b)

st.sidebar.markdown("---")
st.sidebar.info(f"**{name_a}**: {df_a.shape[0]:,} × {df_a.shape[1]}  \n"
                f"**{name_b}**: {df_b.shape[0]:,} × {df_b.shape[1]}")

# ═══════════════════════════════════════════════════════
#  ALL SECTIONS ON ONE SCROLLABLE PAGE
# ═══════════════════════════════════════════════════════

# ────────────── 1. OVERVIEW ──────────────
st.markdown("---")
st.header("1️⃣ Dataset Overview")
tab_ov1, tab_ov2 = st.tabs([f"📕 {name_a}", f"📘 {name_b}"])
with tab_ov1:
    show_overview(df_a_raw, name_a)
with tab_ov2:
    show_overview(df_b_raw, name_b)

# ────────────── 2. DATA QUALITY ──────────────
st.markdown("---")
st.header("2️⃣ Data Quality Analysis")
tab_q1, tab_q2 = st.tabs([f"📕 {name_a}", f"📘 {name_b}"])
with tab_q1:
    show_missing_values(df_a_raw, name_a)
    show_duplicates(df_a_raw, name_a)
    show_outliers(df_a_raw, name_a)
    show_class_imbalance(df_a_raw, target_a, name_a)
with tab_q2:
    show_missing_values(df_b_raw, name_b)
    show_duplicates(df_b_raw, name_b)
    show_outliers(df_b_raw, name_b)
    show_class_imbalance(df_b_raw, target_b, name_b)

# ────────────── 3. PREPROCESSING ──────────────
st.markdown("---")
st.header("3️⃣ Preprocessing Pipeline")
tab_p1, tab_p2 = st.tabs([f"📕 {name_a}", f"📘 {name_b}"])
with tab_p1:
    df_a_proc = show_preprocessing(df_a, name_a)
with tab_p2:
    df_b_proc = show_preprocessing(df_b, name_b)

# ────────────── 4. DESCRIPTIVE STATISTICS ──────────────
st.markdown("---")
st.header("4️⃣ Descriptive Statistics")
tab_s1, tab_s2 = st.tabs([f"📕 {name_a}", f"📘 {name_b}"])
with tab_s1:
    show_descriptive_stats(df_a, name_a)
with tab_s2:
    show_descriptive_stats(df_b, name_b)

# ────────────── 5. UNIVARIATE EDA ──────────────
st.markdown("---")
st.header("5️⃣ Univariate Analysis")
tab_u1, tab_u2 = st.tabs([f"📕 {name_a}", f"📘 {name_b}"])
with tab_u1:
    show_univariate(df_a, name_a)
with tab_u2:
    show_univariate(df_b, name_b)

# ────────────── 6. BIVARIATE EDA ──────────────
st.markdown("---")
st.header("6️⃣ Bivariate Analysis")
tab_bi1, tab_bi2 = st.tabs([f"📕 {name_a}", f"📘 {name_b}"])
with tab_bi1:
    show_bivariate(df_a, name_a)
with tab_bi2:
    show_bivariate(df_b, name_b)

# ────────────── 7. VISUALIZATIONS ──────────────
st.markdown("---")
st.header("7️⃣ Visualizations")
tab_v1, tab_v2 = st.tabs([f"📕 {name_a}", f"📘 {name_b}"])
with tab_v1:
    show_visualization(df_a, name_a)
with tab_v2:
    show_visualization(df_b, name_b)

# ────────────── 8. CORRELATION ──────────────
st.markdown("---")
st.header("8️⃣ Correlation Analysis")
tab_c1, tab_c2 = st.tabs([f"📕 {name_a}", f"📘 {name_b}"])
with tab_c1:
    show_correlation(df_a, name_a)
with tab_c2:
    show_correlation(df_b, name_b)

# ────────────── 9. NORMALITY TEST ──────────────
st.markdown("---")
st.header("9️⃣ Normality Tests & Stat Matrices")
tab_n1, tab_n2 = st.tabs([f"📕 {name_a}", f"📘 {name_b}"])
with tab_n1:
    show_shapiro_test(df_a, name_a)
    show_stat_matrices(df_a, name_a)
with tab_n2:
    show_shapiro_test(df_b, name_b)
    show_stat_matrices(df_b, name_b)

# ────────────── 10. MULTIVARIATE ──────────────
st.markdown("---")
st.header("🔟 Multivariate Analysis")
tab_m1, tab_m2 = st.tabs([f"📕 {name_a}", f"📘 {name_b}"])
with tab_m1:
    show_multivariate(df_a, name_a)
with tab_m2:
    show_multivariate(df_b, name_b)

# ────────────── 11. PCA ──────────────
st.markdown("---")
st.header("1️⃣1️⃣ PCA (Principal Component Analysis)")
tab_pca1, tab_pca2 = st.tabs([f"📕 {name_a}", f"📘 {name_b}"])
with tab_pca1:
    show_pca(df_a, name_a)
with tab_pca2:
    show_pca(df_b, name_b)

# ────────────── 12. LDA ──────────────
st.markdown("---")
st.header("1️⃣2️⃣ LDA (Linear Discriminant Analysis)")
tab_lda1, tab_lda2 = st.tabs([f"📕 {name_a}", f"📘 {name_b}"])
with tab_lda1:
    show_lda(df_a, name_a)
with tab_lda2:
    show_lda(df_b, name_b)

# ────────────── 13. FACTOR ANALYSIS ──────────────
st.markdown("---")
st.header("1️⃣3️⃣ Factor Analysis")
tab_fa1, tab_fa2 = st.tabs([f"📕 {name_a}", f"📘 {name_b}"])
with tab_fa1:
    show_factor_analysis(df_a, name_a)
with tab_fa2:
    show_factor_analysis(df_b, name_b)

# ────────────── 14. INSIGHTS ──────────────
st.markdown("---")
st.header("1️⃣4️⃣ Insights")
col_i1, col_i2 = st.columns(2)
with col_i1:
    generate_insights(df_a_raw, name_a)
with col_i2:
    generate_insights(df_b_raw, name_b)

# ────────────── 15. COMPARISON ──────────────
st.markdown("---")
st.header("1️⃣5️⃣ Dataset Comparison")
show_comparison(df_a_raw, df_b_raw, name_a, name_b)

# ────────────── FOOTER ──────────────
st.markdown("---")
st.caption("Built with Streamlit · Pandas · Plotly · Scikit-learn · Scipy")
