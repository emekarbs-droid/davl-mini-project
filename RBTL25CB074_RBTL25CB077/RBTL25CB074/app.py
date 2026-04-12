import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, mean_squared_error

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="ML Dashboard", layout="wide", page_icon="✦")

# ---------------- CUSTOM CSS ----------------
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Background */
    .stApp {
        background-color: #0a0a0f;
        color: #e8e8f0;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #0f0f18;
        border-right: 1px solid #1e1e30;
    }

    [data-testid="stSidebar"] * {
        color: #b0b0c8 !important;
    }

    /* Hide default header */
    header[data-testid="stHeader"] {
        background: transparent;
    }

    /* Metric cards */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #13131f 0%, #1a1a2e 100%);
        border: 1px solid #2a2a45;
        border-radius: 14px;
        padding: 20px 24px;
        transition: border-color 0.2s ease;
    }

    [data-testid="stMetric"]:hover {
        border-color: #6c63ff;
    }

    [data-testid="stMetricLabel"] {
        color: #7878a0 !important;
        font-size: 11px !important;
        font-weight: 500 !important;
        letter-spacing: 0.08em !important;
        text-transform: uppercase !important;
    }

    [data-testid="stMetricValue"] {
        color: #e8e8f8 !important;
        font-size: 26px !important;
        font-weight: 600 !important;
    }

    /* Dataframes */
    [data-testid="stDataFrame"] {
        border: 1px solid #1e1e30 !important;
        border-radius: 12px !important;
        overflow: hidden;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #6c63ff, #a855f7);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 24px;
        font-weight: 500;
        transition: opacity 0.2s;
    }

    .stButton > button:hover {
        opacity: 0.85;
    }

    /* File uploader */
    [data-testid="stFileUploader"] {
        background: #13131f;
        border: 1px dashed #2a2a45;
        border-radius: 14px;
        padding: 12px;
    }

    /* Select boxes */
    [data-testid="stSelectbox"] > div > div {
        background: #13131f;
        border: 1px solid #2a2a45;
        border-radius: 10px;
        color: #e8e8f0;
    }

    /* Divider */
    hr {
        border-color: #1e1e30 !important;
        margin: 1.5rem 0;
    }

    /* Info box */
    .stInfo {
        background: #13131f;
        border: 1px solid #2a2a45;
        border-radius: 12px;
        color: #7878a0;
    }

    /* Section headings */
    h2, h3 {
        font-weight: 500 !important;
        letter-spacing: -0.01em !important;
    }

    /* Plot backgrounds via matplotlib */
    </style>
""", unsafe_allow_html=True)

# ---------------- MATPLOTLIB THEME ----------------
plt.rcParams.update({
    "figure.facecolor": "#0f0f18",
    "axes.facecolor": "#13131f",
    "axes.edgecolor": "#2a2a45",
    "axes.labelcolor": "#9090b8",
    "axes.titlecolor": "#e8e8f8",
    "axes.titlesize": 13,
    "axes.titleweight": "500",
    "axes.titlepad": 12,
    "axes.labelsize": 11,
    "xtick.color": "#6060a0",
    "ytick.color": "#6060a0",
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "grid.color": "#1e1e30",
    "grid.linewidth": 0.6,
    "text.color": "#c0c0e0",
    "font.family": "sans-serif",
    "figure.dpi": 120,
    "axes.spines.top": False,
    "axes.spines.right": False,
})

PALETTE = ["#6c63ff", "#a855f7", "#22d3ee", "#34d399", "#f97316", "#f43f5e"]
GRADIENT = ["#6c63ff", "#8b5cf6", "#a855f7", "#c084fc", "#e879f9"]

# ---------------- HEADER ----------------
st.markdown("""
    <div style="padding: 2.5rem 0 1rem 0;">
        <div style="display:flex; align-items:center; gap:12px; margin-bottom:6px;">
            <span style="font-size:22px; color:#6c63ff;">✦</span>
            <span style="font-size:26px; font-weight:600; color:#e8e8f8; letter-spacing:-0.02em;">ML Analytics Dashboard</span>
        </div>
        <p style="color:#6060a0; font-size:13px; margin:0; padding-left:34px;">
            Upload your dataset · Explore patterns · Benchmark models
        </p>
    </div>
    <hr>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown("""
        <div style="padding: 1rem 0 0.5rem 0;">
            <p style="font-size:11px; font-weight:600; letter-spacing:0.1em; color:#6c63ff; text-transform:uppercase; margin-bottom:12px;">
                ⚙ Controls
            </p>
        </div>
    """, unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

    st.markdown("""<hr style="border-color:#1e1e30; margin: 1rem 0;">""", unsafe_allow_html=True)
    st.markdown("""
        <p style="font-size:11px; color:#44446a; line-height:1.6;">
            Supports numeric datasets.<br>
            Last column is used as the <strong style="color:#6c63ff;">target variable</strong>.
        </p>
    """, unsafe_allow_html=True)

# ---------------- MAIN ----------------
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # --- Data Preview ---
    st.markdown("### 📋 Data Preview")
    st.dataframe(df.head(), use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 📊 Dataset Summary")
        st.dataframe(df.describe(), use_container_width=True)
    with col2:
        st.markdown("### ❗ Missing Values")
        st.dataframe(df.isnull().sum(), use_container_width=True)

    # Date conversion + fill NaNs
    for col in df.columns:
        if "date" in col.lower():
            df[col] = pd.to_datetime(df[col], errors="coerce")
    df = df.fillna(df.select_dtypes(include=np.number).mean())
    numeric_df = df.select_dtypes(include=np.number)

    if numeric_df.shape[1] < 2:
        st.error("Not enough numeric columns.")
    else:

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("### 📈 Visualizations")

        colA, colB = st.columns(2)

        # Heatmap
        with colA:
            fig, ax = plt.subplots(figsize=(5.5, 4))
            mask = np.triu(np.ones_like(numeric_df.corr(), dtype=bool))
            sns.heatmap(
                numeric_df.corr(), annot=True, fmt=".2f",
                cmap=sns.color_palette("mako", as_cmap=True),
                ax=ax, linewidths=0.3, linecolor="#1a1a2e",
                mask=mask, cbar_kws={"shrink": 0.75},
                annot_kws={"size": 8, "color": "#c0c0e0"}
            )
            ax.set_title("Correlation Heatmap")
            fig.tight_layout()
            st.pyplot(fig)

        # Histogram
        with colB:
            col_sel = st.selectbox("Select Column for Distribution", numeric_df.columns)
            fig, ax = plt.subplots(figsize=(5.5, 4))
            sns.histplot(
                numeric_df[col_sel], kde=True, ax=ax,
                color="#6c63ff", alpha=0.6,
                line_kws={"color": "#a855f7", "linewidth": 2}
            )
            ax.set_title(f"Distribution — {col_sel}")
            ax.set_xlabel(col_sel)
            ax.set_ylabel("Count")
            ax.grid(True, axis="y", alpha=0.4)
            fig.tight_layout()
            st.pyplot(fig)

        colC, colD = st.columns(2)

        # Box Plot
        with colC:
            fig, ax = plt.subplots(figsize=(5.5, 4))
            bp = ax.boxplot(
                numeric_df[col_sel].dropna(),
                patch_artist=True,
                widths=0.45,
                medianprops=dict(color="#22d3ee", linewidth=2),
                boxprops=dict(facecolor="#1a1a35", color="#6c63ff"),
                whiskerprops=dict(color="#6060a0"),
                capprops=dict(color="#6060a0"),
                flierprops=dict(marker="o", color="#f43f5e", alpha=0.5, markersize=4)
            )
            ax.set_title(f"Box Plot — {col_sel}")
            ax.set_xticks([])
            ax.grid(True, axis="y", alpha=0.4)
            fig.tight_layout()
            st.pyplot(fig)

        # Scatter Plot
        with colD:
            x_col = st.selectbox("X-axis", numeric_df.columns, key="x")
            y_col = st.selectbox("Y-axis", numeric_df.columns, key="y")
            fig, ax = plt.subplots(figsize=(5.5, 4))
            ax.scatter(
                numeric_df[x_col], numeric_df[y_col],
                c="#6c63ff", alpha=0.55, s=22, edgecolors="none"
            )
            ax.set_title(f"{x_col} vs {y_col}")
            ax.set_xlabel(x_col)
            ax.set_ylabel(y_col)
            ax.grid(True, alpha=0.25)
            fig.tight_layout()
            st.pyplot(fig)

        # --- PCA ---
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("### 🧠 PCA Projection")

        X = numeric_df.iloc[:, :-1]
        y = numeric_df.iloc[:, -1]
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        pca = PCA(n_components=2)
        X_pca = pca.fit_transform(X_scaled)
        exp_var = pca.explained_variance_ratio_ * 100

        fig, ax = plt.subplots(figsize=(7, 4))
        sc = ax.scatter(
            X_pca[:, 0], X_pca[:, 1],
            c=y, cmap="cool", alpha=0.65, s=20, edgecolors="none"
        )
        cbar = plt.colorbar(sc, ax=ax)
        cbar.ax.yaxis.set_tick_params(color="#6060a0")
        plt.setp(cbar.ax.yaxis.get_ticklabels(), color="#9090b8", fontsize=9)
        ax.set_xlabel(f"PC1 ({exp_var[0]:.1f}% variance)")
        ax.set_ylabel(f"PC2 ({exp_var[1]:.1f}% variance)")
        ax.set_title("PCA — 2-Component Projection")
        ax.grid(True, alpha=0.2)
        fig.tight_layout()
        st.pyplot(fig)

        # --- Regression ---
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("### 📉 Regression")

        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y, test_size=0.2, random_state=42
        )
        lr = LinearRegression()
        lr.fit(X_train, y_train)
        y_pred = lr.predict(X_test)
        mse_val = mean_squared_error(y_test, y_pred)

        r_col1, r_col2, r_col3 = st.columns(3)
        with r_col1:
            st.metric("MSE", f"{mse_val:.4f}")
        with r_col2:
            st.metric("RMSE", f"{np.sqrt(mse_val):.4f}")
        with r_col3:
            st.metric("R² Score", f"{lr.score(X_test, y_test):.4f}")

        # Actual vs Predicted
        fig, ax = plt.subplots(figsize=(6, 3.5))
        ax.scatter(y_test, y_pred, c="#6c63ff", alpha=0.55, s=18, edgecolors="none", label="Predicted")
        mn, mx = min(y_test.min(), y_pred.min()), max(y_test.max(), y_pred.max())
        ax.plot([mn, mx], [mn, mx], color="#22d3ee", linewidth=1.5, linestyle="--", label="Perfect fit")
        ax.set_xlabel("Actual")
        ax.set_ylabel("Predicted")
        ax.set_title("Actual vs Predicted")
        ax.legend(fontsize=9)
        ax.grid(True, alpha=0.2)
        fig.tight_layout()
        st.pyplot(fig)

        # --- Classification ---
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("### 🤖 Classification")

        y_class = (y > y.mean()).astype(int)
        X_train_c, X_test_c, y_train_c, y_test_c = train_test_split(
            X_scaled, y_class, test_size=0.2, random_state=42
        )

        log = LogisticRegression(max_iter=1000)
        log.fit(X_train_c, y_train_c)
        acc_log = accuracy_score(y_test_c, log.predict(X_test_c))

        dt = DecisionTreeClassifier()
        dt.fit(X_train_c, y_train_c)
        acc_dt = accuracy_score(y_test_c, dt.predict(X_test_c))

        rf = RandomForestClassifier()
        rf.fit(X_train_c, y_train_c)
        acc_rf = accuracy_score(y_test_c, rf.predict(X_test_c))

        c1, c2, c3 = st.columns(3)
        c1.metric("Logistic Regression", f"{acc_log:.2%}")
        c2.metric("Decision Tree", f"{acc_dt:.2%}")
        c3.metric("Random Forest", f"{acc_rf:.2%}")

        # Model Comparison Chart
        st.markdown("### 🏆 Model Comparison")

        results = pd.DataFrame({
            "Model": ["Logistic Regression", "Decision Tree", "Random Forest"],
            "Accuracy": [acc_log, acc_dt, acc_rf]
        }).sort_values("Accuracy", ascending=True)

        fig, ax = plt.subplots(figsize=(7, 3.2))
        colors = ["#6c63ff", "#a855f7", "#22d3ee"]
        bars = ax.barh(
            results["Model"], results["Accuracy"],
            color=colors, alpha=0.85, height=0.5,
            edgecolor="none"
        )
        for bar, acc in zip(bars, results["Accuracy"]):
            ax.text(
                bar.get_width() - 0.01, bar.get_y() + bar.get_height() / 2,
                f"{acc:.2%}", va="center", ha="right",
                color="white", fontsize=11, fontweight="600"
            )
        ax.set_xlim(0, 1.0)
        ax.set_xlabel("Accuracy")
        ax.set_title("Model Accuracy Comparison")
        ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{x:.0%}"))
        ax.grid(True, axis="x", alpha=0.25)
        ax.spines["left"].set_visible(False)
        ax.tick_params(left=False)
        fig.tight_layout()
        st.pyplot(fig)

        st.markdown("<br>", unsafe_allow_html=True)
        best_model = results.iloc[-1]["Model"]
        best_acc = results.iloc[-1]["Accuracy"]
        st.markdown(f"""
            <div style="background:linear-gradient(135deg,#13131f,#1a1a35);
                        border:1px solid #2a2a55; border-radius:14px;
                        padding:18px 24px; display:flex; align-items:center; gap:14px;">
                <span style="font-size:20px; color:#6c63ff;">✦</span>
                <div>
                    <p style="margin:0; font-size:11px; text-transform:uppercase;
                               letter-spacing:0.08em; color:#6060a0; font-weight:500;">Best performer</p>
                    <p style="margin:0; font-size:17px; font-weight:600; color:#e8e8f8;">
                        {best_model}
                        <span style="font-size:13px; color:#a855f7; margin-left:8px;">
                            {best_acc:.2%} accuracy
                        </span>
                    </p>
                </div>
            </div>
        """, unsafe_allow_html=True)

else:
    st.markdown("""
        <div style="display:flex; flex-direction:column; align-items:center;
                    justify-content:center; padding: 5rem 2rem; text-align:center;">
            <div style="font-size:42px; margin-bottom:16px; opacity:0.4;">⬡</div>
            <p style="font-size:18px; font-weight:500; color:#9090c0; margin:0 0 8px 0;">
                No dataset loaded
            </p>
            <p style="font-size:13px; color:#44446a; max-width:300px; line-height:1.7; margin:0;">
                Upload a CSV file from the sidebar to start exploring your data and benchmarking ML models.
            </p>
        </div>
    """, unsafe_allow_html=True)