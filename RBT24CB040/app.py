"""
app.py
------
DAVL — Data Analysis & Visualization Lab
Main Streamlit application entry point.
"""

import streamlit as st
import pandas as pd
import numpy as np

# ── Page config (must be first Streamlit call) ────────────────────────────────
st.set_page_config(
    page_title="DAVL — Data Analysis Lab",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Global ─────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Dark gradient background */
.stApp {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    background-attachment: fixed;
}

/* ── Sidebar ─────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: rgba(15, 12, 41, 0.85);
    backdrop-filter: blur(12px);
    border-right: 1px solid rgba(255,255,255,0.08);
}

/* ── Metrics ─────────────────────────────────────────── */
[data-testid="stMetric"] {
    background: rgba(99, 102, 241, 0.12);
    border: 1px solid rgba(99, 102, 241, 0.3);
    border-radius: 12px;
    padding: 12px 16px;
    backdrop-filter: blur(6px);
}
[data-testid="stMetricValue"] { color: #a5b4fc !important; font-weight: 700; }
[data-testid="stMetricLabel"] { color: #94a3b8 !important; }

/* ── Tabs ─────────────────────────────────────────────── */
[data-baseweb="tab-list"] {
    background: rgba(15, 12, 41, 0.6) !important;
    border-radius: 12px;
    padding: 4px;
    gap: 4px;
    border: 1px solid rgba(255,255,255,0.07);
}
[data-baseweb="tab"] {
    border-radius: 8px !important;
    color: #94a3b8 !important;
    font-weight: 500;
    transition: all 0.2s;
}
[aria-selected="true"][data-baseweb="tab"] {
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
    color: white !important;
}

/* ── DataFrames ──────────────────────────────────────── */
[data-testid="stDataFrame"] {
    border-radius: 10px;
    overflow: hidden;
    border: 1px solid rgba(255,255,255,0.08);
}

/* ── Buttons ─────────────────────────────────────────── */
.stDownloadButton > button, .stButton > button {
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    transition: all 0.2s !important;
}
.stDownloadButton > button:hover, .stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 20px rgba(99,102,241,0.4) !important;
}

/* ── Expanders ───────────────────────────────────────── */
[data-testid="stExpander"] {
    background: rgba(99, 102, 241, 0.06);
    border: 1px solid rgba(99,102,241,0.2);
    border-radius: 10px;
}

/* ── File uploader ───────────────────────────────────── */
[data-testid="stFileUploader"] {
    background: rgba(99, 102, 241, 0.08);
    border: 2px dashed rgba(99, 102, 241, 0.4);
    border-radius: 14px;
    padding: 16px;
    transition: border-color 0.2s;
}

/* ── Info/Warning boxes ──────────────────────────────── */
.stAlert {
    border-radius: 10px;
    border-left-width: 4px;
}

/* ── Section dividers ────────────────────────────────── */
hr { border-color: rgba(99,102,241,0.2) !important; }
</style>
""", unsafe_allow_html=True)

# ── Module imports ────────────────────────────────────────────────────────────
from modules.data_loader import load_dataset, show_preview, get_csv_download
from modules.overview import show_overview
from modules.quality import show_quality, get_quality_summary
from modules.preprocessing import show_preprocessing
from modules.eda import show_eda
from modules.visualizations import show_visualizations
from modules.statistics import show_statistics
from modules.pca_analysis import show_pca
from modules.lda_analysis import show_lda
from modules.factor_analysis import show_factor_analysis
from modules.insights import show_insights


# ═══════════════════════════════════════════════════════════════════════════════
#  SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 16px 0;'>
        <div style='font-size:40px;'>🔬</div>
        <h2 style='color:#a5b4fc; margin:8px 0 4px;'>DAVL</h2>
        <p style='color:#64748b; font-size:0.82rem; margin:0;'>
            Data Analysis & Visualization Lab
        </p>
    </div>
    <hr style='margin:12px 0;'/>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "📂 Upload Dataset",
        type=["csv", "xlsx", "xls"],
        help="Upload a CSV or Excel file to begin full analysis.",
    )

    st.markdown("<hr/>", unsafe_allow_html=True)
    st.markdown("""
    <div style='color:#64748b; font-size:0.78rem; line-height:1.6;'>
    <b style='color:#a5b4fc;'>Supported Formats</b><br>
    CSV · Excel (.xlsx, .xls)<br><br>
    <b style='color:#a5b4fc;'>Analysis Modules</b><br>
    Overview · Quality · Preprocessing<br>
    EDA · Visualizations · Statistics<br>
    PCA · LDA · Factor Analysis · Insights
    </div>
    """, unsafe_allow_html=True)

    if "df_processed" in st.session_state and st.session_state.df_processed is not None:
        st.markdown("<hr/>", unsafe_allow_html=True)
        st.markdown("**⬇️ Download Processed Dataset**")
        csv_bytes = get_csv_download(st.session_state.df_processed)
        st.download_button(
            "Download CSV",
            data=csv_bytes,
            file_name="processed_dataset.csv",
            mime="text/csv",
            use_container_width=True,
        )


# ═══════════════════════════════════════════════════════════════════════════════
#  MAIN CONTENT
# ═══════════════════════════════════════════════════════════════════════════════

# ── Hero header ───────────────────────────────────────────────────────────────
st.markdown("""
<div style='text-align:center; padding: 32px 0 16px;'>
    <h1 style='
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #6366f1, #a78bfa, #38bdf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 8px;
    '>
        🔬 DAVL — Data Analysis & Visualization Lab
    </h1>
    <p style='color:#94a3b8; font-size:1.05rem; max-width:640px; margin:0 auto;'>
        Upload your dataset and instantly get comprehensive analysis, beautiful
        visualizations, and actionable insights — powered by Python.
    </p>
</div>
""", unsafe_allow_html=True)


# ── No file uploaded ──────────────────────────────────────────────────────────
if uploaded_file is None:
    st.markdown("<br>", unsafe_allow_html=True)

    # Feature cards
    cols = st.columns(4)
    features = [
        ("📋", "Smart Overview", "Shape, dtypes, memory, target detection"),
        ("🔍", "Quality Analysis", "Missing values, outliers, imbalance"),
        ("📊", "EDA & Charts", "Interactive Plotly visualizations"),
        ("🧮", "PCA / LDA / FA", "Dimensionality reduction insights"),
    ]
    for col, (icon, title, desc) in zip(cols, features):
        col.markdown(f"""
        <div style='
            background: rgba(99,102,241,0.08);
            border: 1px solid rgba(99,102,241,0.25);
            border-radius: 14px;
            padding: 20px 16px;
            text-align: center;
            height: 140px;
        '>
            <div style='font-size:2rem; margin-bottom:8px;'>{icon}</div>
            <b style='color:#a5b4fc;'>{title}</b>
            <p style='color:#64748b; font-size:0.8rem; margin-top:6px;'>{desc}</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    cols2 = st.columns(4)
    features2 = [
        ("⚙️", "Preprocessing", "Impute, encode, scale, cap outliers"),
        ("📐", "Statistics", "Descriptive stats, skew, kurtosis"),
        ("💡", "Auto Insights", "AI-generated observations & fixes"),
        ("⬇️", "Export All", "Download datasets, plots, reports"),
    ]
    for col, (icon, title, desc) in zip(cols2, features2):
        col.markdown(f"""
        <div style='
            background: rgba(139,92,246,0.08);
            border: 1px solid rgba(139,92,246,0.25);
            border-radius: 14px;
            padding: 20px 16px;
            text-align: center;
            height: 140px;
        '>
            <div style='font-size:2rem; margin-bottom:8px;'>{icon}</div>
            <b style='color:#c084fc;'>{title}</b>
            <p style='color:#64748b; font-size:0.8rem; margin-top:6px;'>{desc}</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div style='text-align:center; margin-top:40px; color:#475569;'>
        ⬆️ Upload a <b>CSV or Excel</b> file from the sidebar to begin
    </div>
    """, unsafe_allow_html=True)
    st.stop()


# ── Load dataset ──────────────────────────────────────────────────────────────
df = load_dataset(uploaded_file)
if df is None:
    st.stop()

# Store in session state for cross-tab access
if "df_raw" not in st.session_state or st.session_state.get("uploaded_name") != uploaded_file.name:
    st.session_state["df_raw"] = df
    st.session_state["uploaded_name"] = uploaded_file.name
    st.session_state["df_processed"] = None
    st.session_state["target_col"] = None

df = st.session_state["df_raw"]

# ── Dataset preview ───────────────────────────────────────────────────────────
show_preview(df)
st.markdown("---")

# ═══════════════════════════════════════════════════════════════════════════════
#  ANALYSIS TABS
# ═══════════════════════════════════════════════════════════════════════════════

tabs = st.tabs([
    "🗂️ Overview",
    "🔍 Quality",
    "⚙️ Preprocessing",
    "🔭 EDA",
    "📊 Visualizations",
    "📐 Statistics",
    "🔬 PCA",
    "📏 LDA",
    "🔮 Factor Analysis",
    "💡 Insights",
])

# ── Tab 1: Overview ───────────────────────────────────────────────────────────
with tabs[0]:
    detected_target = show_overview(df)
    if detected_target:
        st.session_state["target_col"] = detected_target

    # Allow manual override
    all_cols = ["(None)"] + df.columns.tolist()
    default_idx = (all_cols.index(st.session_state["target_col"])
                   if st.session_state["target_col"] in all_cols else 0)
    manual_target = st.selectbox(
        "🎯 Override Target Column (optional)",
        all_cols,
        index=default_idx,
        key="manual_target_select",
    )
    if manual_target != "(None)":
        st.session_state["target_col"] = manual_target
    elif manual_target == "(None)":
        st.session_state["target_col"] = None

target = st.session_state.get("target_col")

# ── Tab 2: Quality ────────────────────────────────────────────────────────────
with tabs[1]:
    quality_summary = get_quality_summary(df)
    show_quality(df, target=target)

# ── Tab 3: Preprocessing ──────────────────────────────────────────────────────
with tabs[2]:
    processed_df = show_preprocessing(df, target=target)
    st.session_state["df_processed"] = processed_df

# ── Tab 4: EDA ────────────────────────────────────────────────────────────────
with tabs[3]:
    show_eda(df, target=target)

# ── Tab 5: Visualizations ─────────────────────────────────────────────────────
with tabs[4]:
    show_visualizations(df, target=target)

# ── Tab 6: Statistics ─────────────────────────────────────────────────────────
with tabs[5]:
    show_statistics(df)

# ── Tab 7: PCA ────────────────────────────────────────────────────────────────
with tabs[6]:
    show_pca(df, target=target)

# ── Tab 8: LDA ────────────────────────────────────────────────────────────────
with tabs[7]:
    show_lda(df, target=target)

# ── Tab 9: Factor Analysis ────────────────────────────────────────────────────
with tabs[8]:
    show_factor_analysis(df)

# ── Tab 10: Insights ──────────────────────────────────────────────────────────
with tabs[9]:
    show_insights(df, target=target, quality_summary=quality_summary)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style='text-align:center; color:#334155; font-size:0.8rem; padding:16px 0;'>
    🔬 DAVL — Data Analysis & Visualization Lab &nbsp;|&nbsp;
    Built with Streamlit, Plotly, scikit-learn, and ❤️
</div>
""", unsafe_allow_html=True)
