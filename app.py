import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.decomposition import PCA
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import (mean_squared_error, r2_score, accuracy_score,
                             confusion_matrix, roc_curve, auc, mean_absolute_error)

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Prism ML",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────────────────────────────────────
# CSS  — full redesign
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@200;300;400;500;600;700&family=JetBrains+Mono:wght@300;400;500&display=swap');

/* ── TOKENS ── */
:root {
  --bg:       #06060f;
  --bg2:      #0c0c1e;
  --glass:    rgba(193,191,255,.04);
  --glass2:   rgba(193,191,255,.08);
  --border:   rgba(193,191,255,.12);
  --border2:  rgba(193,191,255,.22);
  --prism:    #C1BFFF;
  --prism2:   #9b96ff;
  --prism3:   #7b6fff;
  --rose:     #ff8fab;
  --teal:     #5efce8;
  --amber:    #ffd97d;
  --green:    #72efdd;
  --text:     #eeeeff;
  --muted:    rgba(193,191,255,.45);
  --mono:     'JetBrains Mono', monospace;
  --sans:     'Outfit', sans-serif;
}

/* ── RESET / BASE ── */
*, *::before, *::after { box-sizing: border-box; }

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewContainer"] > .main {
  background: var(--bg) !important;
  color: var(--text) !important;
  font-family: var(--sans) !important;
}

/* animated mesh background */
[data-testid="stAppViewContainer"]::before {
  content: '';
  position: fixed; inset: 0; z-index: 0; pointer-events: none;
  background:
    radial-gradient(ellipse 80% 50% at 20% 10%, rgba(193,191,255,.06) 0%, transparent 60%),
    radial-gradient(ellipse 60% 40% at 80% 80%, rgba(94,252,232,.04) 0%, transparent 55%),
    radial-gradient(ellipse 50% 60% at 50% 50%, rgba(255,143,171,.03) 0%, transparent 65%);
}

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
  background: var(--bg2) !important;
  border-right: 1px solid var(--border) !important;
  backdrop-filter: blur(20px);
}
[data-testid="stSidebar"] > div { padding-top: 0 !important; }

/* ── BRAND ── */
.brand {
  padding: 2rem 1.5rem 1.2rem;
  border-bottom: 1px solid var(--border);
  margin-bottom: 1rem;
}
.brand-logo {
  font-family: var(--mono);
  font-size: .65rem;
  color: var(--muted);
  letter-spacing: .3em;
  text-transform: uppercase;
  margin-bottom: .5rem;
}
.brand-title {
  font-size: 1.6rem;
  font-weight: 700;
  letter-spacing: -.02em;
  background: linear-gradient(135deg, var(--prism) 0%, var(--teal) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  line-height: 1;
}
.brand-sub {
  font-size: .72rem;
  color: var(--muted);
  margin-top: .3rem;
  font-weight: 300;
}

/* ── NAV PILLS (replace tabs) ── */
.nav-section {
  font-family: var(--mono);
  font-size: .6rem;
  color: var(--muted);
  letter-spacing: .2em;
  text-transform: uppercase;
  padding: .8rem 1.5rem .3rem;
}
.nav-pill {
  display: flex;
  align-items: center;
  gap: .65rem;
  padding: .55rem 1.5rem;
  margin: .1rem .75rem;
  border-radius: 10px;
  cursor: pointer;
  color: var(--muted);
  font-size: .83rem;
  font-weight: 400;
  transition: all .2s cubic-bezier(.4,0,.2,1);
  border: 1px solid transparent;
  position: relative;
}
.nav-pill:hover {
  background: var(--glass2);
  color: var(--prism);
  border-color: var(--border);
}
.nav-pill.active {
  background: linear-gradient(135deg, rgba(193,191,255,.15), rgba(94,252,232,.08));
  color: var(--prism);
  border-color: var(--border2);
  font-weight: 500;
}
.nav-pill.active::before {
  content: '';
  position: absolute;
  left: -1px; top: 25%; height: 50%;
  width: 3px;
  background: linear-gradient(180deg, var(--prism), var(--teal));
  border-radius: 0 3px 3px 0;
}
.nav-icon {
  font-size: 1rem;
  width: 1.2rem;
  text-align: center;
  flex-shrink: 0;
}
.nav-divider {
  height: 1px;
  background: var(--border);
  margin: .6rem 1.5rem;
}

/* ── PAGE HEADER ── */
.page-header {
  margin-bottom: 2rem;
}
.page-eyebrow {
  font-family: var(--mono);
  font-size: .65rem;
  color: var(--muted);
  letter-spacing: .25em;
  text-transform: uppercase;
  margin-bottom: .4rem;
}
.page-title {
  font-size: 2rem;
  font-weight: 700;
  letter-spacing: -.03em;
  background: linear-gradient(135deg, var(--text) 30%, var(--prism));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  line-height: 1.1;
}
.page-desc {
  font-size: .9rem;
  color: var(--muted);
  margin-top: .5rem;
  font-weight: 300;
}

/* ── GLASS CARDS ── */
.glass-card {
  background: var(--glass);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 1.5rem;
  position: relative;
  overflow: hidden;
  backdrop-filter: blur(12px);
}
.glass-card::after {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(193,191,255,.04) 0%, transparent 60%);
  pointer-events: none;
}

/* ── METRIC CARDS ── */
.metric-grid { display: flex; gap: .75rem; flex-wrap: wrap; margin: 1rem 0; }
.m-card {
  flex: 1; min-width: 120px;
  background: var(--glass);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 1.1rem 1.25rem;
  position: relative;
  overflow: hidden;
  transition: border-color .2s, transform .2s;
}
.m-card:hover {
  border-color: var(--border2);
  transform: translateY(-2px);
}
.m-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 2px;
  background: linear-gradient(90deg, var(--prism), var(--teal));
  opacity: .6;
}
.m-card.rose::before  { background: linear-gradient(90deg, var(--rose), var(--amber)); }
.m-card.teal::before  { background: linear-gradient(90deg, var(--teal), var(--green)); }
.m-card.amber::before { background: linear-gradient(90deg, var(--amber), var(--rose)); }
.m-label {
  font-family: var(--mono);
  font-size: .58rem;
  color: var(--muted);
  letter-spacing: .15em;
  text-transform: uppercase;
  margin-bottom: .4rem;
}
.m-value {
  font-family: var(--mono);
  font-size: 1.5rem;
  font-weight: 500;
  color: var(--text);
  line-height: 1;
}
.m-sub {
  font-size: .7rem;
  color: var(--muted);
  margin-top: .3rem;
}

/* ── SECTION LABEL ── */
.s-label {
  font-family: var(--mono);
  font-size: .65rem;
  color: var(--prism);
  letter-spacing: .2em;
  text-transform: uppercase;
  padding-bottom: .6rem;
  border-bottom: 1px solid var(--border);
  margin: 1.5rem 0 1rem;
}

/* ── PILL TABS (inner sub-navigation) ── */
.pill-tabs {
  display: flex;
  gap: .4rem;
  background: rgba(193,191,255,.05);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: .3rem;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
}
.pill-tab {
  padding: .45rem 1.1rem;
  border-radius: 9px;
  font-size: .8rem;
  font-weight: 500;
  cursor: pointer;
  color: var(--muted);
  transition: all .18s;
  white-space: nowrap;
}
.pill-tab.on {
  background: linear-gradient(135deg, rgba(193,191,255,.25), rgba(94,252,232,.12));
  color: var(--prism);
  box-shadow: 0 2px 12px rgba(193,191,255,.15);
}

/* ── ALERTS ── */
.al {
  border-radius: 10px;
  padding: .8rem 1.1rem;
  font-size: .83rem;
  margin-bottom: .75rem;
  display: flex; align-items: center; gap: .6rem;
}
.al-info  { background: rgba(193,191,255,.07); border: 1px solid rgba(193,191,255,.2); color: #d4d3ff; }
.al-warn  { background: rgba(255,217,125,.06); border: 1px solid rgba(255,217,125,.2); color: #ffe5a0; }
.al-ok    { background: rgba(94,252,232,.06);  border: 1px solid rgba(94,252,232,.2);  color: #a0fff0; }

/* ── STREAMLIT OVERRIDES ── */

/* radio → hide it (we build our own nav) */
[data-testid="stSidebar"] .stRadio > label { display: none !important; }
[data-testid="stSidebar"] .stRadio > div {
  display: flex; flex-direction: column; gap: 0;
}
[data-testid="stSidebar"] .stRadio > div > label {
  background: transparent !important;
  color: var(--muted) !important;
  border-radius: 10px !important;
  padding: .5rem 1.5rem !important;
  margin: .1rem .75rem !important;
  font-family: var(--sans) !important;
  font-size: .83rem !important;
  transition: all .2s !important;
  border: 1px solid transparent !important;
}
[data-testid="stSidebar"] .stRadio > div > label:hover {
  background: rgba(193,191,255,.08) !important;
  color: var(--prism) !important;
  border-color: var(--border) !important;
}
[data-testid="stSidebar"] .stRadio [data-baseweb="radio"] { display: none !important; }
[data-testid="stSidebar"] .stRadio [aria-checked="true"] ~ span,
[data-testid="stSidebar"] .stRadio label[data-selected="true"] {
  background: linear-gradient(135deg, rgba(193,191,255,.15), rgba(94,252,232,.08)) !important;
  color: var(--prism) !important;
  border-color: rgba(193,191,255,.22) !important;
}

/* dataframe */
[data-testid="stDataFrame"] { border-radius: 12px; overflow: hidden; }
[data-testid="stDataFrame"] table {
  background: rgba(12,12,30,.8) !important;
  color: var(--text) !important;
  font-family: var(--mono) !important;
  font-size: .8rem !important;
}
[data-testid="stDataFrame"] th {
  background: rgba(193,191,255,.06) !important;
  color: var(--prism) !important;
  font-size: .72rem !important;
  letter-spacing: .08em !important;
  border-bottom: 1px solid var(--border) !important;
}
[data-testid="stDataFrame"] tr:hover td {
  background: rgba(193,191,255,.04) !important;
}

/* sliders */
[data-testid="stSlider"] > div > div > div > div {
  background: var(--prism) !important;
}

/* buttons */
.stButton > button {
  background: linear-gradient(135deg, rgba(193,191,255,.2), rgba(94,252,232,.1)) !important;
  color: var(--prism) !important;
  border: 1px solid var(--border2) !important;
  border-radius: 10px !important;
  font-family: var(--mono) !important;
  font-size: .78rem !important;
  font-weight: 500 !important;
  letter-spacing: .05em !important;
  padding: .55rem 1.4rem !important;
  transition: all .2s !important;
  box-shadow: 0 0 20px rgba(193,191,255,.08) !important;
}
.stButton > button:hover {
  background: linear-gradient(135deg, rgba(193,191,255,.3), rgba(94,252,232,.18)) !important;
  box-shadow: 0 0 30px rgba(193,191,255,.18) !important;
  transform: translateY(-1px) !important;
}

/* select / multiselect */
[data-baseweb="select"] {
  background: var(--glass) !important;
  border-color: var(--border) !important;
  border-radius: 10px !important;
}
[data-baseweb="select"] * { color: var(--text) !important; background: var(--bg2) !important; }

/* file uploader */
[data-testid="stFileUploader"] {
  background: var(--glass) !important;
  border: 2px dashed var(--border2) !important;
  border-radius: 16px !important;
  padding: 1rem !important;
}

/* expander */
[data-testid="stExpander"] {
  background: var(--glass) !important;
  border: 1px solid var(--border) !important;
  border-radius: 12px !important;
}
[data-testid="stExpander"] summary {
  color: var(--prism) !important;
  font-family: var(--mono) !important;
  font-size: .82rem !important;
}

/* hide stTabs (we won't use them) — but if we do keep them, style nicely */
[data-testid="stTabs"] [data-baseweb="tab-list"] {
  background: rgba(193,191,255,.05) !important;
  border: 1px solid var(--border) !important;
  border-radius: 12px !important;
  padding: .3rem !important;
  gap: .25rem !important;
}
[data-testid="stTabs"] [data-baseweb="tab"] {
  background: transparent !important;
  color: var(--muted) !important;
  font-family: var(--mono) !important;
  font-size: .75rem !important;
  border-radius: 9px !important;
  padding: .45rem 1rem !important;
  border: none !important;
}
[data-testid="stTabs"] [aria-selected="true"] {
  background: linear-gradient(135deg, rgba(193,191,255,.2), rgba(94,252,232,.1)) !important;
  color: var(--prism) !important;
}

/* hide chrome */
#MainMenu, footer, [data-testid="stDeployButton"],
[data-testid="stDecoration"] { display: none !important; }
header { background: transparent !important; box-shadow: none !important; }

/* scrollbar */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(193,191,255,.2); border-radius: 4px; }

/* labels / text */
label, .stCheckbox label span, .stRadio label { color: var(--text) !important; }
p, .stMarkdown p { color: var(--text) !important; font-family: var(--sans) !important; }
h1,h2,h3 { font-family: var(--sans) !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# PLOTLY THEME
# ─────────────────────────────────────────────────────────────────────────────
PALETTE = ['#C1BFFF','#5efce8','#ff8fab','#ffd97d','#72efdd','#9b96ff','#ffb3c6','#a8edea']

LAYOUT = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(193,191,255,.03)',
    font=dict(family='JetBrains Mono, monospace', color='#eeeeff', size=11),
    xaxis=dict(gridcolor='rgba(193,191,255,.08)', linecolor='rgba(193,191,255,.12)',
               tickfont=dict(color='rgba(193,191,255,.5)', size=10)),
    yaxis=dict(gridcolor='rgba(193,191,255,.08)', linecolor='rgba(193,191,255,.12)',
               tickfont=dict(color='rgba(193,191,255,.5)', size=10)),
    margin=dict(l=40, r=20, t=45, b=40),
    colorway=PALETTE,
    legend=dict(bgcolor='rgba(0,0,0,0)', font_color='#eeeeff'),
)

def themed(fig, title='', h=420):
    fig.update_layout(**LAYOUT,
        title=dict(text=title, font=dict(color='#C1BFFF', size=13, family='JetBrains Mono')),
        height=h)
    return fig

# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def mcard(label, val, cls='', sub=''):
    st.markdown(f"""
    <div class="m-card {cls}">
      <div class="m-label">{label}</div>
      <div class="m-value">{val}</div>
      {"<div class='m-sub'>"+sub+"</div>" if sub else ""}
    </div>""", unsafe_allow_html=True)

def slabel(text):
    st.markdown(f'<div class="s-label">{text}</div>', unsafe_allow_html=True)

def info(msg):  st.markdown(f'<div class="al al-info">ℹ {msg}</div>', unsafe_allow_html=True)
def warn(msg):  st.markdown(f'<div class="al al-warn">⚠ {msg}</div>', unsafe_allow_html=True)
def ok(msg):    st.markdown(f'<div class="al al-ok">✓ {msg}</div>', unsafe_allow_html=True)

def page_header(eyebrow, title, desc=''):
    st.markdown(f"""
    <div class="page-header">
      <div class="page-eyebrow">{eyebrow}</div>
      <div class="page-title">{title}</div>
      {"<div class='page-desc'>"+desc+"</div>" if desc else ""}
    </div>""", unsafe_allow_html=True)

@st.cache_data
def load_samples():
    from sklearn.datasets import (load_iris, load_wine, load_breast_cancer,
                                  fetch_california_housing, load_digits)
    return {
        "Iris — Multiclass": load_iris(as_frame=True).frame,
        "Wine — Multiclass": load_wine(as_frame=True).frame,
        "Breast Cancer — Binary": load_breast_cancer(as_frame=True).frame,
        "California Housing — Regression": fetch_california_housing(as_frame=True).frame,
    }

# ─────────────────────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────────────────────
defaults = dict(df=None, target=None, task="Classification")
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR — custom pill nav
# ─────────────────────────────────────────────────────────────────────────────
NAV = {
    "workspace": [
        ("🏠", "Overview"),
        ("📂", "Data Loading"),
    ],
    "explore": [
        ("🔍", "EDA"),
        ("🌡️", "Heatmap"),
        ("📊", "Histograms"),
        ("📦", "Box Plots"),
        ("✦",  "Scatter Plots"),
    ],
    "models": [
        ("🔮", "PCA"),
        ("〜", "Linear Regression"),
        ("◎",  "Logistic Regression"),
        ("🌳", "Decision Tree"),
        ("🌲", "Random Forest"),
        ("🏆", "Model Comparison"),
    ],
}

with st.sidebar:
    st.markdown("""
    <div class="brand">
      <div class="brand-logo">✦ Prism</div>
      <div class="brand-title">ML Studio</div>
      <div class="brand-sub">machine learning workspace</div>
    </div>""", unsafe_allow_html=True)

    all_pages = [name for group in NAV.values() for (_, name) in group]
    if "page" not in st.session_state:
        st.session_state["page"] = "Overview"

    for group_name, items in NAV.items():
        st.markdown(f'<div class="nav-section">{group_name}</div>', unsafe_allow_html=True)
        for icon, name in items:
            active = "active" if st.session_state["page"] == name else ""
            if st.button(f"{icon}  {name}", key=f"nav_{name}",
                         use_container_width=True):
                st.session_state["page"] = name
                st.rerun()
        st.markdown('<div class="nav-divider"></div>', unsafe_allow_html=True)

    # Status footer
    if st.session_state.df is not None:
        df_info = st.session_state.df
        st.markdown(f"""
        <div style="padding:.75rem 1.5rem; margin-top:.5rem;">
          <div class="m-label">Dataset loaded</div>
          <div style="font-family:var(--mono);font-size:.78rem;color:var(--prism);margin:.3rem 0 .1rem;">
            {df_info.shape[0]:,} × {df_info.shape[1]} 
          </div>
          {"<div class='m-sub'>🎯 "+st.session_state.target+"</div>" if st.session_state.target else ""}
        </div>""", unsafe_allow_html=True)

page = st.session_state["page"]

# ─────────────────────────────────────────────────────────────────────────────
# PAGE: OVERVIEW
# ─────────────────────────────────────────────────────────────────────────────
if page == "Overview":
    st.markdown("""
    <div style="padding: 4rem 2rem 2rem; text-align:center; max-width:700px; margin:auto;">
      <div style="font-family:'JetBrains Mono',monospace; font-size:.65rem;
                  color:rgba(193,191,255,.5); letter-spacing:.35em; text-transform:uppercase;
                  margin-bottom:1rem;">
        ✦ machine learning workspace
      </div>
      <h1 style="font-size:3.2rem; font-weight:700; letter-spacing:-.04em; margin:0; line-height:1;
                 background:linear-gradient(135deg,#eeeeff 0%,#C1BFFF 50%,#5efce8 100%);
                 -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;">
        Prism ML Studio
      </h1>
      <p style="color:rgba(193,191,255,.5); margin-top:1rem; font-size:1rem; font-weight:300;
                line-height:1.6;">
        End-to-end data exploration and model training—<br>from raw CSV to model comparison in one unified space.
      </p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    features = [
        ("📂", "Data Loading", "CSV upload · built-in datasets · target config", ""),
        ("🔍", "Exploration", "EDA · heatmaps · histograms · scatter · box plots", "teal"),
        ("🔮", "Decomposition", "2D + 3D PCA with interactive rotation", "rose"),
        ("🤖", "ML Models", "Linear · Logistic · Decision Tree · Random Forest", "amber"),
    ]
    for col, (icon, title, sub, cls) in zip([c1,c2,c3,c4], features):
        with col:
            st.markdown(f"""
            <div class="m-card {cls}" style="padding:1.5rem; text-align:center; cursor:default;">
              <div style="font-size:2rem; margin-bottom:.75rem;">{icon}</div>
              <div style="font-size:.92rem; font-weight:600; color:var(--text); margin-bottom:.4rem;">{title}</div>
              <div class="m-sub" style="font-size:.75rem; line-height:1.5;">{sub}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    info("Begin by navigating to  <strong>Data Loading</strong>  in the sidebar.")

# ─────────────────────────────────────────────────────────────────────────────
# PAGE: DATA LOADING
# ─────────────────────────────────────────────────────────────────────────────
elif page == "Data Loading":
    page_header("workspace · 01", "Data Loading", "Upload your own CSV or pick a built-in dataset to get started.")

    t1, t2 = st.tabs(["  📤  Upload CSV  ", "  🗃️  Sample Datasets  "])

    with t1:
        uploaded = st.file_uploader("", type=["csv"], label_visibility="collapsed")
        if uploaded:
            df = pd.read_csv(uploaded)
            st.session_state.df = df
            ok(f"Loaded **{uploaded.name}** — {df.shape[0]:,} rows × {df.shape[1]} columns")

    with t2:
        samples = load_samples()
        chosen = st.selectbox("", list(samples.keys()), label_visibility="collapsed")
        if st.button("Load Dataset →"):
            st.session_state.df = samples[chosen]
            ok(f"Loaded  **{chosen}**")

    if st.session_state.df is not None:
        df = st.session_state.df
        slabel("configuration")
        c1, c2 = st.columns(2)
        with c1:
            st.session_state.target = st.selectbox("Target column", df.columns.tolist(),
                                                    index=len(df.columns)-1)
        with c2:
            st.session_state.task = st.selectbox("Task type", ["Classification","Regression"])

        slabel("preview")
        n = st.slider("Rows", 5, min(200, len(df)), 10)
        st.dataframe(df.head(n), use_container_width=True)

        slabel("quick stats")
        cols = st.columns(4)
        stats = [
            ("rows", f"{df.shape[0]:,}", "", ""),
            ("columns", f"{df.shape[1]}", "teal", ""),
            ("missing", f"{df.isnull().sum().sum():,}", "rose" if df.isnull().sum().sum() else "teal", "values"),
            ("duplicates", f"{df.duplicated().sum()}", "amber" if df.duplicated().sum() else "teal", "rows"),
        ]
        for col, (lbl, val, cls, sub) in zip(cols, stats):
            with col: mcard(lbl, val, cls, sub)

# ─────────────────────────────────────────────────────────────────────────────
# GATE — all analysis pages need data
# ─────────────────────────────────────────────────────────────────────────────
elif st.session_state.df is None:
    warn("Load a dataset first via  **Data Loading**.")
    st.stop()

else:
    df     = st.session_state.df
    target = st.session_state.target
    task   = st.session_state.task
    num_cols = df.select_dtypes(include=np.number).columns.tolist()
    cat_cols = df.select_dtypes(exclude=np.number).columns.tolist()

    # ── EDA ──────────────────────────────────────────────────────────────────
    if page == "EDA":
        page_header("explore · 01", "Exploratory Data Analysis",
                    "Understand your dataset's structure, distributions and missing data.")

        subtab = st.radio("", ["Overview","Statistics","Missing Values","Column Types"],
                          horizontal=True, label_visibility="collapsed")

        if subtab == "Overview":
            cols = st.columns(4)
            for col, (lbl, val, cls) in zip(cols, [
                ("rows", f"{df.shape[0]:,}", ""),
                ("columns", f"{df.shape[1]}", "teal"),
                ("numeric", f"{len(num_cols)}", ""),
                ("categorical", f"{len(cat_cols)}", "amber"),
            ]):
                with col: mcard(lbl, val, cls)
            st.dataframe(df.head(30), use_container_width=True)

        elif subtab == "Statistics":
            st.dataframe(df.describe().T.round(3), use_container_width=True)

        elif subtab == "Missing Values":
            miss = df.isnull().sum().reset_index()
            miss.columns = ["Column","Missing"]
            miss["Pct"] = (miss["Missing"]/len(df)*100).round(2)
            miss = miss[miss["Missing"] > 0]
            if miss.empty:
                ok("No missing values found — clean dataset!")
            else:
                fig = px.bar(miss, x="Column", y="Pct",
                             color="Pct", color_continuous_scale=["#5efce8","#ffd97d","#ff8fab"])
                themed(fig, "Missing Values by Column (%)")
                st.plotly_chart(fig, use_container_width=True)
                st.dataframe(miss, use_container_width=True)

        else:
            dtype_df = pd.DataFrame({
                "Column": df.columns, "Dtype": df.dtypes.astype(str),
                "Unique": df.nunique(), "Nulls": df.isnull().sum(),
                "Sample": [str(df[c].dropna().iloc[0]) if len(df[c].dropna()) else "—" for c in df.columns]
            })
            st.dataframe(dtype_df, use_container_width=True)

    # ── HEATMAP ──────────────────────────────────────────────────────────────
    elif page == "Heatmap":
        page_header("explore · 02", "Correlation Heatmap",
                    "Pearson correlations between numeric features visualised as an interactive matrix.")

        corr_cols = [c for c in num_cols if df[c].nunique() > 1]
        if len(corr_cols) < 2:
            warn("Need at least 2 numeric columns.")
        else:
            sel = st.multiselect("Select features", corr_cols,
                                 default=corr_cols[:min(14, len(corr_cols))])
            if len(sel) >= 2:
                corr = df[sel].corr()
                fig = px.imshow(corr, text_auto=".2f",
                                color_continuous_scale=[[0,'#ff8fab'],[.5,'#0c0c1e'],[1,'#C1BFFF']],
                                zmin=-1, zmax=1, aspect="auto")
                fig.update_traces(textfont_size=9)
                themed(fig, "Pearson Correlation Matrix", h=620)
                st.plotly_chart(fig, use_container_width=True)

                with st.expander("Top Feature Pairs"):
                    pairs = [(corr.columns[i], corr.columns[j], round(corr.iloc[i,j],4))
                             for i in range(len(corr.columns))
                             for j in range(i+1, len(corr.columns))]
                    top = pd.DataFrame(pairs, columns=["A","B","ρ"])
                    top = top.reindex(top["ρ"].abs().sort_values(ascending=False).index)
                    st.dataframe(top.head(20), use_container_width=True)

    # ── HISTOGRAMS ───────────────────────────────────────────────────────────
    elif page == "Histograms":
        page_header("explore · 03", "Histograms",
                    "Distribution of numeric features with adjustable bin resolution.")
        if not num_cols:
            warn("No numeric columns.")
        else:
            c1, c2 = st.columns([3,1])
            with c1: sel = st.multiselect("Features", num_cols, default=num_cols[:min(6,len(num_cols))])
            with c2: bins = st.slider("Bins", 10, 120, 35)
            if sel:
                n_cols = min(3, len(sel))
                n_rows = (len(sel)+n_cols-1)//n_cols
                fig = make_subplots(rows=n_rows, cols=n_cols,
                                    subplot_titles=[f"<span style='color:#C1BFFF;font-size:11px'>{c}</span>" for c in sel],
                                    vertical_spacing=.1)
                for i, col in enumerate(sel):
                    r, c_ = divmod(i, n_cols)
                    fig.add_trace(go.Histogram(
                        x=df[col].dropna(), nbinsx=bins,
                        marker=dict(color=PALETTE[i%len(PALETTE)],
                                    line=dict(width=0)),
                        name=col, opacity=.8), row=r+1, col=c_+1)
                fig.update_layout(**LAYOUT, height=280*n_rows, showlegend=False)
                st.plotly_chart(fig, use_container_width=True)

    # ── BOX PLOTS ────────────────────────────────────────────────────────────
    elif page == "Box Plots":
        page_header("explore · 04", "Box Plots",
                    "Median, IQR and outliers across features, optionally grouped by category.")
        if not num_cols:
            warn("No numeric columns.")
        else:
            c1, c2 = st.columns(2)
            with c1: sel = st.multiselect("Y-axis features", num_cols, default=num_cols[:min(5,len(num_cols))])
            with c2:
                grp_opts = ["None"] + cat_cols + ([target] if target in df.columns else [])
                group_by = st.selectbox("Group by", grp_opts)
            if sel:
                melted = df[sel].melt(var_name="Feature", value_name="Value")
                if group_by != "None" and group_by in df.columns:
                    rep_times = len(melted)//len(df)
                    melted[group_by] = list(df[group_by].values)*rep_times + list(df[group_by].values[:len(melted)%len(df)])
                    fig = px.box(melted, x="Feature", y="Value", color=group_by,
                                 color_discrete_sequence=PALETTE)
                else:
                    fig = px.box(melted, x="Feature", y="Value", color="Feature",
                                 color_discrete_sequence=PALETTE)
                themed(fig, "Feature Distributions")
                st.plotly_chart(fig, use_container_width=True)

    # ── SCATTER PLOTS ────────────────────────────────────────────────────────
    elif page == "Scatter Plots":
        page_header("explore · 05", "Scatter Plots",
                    "2-D scatter with optional colour / size encoding and pair-plot matrix.")
        if len(num_cols) < 2:
            warn("Need at least 2 numeric columns.")
        else:
            c1, c2, c3, c4 = st.columns(4)
            with c1: x_col = st.selectbox("X", num_cols, 0)
            with c2: y_col = st.selectbox("Y", num_cols, min(1,len(num_cols)-1))
            with c3: color_col = st.selectbox("Colour", ["None"]+df.columns.tolist())
            with c4: size_col  = st.selectbox("Size",   ["None"]+num_cols)

            kw = dict(x=x_col, y=y_col, opacity=.75,
                      color_discrete_sequence=PALETTE)
            if color_col != "None": kw["color"] = color_col
            if size_col  != "None": kw["size"]  = size_col
            fig = px.scatter(df, **kw)
            themed(fig, f"{x_col}  ↔  {y_col}", h=500)
            st.plotly_chart(fig, use_container_width=True)

            with st.expander("Pair-Plot Matrix"):
                pair_sel = st.multiselect("Features", num_cols, default=num_cols[:min(4,len(num_cols))])
                if len(pair_sel) >= 2:
                    pkw = dict(dimensions=pair_sel, opacity=.65,
                               color_continuous_scale="Purp")
                    if color_col != "None" and color_col in df.columns:
                        pkw["color"] = color_col
                    fig2 = px.scatter_matrix(df, **pkw)
                    fig2.update_layout(**LAYOUT, height=600)
                    st.plotly_chart(fig2, use_container_width=True)

    # ── PCA ──────────────────────────────────────────────────────────────────
    elif page == "PCA":
        page_header("models · 01", "Principal Component Analysis",
                    "Dimensionality reduction with interactive 2D & 3D projections.")

        feats = [c for c in num_cols if c != target]
        if len(feats) < 3:
            warn("Need at least 3 numeric features for PCA.")
            st.stop()

        max_comp = min(len(feats), 10)
        c1, c2 = st.columns([2,1])
        with c1: n_comp = st.slider("Number of components", 3, max_comp, min(6, max_comp))
        with c2:
            color_by = st.selectbox("Colour points by",
                                    ["None"] + df.columns.tolist(),
                                    index=df.columns.tolist().index(target)+1 if target in df.columns.tolist() else 0)

        Xs = df[feats].fillna(df[feats].median())
        scaler = StandardScaler()
        X_sc = scaler.fit_transform(Xs)
        pca = PCA(n_components=n_comp)
        X_pca = pca.fit_transform(X_sc)
        evr = pca.explained_variance_ratio_

        # ── scree ──
        slabel("explained variance")
        fig_scree = go.Figure()
        fig_scree.add_trace(go.Bar(
            x=[f"PC{i+1}" for i in range(n_comp)], y=evr*100,
            marker=dict(color=PALETTE[0],
                        line=dict(width=0)),
            name="Individual", opacity=.85))
        fig_scree.add_trace(go.Scatter(
            x=[f"PC{i+1}" for i in range(n_comp)], y=np.cumsum(evr)*100,
            mode='lines+markers', name="Cumulative",
            line=dict(color='#5efce8', width=2),
            marker=dict(size=6, color='#5efce8')))
        themed(fig_scree, "Scree Plot — Explained Variance (%)", h=320)
        st.plotly_chart(fig_scree, use_container_width=True)

        pca_df = pd.DataFrame(X_pca, columns=[f"PC{i+1}" for i in range(n_comp)])
        color_vals = None
        if color_by != "None" and color_by in df.columns:
            pca_df[color_by] = df[color_by].values[:len(pca_df)]
            color_vals = color_by

        # ── 2D projection ──
        slabel("2D projection  —  PC1 vs PC2")
        fig2d = px.scatter(
            pca_df, x="PC1", y="PC2",
            color=color_vals,
            color_discrete_sequence=PALETTE,
            color_continuous_scale="Purp",
            opacity=.82,
            hover_data=pca_df.columns[:4].tolist()
        )
        fig2d.update_traces(marker=dict(size=7, line=dict(width=0)))
        themed(fig2d,
               f"PC1 ({evr[0]*100:.1f}%)  ×  PC2 ({evr[1]*100:.1f}%)", h=460)
        st.plotly_chart(fig2d, use_container_width=True)

        # ── 3D projection ──
        slabel("3D projection  —  PC1 · PC2 · PC3  (drag to rotate)")
        if n_comp >= 3:
            if color_vals and color_vals in pca_df.columns:
                raw_col = pca_df[color_vals]
                # numeric colour mapping
                if pd.api.types.is_numeric_dtype(raw_col):
                    marker_kw = dict(
                        color=raw_col,
                        colorscale=[[0,'#ff8fab'],[.5,'#C1BFFF'],[1,'#5efce8']],
                        showscale=True,
                        colorbar=dict(thickness=10, tickfont=dict(color='#C1BFFF', size=9)),
                        size=5, opacity=.85,
                        line=dict(width=0)
                    )
                    traces = [go.Scatter3d(
                        x=pca_df["PC1"], y=pca_df["PC2"], z=pca_df["PC3"],
                        mode='markers', marker=marker_kw, name='data'
                    )]
                else:
                    # categorical
                    cats = raw_col.unique()
                    traces = []
                    for i, cat in enumerate(cats):
                        mask = raw_col == cat
                        traces.append(go.Scatter3d(
                            x=pca_df.loc[mask,"PC1"], y=pca_df.loc[mask,"PC2"],
                            z=pca_df.loc[mask,"PC3"], mode='markers',
                            name=str(cat),
                            marker=dict(size=5, color=PALETTE[i%len(PALETTE)],
                                        opacity=.85, line=dict(width=0))
                        ))
            else:
                traces = [go.Scatter3d(
                    x=pca_df["PC1"], y=pca_df["PC2"], z=pca_df["PC3"],
                    mode='markers',
                    marker=dict(size=5, color='#C1BFFF', opacity=.82, line=dict(width=0))
                )]

            fig3d = go.Figure(data=traces)
            fig3d.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                scene=dict(
                    bgcolor='rgba(12,12,30,.9)',
                    xaxis=dict(title=dict(text=f"PC1 ({evr[0]*100:.1f}%)",
                                          font=dict(color='#C1BFFF', size=11)),
                               backgroundcolor='rgba(0,0,0,0)',
                               gridcolor='rgba(193,191,255,.1)',
                               zerolinecolor='rgba(193,191,255,.2)',
                               tickfont=dict(color='rgba(193,191,255,.5)', size=9)),
                    yaxis=dict(title=dict(text=f"PC2 ({evr[1]*100:.1f}%)",
                                          font=dict(color='#C1BFFF', size=11)),
                               backgroundcolor='rgba(0,0,0,0)',
                               gridcolor='rgba(193,191,255,.1)',
                               zerolinecolor='rgba(193,191,255,.2)',
                               tickfont=dict(color='rgba(193,191,255,.5)', size=9)),
                    zaxis=dict(title=dict(text=f"PC3 ({evr[2]*100:.1f}%)",
                                          font=dict(color='#C1BFFF', size=11)),
                               backgroundcolor='rgba(0,0,0,0)',
                               gridcolor='rgba(193,191,255,.1)',
                               zerolinecolor='rgba(193,191,255,.2)',
                               tickfont=dict(color='rgba(193,191,255,.5)', size=9)),
                    camera=dict(eye=dict(x=1.5, y=1.5, z=1.2)),
                ),
                font=dict(family='JetBrains Mono', color='#eeeeff', size=11),
                margin=dict(l=0, r=0, t=40, b=0),
                height=580,
                title=dict(text=f"3D PCA Projection — {np.sum(evr[:3])*100:.1f}% variance explained",
                           font=dict(color='#C1BFFF', size=13)),
                legend=dict(bgcolor='rgba(12,12,30,.6)', bordercolor='rgba(193,191,255,.15)',
                            borderwidth=1, font=dict(color='#eeeeff', size=10)),
            )
            st.plotly_chart(fig3d, use_container_width=True)

        # ── loadings ──
        with st.expander("Component Loadings"):
            loadings = pd.DataFrame(
                pca.components_.T, index=feats,
                columns=[f"PC{i+1}" for i in range(n_comp)])
            st.dataframe(loadings.round(4), use_container_width=True)

    # ──────────────────────────────────────────────────────────────────────────
    # ML — shared prep
    # ──────────────────────────────────────────────────────────────────────────
    elif page in ["Linear Regression","Logistic Regression",
                   "Decision Tree","Random Forest","Model Comparison"]:

        if not target or target not in df.columns:
            warn("Set a target column in **Data Loading** first."); st.stop()

        feats = [c for c in num_cols if c != target]
        if not feats:
            warn("No numeric features available."); st.stop()

        X_raw = df[feats].fillna(df[feats].median())
        y_raw = df[target]
        le = LabelEncoder()
        if task == "Classification":
            y_enc = le.fit_transform(y_raw.astype(str))
        else:
            if not pd.api.types.is_numeric_dtype(y_raw):
                warn("Target must be numeric for Regression."); st.stop()
            y_enc = y_raw.values

        scaler = StandardScaler()
        X_sc = scaler.fit_transform(X_raw)

        with st.sidebar:
            st.markdown('<div class="nav-divider"></div>', unsafe_allow_html=True)
            test_size = st.slider("Test split", .1, .5, .2, .05)
            rs = st.number_input("Random state", 0, 99, 42)

        X_tr, X_te, y_tr, y_te = train_test_split(X_sc, y_enc, test_size=test_size, random_state=int(rs))

        # ── LINEAR REGRESSION ────────────────────────────────────────────────
        if page == "Linear Regression":
            page_header("models · 02", "Linear Regression",
                        "Ordinary least squares — coefficients, residuals and fit metrics.")
            if task != "Regression":
                warn("Switch Task Type to  Regression  in Data Loading."); st.stop()

            fit_int = st.checkbox("Fit intercept", True)
            model = LinearRegression(fit_intercept=fit_int)
            model.fit(X_tr, y_tr)
            preds = model.predict(X_te)
            r2   = r2_score(y_te, preds)
            rmse = np.sqrt(mean_squared_error(y_te, preds))
            mae  = mean_absolute_error(y_te, preds)
            cv   = cross_val_score(model, X_sc, y_enc, cv=5, scoring='r2').mean()

            slabel("metrics")
            cols = st.columns(4)
            for col, (lbl, val, cls) in zip(cols, [
                ("R² Score", f"{r2:.4f}", "teal" if r2>.7 else "amber"),
                ("CV R²",    f"{cv:.4f}", "teal" if cv>.7 else "amber"),
                ("RMSE",     f"{rmse:.4f}", ""),
                ("MAE",      f"{mae:.4f}",  "rose"),
            ]):
                with col: mcard(lbl, val, cls)

            slabel("diagnostics")
            c1, c2 = st.columns(2)
            with c1:
                fig = go.Figure()
                mn, mx = float(min(y_te.min(), preds.min())), float(max(y_te.max(), preds.max()))
                fig.add_trace(go.Scatter(x=y_te, y=preds, mode='markers',
                                         marker=dict(color='#C1BFFF', size=6, opacity=.7)))
                fig.add_trace(go.Scatter(x=[mn,mx], y=[mn,mx], mode='lines',
                                         line=dict(color='#ff8fab', dash='dash', width=1.5), name='perfect'))
                themed(fig, "Actual vs Predicted")
                st.plotly_chart(fig, use_container_width=True)

            with c2:
                residuals = y_te - preds
                fig = go.Figure(go.Histogram(x=residuals, nbinsx=35,
                                              marker=dict(color='#5efce8', line=dict(width=0)), opacity=.85))
                themed(fig, "Residual Distribution")
                st.plotly_chart(fig, use_container_width=True)

            with st.expander("Feature Coefficients"):
                coef_df = pd.DataFrame({"Feature":feats,"Coefficient":model.coef_})
                coef_df = coef_df.sort_values("Coefficient", key=abs, ascending=True)
                fig = px.bar(coef_df, x="Coefficient", y="Feature", orientation='h',
                             color="Coefficient",
                             color_continuous_scale=[[0,'#ff8fab'],[.5,'#0c0c1e'],[1,'#C1BFFF']])
                themed(fig, "Coefficients")
                st.plotly_chart(fig, use_container_width=True)

        # ── LOGISTIC REGRESSION ──────────────────────────────────────────────
        elif page == "Logistic Regression":
            page_header("models · 03", "Logistic Regression",
                        "Probabilistic classifier with ROC-AUC curve and confusion matrix.")
            if task != "Classification":
                warn("Switch Task Type to  Classification."); st.stop()

            c1, c2 = st.columns(2)
            with c1: C = st.select_slider("Regularisation C", [.01,.1,1,10,100], value=1)
            with c2: solver = st.selectbox("Solver", ["lbfgs","saga","liblinear"])

            model = LogisticRegression(C=C, solver=solver, max_iter=2000, random_state=42)
            model.fit(X_tr, y_tr)
            preds = model.predict(X_te)
            acc = accuracy_score(y_te, preds)
            cv  = cross_val_score(model, X_sc, y_enc, cv=5).mean()

            slabel("metrics")
            cols = st.columns(3)
            for col, (lbl, val, cls) in zip(cols, [
                ("Accuracy",    f"{acc:.4f}", "teal" if acc>.8 else "amber"),
                ("CV Accuracy", f"{cv:.4f}",  "teal" if cv>.8 else "amber"),
                ("Classes",     f"{len(np.unique(y_enc))}", ""),
            ]):
                with col: mcard(lbl, val, cls)

            slabel("diagnostics")
            c1, c2 = st.columns(2)
            with c1:
                cm = confusion_matrix(y_te, preds)
                fig = px.imshow(cm, text_auto=True,
                                color_continuous_scale=[[0,'#06060f'],[1,'#C1BFFF']],
                                labels=dict(x="Predicted", y="Actual"))
                themed(fig, "Confusion Matrix")
                st.plotly_chart(fig, use_container_width=True)
            with c2:
                if len(np.unique(y_enc)) == 2:
                    prob = model.predict_proba(X_te)[:,1]
                    fpr, tpr, _ = roc_curve(y_te, prob)
                    auc_s = auc(fpr, tpr)
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(x=fpr, y=tpr, fill='tozeroy',
                                             fillcolor='rgba(193,191,255,.1)',
                                             line=dict(color='#C1BFFF', width=2),
                                             name=f"AUC = {auc_s:.3f}"))
                    fig.add_trace(go.Scatter(x=[0,1], y=[0,1], mode='lines',
                                             line=dict(dash='dash', color='rgba(193,191,255,.3)',width=1),
                                             name="Random"))
                    themed(fig, "ROC Curve")
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.text("Multi-class ROC not shown — see confusion matrix.")

        # ── DECISION TREE ────────────────────────────────────────────────────
        elif page == "Decision Tree":
            page_header("models · 04", "Decision Tree",
                        "Non-parametric learner — tune depth and inspect feature importances.")
            c1, c2 = st.columns(2)
            with c1: max_d = st.slider("Max depth", 1, 20, 5)
            with c2: min_s = st.slider("Min samples split", 2, 50, 2)

            if task == "Classification":
                model = DecisionTreeClassifier(max_depth=max_d, min_samples_split=min_s, random_state=42)
                model.fit(X_tr, y_tr); preds = model.predict(X_te)
                acc = accuracy_score(y_te, preds)
                cv  = cross_val_score(model, X_sc, y_enc, cv=5).mean()
                cols = st.columns(3)
                for col, (lbl, val, cls) in zip(cols, [
                    ("Accuracy", f"{acc:.4f}", "teal" if acc>.8 else "amber"),
                    ("CV Score", f"{cv:.4f}",  "teal" if cv>.8 else "amber"),
                    ("Depth",    f"{model.get_depth()}", ""),
                ]):
                    with col: mcard(lbl, val, cls)

                cm = confusion_matrix(y_te, preds)
                fig = px.imshow(cm, text_auto=True,
                                color_continuous_scale=[[0,'#06060f'],[1,'#C1BFFF']],
                                labels=dict(x="Predicted", y="Actual"))
                themed(fig, "Confusion Matrix")
                st.plotly_chart(fig, use_container_width=True)
            else:
                model = DecisionTreeRegressor(max_depth=max_d, min_samples_split=min_s, random_state=42)
                model.fit(X_tr, y_tr); preds = model.predict(X_te)
                r2   = r2_score(y_te, preds)
                rmse = np.sqrt(mean_squared_error(y_te, preds))
                cols = st.columns(2)
                with cols[0]: mcard("R²", f"{r2:.4f}", "teal" if r2>.7 else "amber")
                with cols[1]: mcard("RMSE", f"{rmse:.4f}", "rose")
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=y_te, y=preds, mode='markers',
                                         marker=dict(color='#C1BFFF', size=5, opacity=.7)))
                mn, mx = float(min(y_te.min(),preds.min())), float(max(y_te.max(),preds.max()))
                fig.add_trace(go.Scatter(x=[mn,mx],y=[mn,mx],mode='lines',
                                         line=dict(color='#ff8fab',dash='dash',width=1.5)))
                themed(fig, "Actual vs Predicted"); st.plotly_chart(fig, use_container_width=True)

            with st.expander("Feature Importances"):
                fi = pd.DataFrame({"Feature":feats,"Importance":model.feature_importances_})
                fi = fi.sort_values("Importance", ascending=True)
                fig = px.bar(fi, x="Importance", y="Feature", orientation='h',
                             color="Importance", color_continuous_scale=["#0c0c1e","#C1BFFF"])
                themed(fig, "Feature Importances")
                st.plotly_chart(fig, use_container_width=True)

        # ── RANDOM FOREST ────────────────────────────────────────────────────
        elif page == "Random Forest":
            page_header("models · 05", "Random Forest",
                        "Ensemble of decision trees — strong baseline with built-in feature ranking.")
            c1, c2, c3 = st.columns(3)
            with c1: n_est = st.slider("Estimators", 10, 300, 100, 10)
            with c2: max_d = st.slider("Max depth", 1, 20, 5)
            with c3: min_s = st.slider("Min samples", 2, 30, 2)

            with st.spinner("Training ensemble…"):
                if task == "Classification":
                    model = RandomForestClassifier(n_estimators=n_est, max_depth=max_d,
                                                   min_samples_split=min_s, random_state=42, n_jobs=-1)
                    model.fit(X_tr, y_tr); preds = model.predict(X_te)
                    acc = accuracy_score(y_te, preds)
                    cv  = cross_val_score(model, X_sc, y_enc, cv=5).mean()
                    slabel("metrics")
                    cols = st.columns(3)
                    for col, (lbl, val, cls) in zip(cols, [
                        ("Accuracy",    f"{acc:.4f}", "teal" if acc>.8 else "amber"),
                        ("CV Accuracy", f"{cv:.4f}",  "teal" if cv>.8 else "amber"),
                        ("Trees",       f"{n_est}", ""),
                    ]):
                        with col: mcard(lbl, val, cls)

                    slabel("diagnostics")
                    c1, c2 = st.columns(2)
                    with c1:
                        cm = confusion_matrix(y_te, preds)
                        fig = px.imshow(cm, text_auto=True,
                                        color_continuous_scale=[[0,'#06060f'],[1,'#5efce8']],
                                        labels=dict(x="Predicted", y="Actual"))
                        themed(fig, "Confusion Matrix")
                        st.plotly_chart(fig, use_container_width=True)
                    with c2:
                        fi = pd.DataFrame({"Feature":feats,"Importance":model.feature_importances_})
                        fi = fi.sort_values("Importance",ascending=True).tail(15)
                        fig = px.bar(fi, x="Importance", y="Feature", orientation='h',
                                     color="Importance", color_continuous_scale=["#0c0c1e","#5efce8"])
                        themed(fig, "Feature Importances")
                        st.plotly_chart(fig, use_container_width=True)
                else:
                    model = RandomForestRegressor(n_estimators=n_est, max_depth=max_d,
                                                  min_samples_split=min_s, random_state=42, n_jobs=-1)
                    model.fit(X_tr, y_tr); preds = model.predict(X_te)
                    r2   = r2_score(y_te, preds)
                    rmse = np.sqrt(mean_squared_error(y_te, preds))
                    cols = st.columns(2)
                    with cols[0]: mcard("R²", f"{r2:.4f}", "teal" if r2>.7 else "amber")
                    with cols[1]: mcard("RMSE", f"{rmse:.4f}", "rose")
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(x=y_te, y=preds, mode='markers',
                                             marker=dict(color='#5efce8', size=5, opacity=.72)))
                    mn, mx = float(min(y_te.min(),preds.min())), float(max(y_te.max(),preds.max()))
                    fig.add_trace(go.Scatter(x=[mn,mx],y=[mn,mx],mode='lines',
                                             line=dict(color='#ff8fab',dash='dash',width=1.5)))
                    themed(fig, "Actual vs Predicted"); st.plotly_chart(fig, use_container_width=True)

        # ── MODEL COMPARISON ─────────────────────────────────────────────────
        elif page == "Model Comparison":
            page_header("models · 06", "Model Comparison",
                        "Side-by-side leaderboard with bar chart and radar visualisation.")

            with st.spinner("Training all models…"):
                results = {}
                if task == "Classification":
                    models_dict = {
                        "Logistic Reg.": LogisticRegression(max_iter=2000, random_state=42),
                        "Decision Tree": DecisionTreeClassifier(max_depth=5, random_state=42),
                        "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1),
                    }
                    for nm, m in models_dict.items():
                        m.fit(X_tr, y_tr); p = m.predict(X_te)
                        cv = cross_val_score(m, X_sc, y_enc, cv=5).mean()
                        results[nm] = {"Test Accuracy": accuracy_score(y_te,p), "CV Accuracy": cv}
                else:
                    models_dict = {
                        "Linear Reg.":  LinearRegression(),
                        "Decision Tree":DecisionTreeRegressor(max_depth=5, random_state=42),
                        "Random Forest":RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1),
                    }
                    for nm, m in models_dict.items():
                        m.fit(X_tr, y_tr); p = m.predict(X_te)
                        cv = cross_val_score(m, X_sc, y_enc, cv=5, scoring='r2').mean()
                        results[nm] = {"Test R²": r2_score(y_te,p), "CV R²": cv,
                                       "RMSE": np.sqrt(mean_squared_error(y_te,p))}

            res_df = pd.DataFrame(results).T.round(4)
            slabel("leaderboard")
            st.dataframe(res_df, use_container_width=True)

            metric = list(res_df.columns)[0]
            slabel("comparison chart")
            fig = px.bar(res_df.reset_index(), x="index", y=metric,
                         color=metric, color_continuous_scale=[[0,'#0c0c1e'],[1,'#C1BFFF']],
                         text_auto=".4f")
            fig.update_traces(marker_line_width=0, width=.5)
            themed(fig, f"Model Comparison — {metric}")
            fig.update_layout(xaxis_title="Model", bargap=.35)
            st.plotly_chart(fig, use_container_width=True)

            # radar
            if len(res_df.columns) >= 2:
                slabel("radar chart")
                cats = res_df.columns.tolist()
                fig2 = go.Figure()
                for i, (nm, row) in enumerate(res_df.iterrows()):
                    vals = row.tolist(); vals.append(vals[0])
                    c = PALETTE[i % len(PALETTE)]
                    fig2.add_trace(go.Scatterpolar(
                        r=vals, theta=cats+[cats[0]], fill='toself', name=nm,
                        line=dict(color=c, width=2),
                        fillcolor=c.replace('FF','22') if len(c)==7 else f'rgba(193,191,255,.08)'
                    ))
                fig2.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    polar=dict(
                        bgcolor='rgba(12,12,30,.8)',
                        radialaxis=dict(gridcolor='rgba(193,191,255,.1)',
                                        tickfont=dict(color='rgba(193,191,255,.4)', size=8)),
                        angularaxis=dict(gridcolor='rgba(193,191,255,.1)',
                                         tickfont=dict(color='#eeeeff', size=10)),
                    ),
                    font=dict(family='JetBrains Mono', color='#eeeeff'),
                    legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color='#eeeeff', size=10)),
                    height=440,
                    title=dict(text="Radar — Model Metrics", font=dict(color='#C1BFFF', size=13)),
                    margin=dict(l=40, r=40, t=50, b=40),
                )
                st.plotly_chart(fig2, use_container_width=True)

            best = res_df[metric].idxmax()
            ok(f"Best model: <strong>{best}</strong> — {metric} = <strong>{res_df.loc[best,metric]:.4f}</strong>")