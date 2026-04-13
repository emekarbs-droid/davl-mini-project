"""
DAVL — Data Analysis & Visualization Lab
Main Streamlit Application
"""

import streamlit as st
import pandas as pd
import numpy as np
import os
import warnings

warnings.filterwarnings("ignore")

# ---------- Page Config ----------
st.set_page_config(
    page_title="DAVL — Data Analysis & Visualization Lab",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Load Custom CSS ----------
css_path = os.path.join(os.path.dirname(__file__), "assets", "style.css")
if os.path.exists(css_path):
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ---------- Imports ----------
from src.data_handler import load_dataset, get_preview, get_overview, detect_target_column, get_column_info
from src.data_quality import data_quality_summary, missing_value_analysis, detect_outliers_iqr
from src.preprocessing import (
    handle_missing_values, remove_duplicates, encode_categoricals,
    scale_features, handle_outliers_iqr, select_features,
)
from src.eda import (
    univariate_numeric_summary, univariate_categorical_summary,
    correlation_analysis, highly_correlated_pairs, distribution_analysis,
    bivariate_analysis,
)
from src.visualizations import (
    histogram, boxplot, scatterplot, correlation_heatmap,
    count_plot, violin_plot, missing_values_heatmap, missing_bar_chart,
    pairplot_matplotlib, scree_plot, scatter_2d, scatter_3d, loadings_heatmap,
)
from src.statistics import (
    descriptive_statistics, correlation_matrix, covariance_matrix,
    normality_tests, feature_importance_by_correlation,
)
from src.pca_analysis import run_pca
from src.lda_analysis import run_lda, can_apply_lda
from src.factor_analysis import run_factor_analysis, can_apply_factor_analysis
from src.insights import generate_insights, format_insights_markdown
from src.report_export import (
    export_dataframe_csv, export_dataframe_excel,
    generate_analysis_report, export_insights_json,
)

# ---------- Session State Init ----------
if "df" not in st.session_state:
    st.session_state.df = None
if "df_processed" not in st.session_state:
    st.session_state.df_processed = None
if "target_col" not in st.session_state:
    st.session_state.target_col = None
if "overview" not in st.session_state:
    st.session_state.overview = None
if "quality" not in st.session_state:
    st.session_state.quality = None
if "insights" not in st.session_state:
    st.session_state.insights = None


# ============================================================
#  SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("## 📊 DAVL")
    st.markdown("**Data Analysis & Visualization Lab**")
    st.markdown("---")

    uploaded_file = st.file_uploader(
        "📂 Upload Dataset",
        type=["csv", "xls", "xlsx"],
        help="Upload a CSV or Excel file to begin analysis",
    )

    if uploaded_file is not None:
        df = load_dataset(uploaded_file)
        if df is not None:
            st.session_state.df = df
            st.session_state.overview = get_overview(df)

            # Target detection
            detected = detect_target_column(df)
            target_options = ["None (no target)"] + df.columns.tolist()
            default_idx = target_options.index(detected) if detected in target_options else 0

            selected_target = st.selectbox(
                "🎯 Target Column",
                target_options,
                index=default_idx,
                help="Select the target/label column for supervised analysis",
            )
            st.session_state.target_col = None if selected_target == "None (no target)" else selected_target

            # Quick stats
            st.markdown("---")
            st.markdown("### 📋 Quick Info")
            ov = st.session_state.overview
            st.markdown(f"**Rows:** {ov['rows']:,}")
            st.markdown(f"**Columns:** {ov['columns']}")
            st.markdown(f"**Memory:** {ov['memory_usage']}")
            st.markdown(f"**Missing:** {ov['missing_total']:,}")
            st.markdown(f"**Duplicates:** {ov['duplicate_rows']:,}")
            if st.session_state.target_col:
                st.markdown(f"**Target:** {st.session_state.target_col}")

            st.success(f"✅ Loaded: {uploaded_file.name}")

    st.markdown("---")
    st.markdown(
        "<div style='text-align:center; color:#5a6478; font-size:0.75rem;'>"
        "DAVL v1.0 • Built with Streamlit</div>",
        unsafe_allow_html=True,
    )


# ============================================================
#  MAIN CONTENT
# ============================================================
if st.session_state.df is None:
    # Landing page
    st.markdown(
        """
        <div style="text-align:center; padding: 80px 20px;">
            <h1 style="font-size:3rem; margin-bottom:0.5rem;">📊 DAVL</h1>
            <h2 style="font-size:1.5rem; color:#8892a8; font-weight:400; margin-bottom:2rem;">
                Data Analysis & Visualization Lab
            </h2>
            <p style="color:#5a6478; font-size:1.1rem; max-width:700px; margin:0 auto 2rem;">
                Upload a CSV or Excel dataset to get a complete automated analysis — 
                data quality checks, EDA, statistical summaries, PCA, LDA, factor analysis, 
                and auto-generated insights.
            </p>
            <div style="display:flex; justify-content:center; gap:30px; flex-wrap:wrap; margin-top:40px;">
                <div style="background:linear-gradient(145deg,#1a1f35,#151a2e); border:1px solid #2a3050; border-radius:12px; padding:20px 30px; min-width:160px;">
                    <div style="font-size:2rem;">🔍</div>
                    <div style="color:#e8ecf4; font-weight:600; margin-top:8px;">Data Quality</div>
                </div>
                <div style="background:linear-gradient(145deg,#1a1f35,#151a2e); border:1px solid #2a3050; border-radius:12px; padding:20px 30px; min-width:160px;">
                    <div style="font-size:2rem;">📈</div>
                    <div style="color:#e8ecf4; font-weight:600; margin-top:8px;">EDA & Charts</div>
                </div>
                <div style="background:linear-gradient(145deg,#1a1f35,#151a2e); border:1px solid #2a3050; border-radius:12px; padding:20px 30px; min-width:160px;">
                    <div style="font-size:2rem;">📐</div>
                    <div style="color:#e8ecf4; font-weight:600; margin-top:8px;">Statistics</div>
                </div>
                <div style="background:linear-gradient(145deg,#1a1f35,#151a2e); border:1px solid #2a3050; border-radius:12px; padding:20px 30px; min-width:160px;">
                    <div style="font-size:2rem;">🧮</div>
                    <div style="color:#e8ecf4; font-weight:600; margin-top:8px;">PCA / LDA</div>
                </div>
                <div style="background:linear-gradient(145deg,#1a1f35,#151a2e); border:1px solid #2a3050; border-radius:12px; padding:20px 30px; min-width:160px;">
                    <div style="font-size:2rem;">💡</div>
                    <div style="color:#e8ecf4; font-weight:600; margin-top:8px;">Auto Insights</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.stop()

# ---------- Dataset loaded — show tabs ----------
df = st.session_state.df
target_col = st.session_state.target_col
overview = st.session_state.overview

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
    "📊 Overview",
    "🔍 Data Quality",
    "🛠️ Preprocessing",
    "📈 EDA & Visualizations",
    "📐 Statistics",
    "🧮 PCA Analysis",
    "📉 LDA Analysis",
    "🔬 Factor Analysis",
    "💡 Insights & Report",
])


# ============================================================
#  TAB 1: OVERVIEW
# ============================================================
with tab1:
    st.header("📊 Dataset Overview")

    # Metric cards
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Rows", f"{overview['rows']:,}")
    col2.metric("Columns", overview['columns'])
    col3.metric("Numeric", overview['num_numeric'])
    col4.metric("Categorical", overview['num_categorical'])
    col5.metric("Memory", overview['memory_usage'])

    st.markdown("---")

    # Preview tabs
    preview_tab1, preview_tab2, preview_tab3 = st.tabs(["Head", "Tail", "Random Sample"])
    previews = get_preview(df)
    with preview_tab1:
        st.dataframe(previews["head"], use_container_width=True, height=350)
    with preview_tab2:
        st.dataframe(previews["tail"], use_container_width=True, height=350)
    with preview_tab3:
        st.dataframe(previews["sample"], use_container_width=True, height=350)

    st.markdown("---")

    # Column details
    st.subheader("📋 Column Details")
    col_info = get_column_info(df)
    st.dataframe(col_info, use_container_width=True, height=400)

    # Data types summary
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("📦 Data Types")
        for dtype, count in overview["dtypes_summary"].items():
            st.markdown(f"- **{dtype}**: {count} columns")
    with col_b:
        st.subheader("🔢 Unique Values")
        unique_df = pd.DataFrame({
            "Column": overview["unique_counts"].index,
            "Unique Values": overview["unique_counts"].values,
        })
        st.dataframe(unique_df, use_container_width=True, height=300)


# ============================================================
#  TAB 2: DATA QUALITY
# ============================================================
with tab2:
    st.header("🔍 Data Quality Analysis")

    quality = data_quality_summary(df, target_col)
    st.session_state.quality = quality

    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    missing_cols_count = (quality["missing_values"]["Missing Count"] > 0).sum()
    col1.metric("Columns with Missing", missing_cols_count)
    col2.metric("Duplicate Rows", quality["duplicates"]["duplicate_count"])
    col3.metric("Constant Columns", len(quality["constant_columns"]))
    col4.metric("High Cardinality", len(quality["high_cardinality"]))

    st.markdown("---")

    # Missing values
    st.subheader("❌ Missing Values")
    missing_df = quality["missing_values"]
    cols_missing = missing_df[missing_df["Missing Count"] > 0]
    if not cols_missing.empty:
        st.dataframe(cols_missing, use_container_width=True)
        # Missing bar chart
        fig = missing_bar_chart(df)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
        # Missing heatmap
        fig_hm = missing_values_heatmap(df)
        if fig_hm:
            with st.expander("🔥 Missing Values Heatmap"):
                st.plotly_chart(fig_hm, use_container_width=True)
    else:
        st.success("✅ No missing values in the dataset!")

    st.markdown("---")

    # Duplicates
    st.subheader("📑 Duplicate Rows")
    dup = quality["duplicates"]
    if dup["duplicate_count"] > 0:
        st.warning(f"Found **{dup['duplicate_count']}** duplicate rows ({dup['duplicate_percentage']}%)")
        with st.expander("View duplicate rows"):
            st.dataframe(dup["duplicate_rows"].head(100), use_container_width=True)
    else:
        st.success("✅ No duplicate rows found.")

    st.markdown("---")

    # Outliers
    st.subheader("📍 Outlier Detection (IQR)")
    outliers = quality["outliers"]
    if not outliers.empty:
        cols_with_outliers = outliers[outliers["Outlier Count"] > 0]
        if not cols_with_outliers.empty:
            st.dataframe(cols_with_outliers, use_container_width=True)
        else:
            st.success("✅ No outliers detected.")
    else:
        st.info("No numeric columns to check for outliers.")

    # Constant & High Cardinality
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("⚪ Constant Columns")
        if quality["constant_columns"]:
            for col_name in quality["constant_columns"]:
                st.markdown(f"- `{col_name}`")
        else:
            st.success("✅ No constant columns.")

    with col_b:
        st.subheader("🔠 High Cardinality")
        if quality["high_cardinality"]:
            for col_name in quality["high_cardinality"]:
                st.markdown(f"- `{col_name}` ({df[col_name].nunique()} unique)")
        else:
            st.success("✅ No high cardinality columns.")

    # Class imbalance
    if quality["class_imbalance"]:
        st.markdown("---")
        st.subheader("⚖️ Class Imbalance")
        ci = quality["class_imbalance"]
        if ci["is_imbalanced"]:
            st.warning(f"⚠️ Class imbalance detected (ratio: {ci['imbalance_ratio']}:1)")
        else:
            st.success(f"✅ Classes are balanced (ratio: {ci['imbalance_ratio']}:1)")

        ci_df = pd.DataFrame({
            "Class": list(ci["class_distribution"].keys()),
            "Count": list(ci["class_distribution"].values()),
            "Percentage": [f"{v}%" for v in ci["class_percentages"].values()],
        })
        st.dataframe(ci_df, use_container_width=True)

        # Class distribution chart
        fig = count_plot(df, target_col)
        st.plotly_chart(fig, use_container_width=True)


# ============================================================
#  TAB 3: PREPROCESSING
# ============================================================
with tab3:
    st.header("🛠️ Data Preprocessing")
    st.info("Apply transformations step by step. Each step operates on the result of previous steps.")

    # Initialize processed df
    if st.session_state.df_processed is None:
        st.session_state.df_processed = df.copy()

    work_df = st.session_state.df_processed

    col_left, col_right = st.columns([1, 1])

    with col_left:
        st.subheader("1️⃣ Handle Missing Values")
        missing_strategy = st.selectbox(
            "Strategy", ["auto", "mean", "median", "mode", "drop_rows", "drop_cols"],
            help="auto = median for numeric, mode for categorical",
        )
        if st.button("Apply Missing Value Handler", key="btn_missing"):
            with st.spinner("Processing..."):
                work_df, changes = handle_missing_values(work_df, missing_strategy)
                st.session_state.df_processed = work_df
                for c in changes:
                    st.write(f"✅ {c}")

    with col_right:
        st.subheader("2️⃣ Remove Duplicates")
        if st.button("Remove Duplicates", key="btn_dup"):
            with st.spinner("Processing..."):
                work_df, changes = remove_duplicates(work_df)
                st.session_state.df_processed = work_df
                for c in changes:
                    st.write(f"✅ {c}")

    st.markdown("---")

    col_left2, col_right2 = st.columns([1, 1])

    with col_left2:
        st.subheader("3️⃣ Handle Outliers")
        outlier_method = st.selectbox("Method", ["clip", "remove"], key="outlier_method")
        if st.button("Handle Outliers", key="btn_outlier"):
            with st.spinner("Processing..."):
                work_df, changes = handle_outliers_iqr(work_df, method=outlier_method)
                st.session_state.df_processed = work_df
                for c in changes:
                    st.write(f"✅ {c}")

    with col_right2:
        st.subheader("4️⃣ Encode Categoricals")
        encode_method = st.selectbox("Method", ["label", "onehot"], key="encode_method")
        if st.button("Encode Categoricals", key="btn_encode"):
            with st.spinner("Processing..."):
                work_df, changes, encoders = encode_categoricals(work_df, encode_method)
                st.session_state.df_processed = work_df
                for c in changes:
                    st.write(f"✅ {c}")

    st.markdown("---")

    col_left3, col_right3 = st.columns([1, 1])

    with col_left3:
        st.subheader("5️⃣ Feature Scaling")
        if st.button("Apply StandardScaler", key="btn_scale"):
            with st.spinner("Scaling..."):
                work_df, changes = scale_features(work_df)
                st.session_state.df_processed = work_df
                for c in changes:
                    st.write(f"✅ {c}")

    with col_right3:
        st.subheader("6️⃣ Feature Selection")
        if st.button("Auto Feature Selection", key="btn_feat_sel"):
            with st.spinner("Selecting features..."):
                work_df, changes, dropped = select_features(work_df, target_col)
                st.session_state.df_processed = work_df
                for c in changes:
                    st.write(f"✅ {c}")

    st.markdown("---")

    # Show processed data preview
    st.subheader("📋 Processed Dataset Preview")
    col_m1, col_m2, col_m3 = st.columns(3)
    col_m1.metric("Rows", f"{len(work_df):,}")
    col_m2.metric("Columns", work_df.shape[1])
    col_m3.metric("Missing", work_df.isnull().sum().sum())

    st.dataframe(work_df.head(20), use_container_width=True, height=350)

    # Reset button
    col_reset, col_download = st.columns(2)
    with col_reset:
        if st.button("🔄 Reset to Original", key="btn_reset"):
            st.session_state.df_processed = df.copy()
            st.rerun()
    with col_download:
        csv_data = export_dataframe_csv(work_df)
        st.download_button(
            "⬇️ Download Processed CSV",
            data=csv_data,
            file_name="processed_dataset.csv",
            mime="text/csv",
        )


# ============================================================
#  TAB 4: EDA & VISUALIZATIONS
# ============================================================
with tab4:
    st.header("📈 Exploratory Data Analysis")

    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()

    eda_tab1, eda_tab2, eda_tab3, eda_tab4, eda_tab5 = st.tabs([
        "Univariate", "Bivariate", "Multivariate", "Correlation", "Distribution",
    ])

    # --- Univariate ---
    with eda_tab1:
        st.subheader("📊 Univariate Analysis")

        if numeric_cols:
            st.markdown("#### Numeric Columns")
            uni_summary = univariate_numeric_summary(df)
            st.dataframe(uni_summary, use_container_width=True)

            selected_num_col = st.selectbox("Select numeric column", numeric_cols, key="uni_num")
            col_hist, col_box = st.columns(2)
            with col_hist:
                st.plotly_chart(histogram(df, selected_num_col), use_container_width=True)
            with col_box:
                st.plotly_chart(boxplot(df, selected_num_col), use_container_width=True)

            st.plotly_chart(violin_plot(df, selected_num_col), use_container_width=True)

        if cat_cols:
            st.markdown("#### Categorical Columns")
            cat_summaries = univariate_categorical_summary(df)

            selected_cat_col = st.selectbox("Select categorical column", cat_cols, key="uni_cat")
            if selected_cat_col in cat_summaries:
                info = cat_summaries[selected_cat_col]
                col_a, col_b, col_c = st.columns(3)
                col_a.metric("Unique Values", info["num_unique"])
                col_b.metric("Top Value", str(info["top_value"]))
                col_c.metric("Top Frequency", info["top_frequency"])

                st.plotly_chart(count_plot(df, selected_cat_col), use_container_width=True)

    # --- Bivariate ---
    with eda_tab2:
        st.subheader("🔗 Bivariate Analysis")

        if len(numeric_cols) >= 2:
            col_x, col_y = st.columns(2)
            with col_x:
                x_col = st.selectbox("X-axis", numeric_cols, index=0, key="bi_x")
            with col_y:
                y_col = st.selectbox("Y-axis", numeric_cols, index=min(1, len(numeric_cols)-1), key="bi_y")

            color_opt = st.selectbox(
                "Color by (optional)", ["None"] + cat_cols + numeric_cols,
                key="bi_color",
            )
            color_col = None if color_opt == "None" else color_opt

            st.plotly_chart(scatterplot(df, x_col, y_col, color_by=color_col), use_container_width=True)

        if target_col and cat_cols:
            st.markdown("#### Numeric by Category")
            if numeric_cols:
                num_for_box = st.selectbox("Numeric column", numeric_cols, key="bi_box_num")
                group_col = st.selectbox("Group by", cat_cols, key="bi_box_cat")
                st.plotly_chart(boxplot(df, num_for_box, group_by=group_col), use_container_width=True)

    # --- Multivariate ---
    with eda_tab3:
        st.subheader("🌐 Multivariate Analysis")

        if len(numeric_cols) >= 2:
            max_pair_cols = min(6, len(numeric_cols))
            pair_cols = st.multiselect(
                "Select columns for pair plot (max 6)",
                numeric_cols,
                default=numeric_cols[:max_pair_cols],
                key="pair_cols",
            )

            hue_opt = st.selectbox(
                "Color by", ["None"] + cat_cols,
                key="pair_hue",
            )
            hue_col = None if hue_opt == "None" else hue_opt

            if pair_cols and len(pair_cols) >= 2:
                with st.spinner("Generating pair plot..."):
                    fig = pairplot_matplotlib(df, columns=pair_cols, hue=hue_col)
                    if fig:
                        st.pyplot(fig)
                    else:
                        st.warning("Need at least 2 numeric columns for pair plot.")
        else:
            st.info("Need at least 2 numeric columns for multivariate analysis.")

    # --- Correlation ---
    with eda_tab4:
        st.subheader("🔥 Correlation Analysis")

        if len(numeric_cols) >= 2:
            corr_method = st.selectbox("Method", ["pearson", "spearman", "kendall"], key="corr_method")
            corr = correlation_analysis(df, method=corr_method)

            if not corr.empty:
                st.plotly_chart(correlation_heatmap(corr), use_container_width=True, key="eda_corr_heatmap")

                # Highly correlated pairs
                high_corr = highly_correlated_pairs(df, threshold=0.7)
                if not high_corr.empty:
                    st.subheader("🔗 Highly Correlated Pairs (|r| > 0.7)")
                    st.dataframe(high_corr, use_container_width=True)
                else:
                    st.success("No highly correlated pairs above threshold.")
        else:
            st.info("Need at least 2 numeric columns for correlation analysis.")

    # --- Distribution ---
    with eda_tab5:
        st.subheader("📊 Distribution Analysis")
        dist_results = distribution_analysis(df)
        if not dist_results.empty:
            st.dataframe(dist_results, use_container_width=True)

            # Histogram overlay
            if numeric_cols:
                dist_col = st.selectbox("Column for distribution", numeric_cols, key="dist_col")
                fig = histogram(df, dist_col, bins=40)
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Insufficient data for distribution analysis.")


# ============================================================
#  TAB 5: STATISTICS
# ============================================================
with tab5:
    st.header("📐 Statistical Summary")

    stat_tab1, stat_tab2, stat_tab3, stat_tab4 = st.tabs([
        "Descriptive Stats", "Correlation Matrix", "Covariance Matrix", "Normality Tests",
    ])

    with stat_tab1:
        st.subheader("📊 Descriptive Statistics")
        desc = descriptive_statistics(df)
        if not desc.empty:
            st.dataframe(desc, use_container_width=True, height=500)
        else:
            st.info("No numeric columns for descriptive statistics.")

    with stat_tab2:
        st.subheader("🔗 Correlation Matrix")
        corr_m = st.selectbox("Method", ["pearson", "spearman", "kendall"], key="stat_corr_method")
        corr_mat = correlation_matrix(df, method=corr_m)
        if not corr_mat.empty:
            st.dataframe(corr_mat, use_container_width=True)
            st.plotly_chart(correlation_heatmap(corr_mat), use_container_width=True, key="stat_corr_heatmap")
        else:
            st.info("Need at least 2 numeric columns.")

    with stat_tab3:
        st.subheader("📦 Covariance Matrix")
        cov_mat = covariance_matrix(df)
        if not cov_mat.empty:
            st.dataframe(cov_mat, use_container_width=True)
        else:
            st.info("Need at least 2 numeric columns.")

    with stat_tab4:
        st.subheader("🔔 Normality Tests")
        norm = normality_tests(df)
        if not norm.empty:
            st.dataframe(norm, use_container_width=True)
        else:
            st.info("Insufficient data for normality tests.")

    # Feature importance
    if target_col and target_col in df.select_dtypes(include=np.number).columns:
        st.markdown("---")
        st.subheader("⭐ Feature Importance (by Correlation)")
        fi = feature_importance_by_correlation(df, target_col)
        if not fi.empty:
            st.dataframe(fi, use_container_width=True)


# ============================================================
#  TAB 6: PCA ANALYSIS
# ============================================================
with tab6:
    st.header("🧮 PCA Analysis")

    numeric_cols_pca = df.select_dtypes(include=np.number).columns.tolist()
    if len(numeric_cols_pca) < 2:
        st.warning("Need at least 2 numeric features for PCA analysis.")
    else:
        n_comp = st.slider(
            "Number of components",
            min_value=2,
            max_value=min(len(numeric_cols_pca), df.shape[0]),
            value=min(len(numeric_cols_pca), df.shape[0]),
            key="pca_n_comp",
        )

        with st.spinner("Running PCA..."):
            pca_results = run_pca(df, target_col, n_components=n_comp)

        if "error" in pca_results:
            st.error(pca_results["error"])
        else:
            # Metrics
            col1, col2, col3 = st.columns(3)
            col1.metric("Components", pca_results["n_components"])
            col2.metric("Optimal (95% var)", pca_results["optimal_components"])
            cum_var = pca_results["cumulative_variance"]
            col3.metric("Var (2 PCs)", f"{cum_var[1]*100:.1f}%" if len(cum_var) > 1 else "N/A")

            st.markdown("---")

            # Variance table
            st.subheader("📊 Explained Variance")
            st.dataframe(pca_results["variance_table"], use_container_width=True)

            # Scree Plot
            fig_scree = scree_plot(pca_results["explained_variance"], "PCA Scree Plot")
            st.plotly_chart(fig_scree, use_container_width=True, key="pca_scree_plot")

            st.markdown("---")

            # PCA Scatter
            st.subheader("🔵 PCA Projection")
            transformed = pca_results["transformed"]
            labels = pca_results["labels"]
            label_str = [str(l) for l in labels] if labels is not None else None

            pca_col1, pca_col2 = st.columns(2)
            with pca_col1:
                fig_2d = scatter_2d(
                    transformed[:, 0], transformed[:, 1],
                    labels=label_str,
                    title="PCA — 2D Projection",
                )
                st.plotly_chart(fig_2d, use_container_width=True, key="pca_2d_projection")

            with pca_col2:
                if transformed.shape[1] >= 3:
                    fig_3d = scatter_3d(
                        transformed[:, 0], transformed[:, 1], transformed[:, 2],
                        labels=label_str,
                        title="PCA — 3D Projection",
                    )
                    st.plotly_chart(fig_3d, use_container_width=True, key="pca_3d_projection")

            st.markdown("---")

            # Loadings
            st.subheader("📋 Component Loadings")
            display_loadings = pca_results["loadings"].iloc[:, :min(10, pca_results["n_components"])]
            st.plotly_chart(loadings_heatmap(display_loadings, "PCA Component Loadings"), use_container_width=True)
            with st.expander("View loadings table"):
                st.dataframe(pca_results["loadings"], use_container_width=True)


# ============================================================
#  TAB 7: LDA ANALYSIS
# ============================================================
with tab7:
    st.header("📉 LDA Analysis")

    can_lda, lda_msg = can_apply_lda(df, target_col)

    if not can_lda:
        st.warning(lda_msg)
    else:
        with st.spinner("Running LDA..."):
            lda_results = run_lda(df, target_col)

        if "error" in lda_results:
            st.error(lda_results["error"])
        else:
            col1, col2 = st.columns(2)
            col1.metric("LDA Components", lda_results["n_components"])
            col2.metric("Classes", len(lda_results["class_names"]))

            st.markdown("---")

            # Explained variance
            if lda_results["explained_variance_ratio"] is not None:
                st.subheader("📊 Explained Variance Ratio")
                ev_df = pd.DataFrame({
                    "Component": [f"LD{i+1}" for i in range(len(lda_results["explained_variance_ratio"]))],
                    "Variance Ratio": (lda_results["explained_variance_ratio"] * 100).round(2),
                })
                st.dataframe(ev_df, use_container_width=True)

            # LDA Scatter
            st.subheader("🔵 LDA Projection")
            transformed = lda_results["transformed"]
            labels = [str(l) for l in lda_results["labels"]]

            if transformed.shape[1] >= 2:
                lda_col1, lda_col2 = st.columns(2)
                with lda_col1:
                    fig_2d = scatter_2d(
                        transformed[:, 0], transformed[:, 1],
                        labels=labels, title="LDA — 2D Projection",
                    )
                    st.plotly_chart(fig_2d, use_container_width=True, key="lda_2d_projection")
                with lda_col2:
                    if transformed.shape[1] >= 3:
                        fig_3d = scatter_3d(
                            transformed[:, 0], transformed[:, 1], transformed[:, 2],
                            labels=labels, title="LDA — 3D Projection",
                        )
                        st.plotly_chart(fig_3d, use_container_width=True, key="lda_3d_projection")
            elif transformed.shape[1] == 1:
                fig = histogram(
                    pd.DataFrame({"LD1": transformed[:, 0], "Class": labels}),
                    "LD1", color_by="Class",
                )
                st.plotly_chart(fig, use_container_width=True)

            st.markdown("---")

            # LDA Coefficients
            st.subheader("📋 LDA Coefficients")
            st.plotly_chart(
                loadings_heatmap(lda_results["coefficients"], "LDA Discriminant Weights"),
                use_container_width=True,
            )
            with st.expander("View coefficients table"):
                st.dataframe(lda_results["coefficients"], use_container_width=True)


# ============================================================
#  TAB 8: FACTOR ANALYSIS
# ============================================================
with tab8:
    st.header("🔬 Factor Analysis")

    can_fa, fa_msg = can_apply_factor_analysis(df)

    if not can_fa:
        st.warning(fa_msg)
    else:
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            n_factors_input = st.number_input(
                "Number of factors (0 = auto)",
                min_value=0, max_value=df.select_dtypes(include=np.number).shape[1] - 1,
                value=0, key="fa_n_factors",
            )
        with col_f2:
            rotation = st.selectbox("Rotation", ["varimax", "promax", "oblimin", "quartimax"], key="fa_rotation")

        n_factors = None if n_factors_input == 0 else int(n_factors_input)

        with st.spinner("Running Factor Analysis..."):
            fa_results = run_factor_analysis(df, n_factors=n_factors, rotation=rotation)

        if "error" in fa_results:
            st.error(fa_results["error"])
        else:
            # Adequacy tests
            col_a, col_b, col_c = st.columns(3)
            bartlett = fa_results["bartlett"]
            kmo = fa_results["kmo"]
            col_a.metric("Optimal Factors", fa_results["optimal_factors"])
            col_b.metric("KMO", kmo["overall"] if kmo["overall"] else "N/A")
            col_c.metric(
                "Bartlett's Test",
                "✅ Significant" if bartlett.get("significant") else "❌ Not Significant",
            )

            st.markdown("---")

            # Scree plot
            st.subheader("📊 Scree Plot")
            if len(fa_results["eigenvalues"]) > 0:
                # Normalize eigenvalues for display
                ev = fa_results["eigenvalues"]
                ev_ratio = ev / ev.sum()
                fig = scree_plot(ev_ratio, "Factor Analysis Scree Plot")
                st.plotly_chart(fig, use_container_width=True, key="fa_scree_plot")

            # Variance explained
            st.subheader("📊 Variance Explained")
            st.dataframe(fa_results["variance"], use_container_width=True)

            st.markdown("---")

            # Factor loadings
            st.subheader("📋 Factor Loadings")
            st.plotly_chart(
                loadings_heatmap(fa_results["loadings"], f"Factor Loadings ({rotation} rotation)"),
                use_container_width=True,
            )
            with st.expander("View loadings table"):
                st.dataframe(fa_results["loadings"], use_container_width=True)

            # Communalities
            st.subheader("🔢 Communalities")
            st.dataframe(fa_results["communalities"], use_container_width=True)


# ============================================================
#  TAB 9: INSIGHTS & REPORT
# ============================================================
with tab9:
    st.header("💡 Analyst Insights & Report")

    with st.spinner("Generating insights..."):
        insights = generate_insights(df, target_col)
        st.session_state.insights = insights

    # Display insights by category
    sections = {
        "key_observations": ("📋 Key Observations", "info"),
        "data_quality": ("🔍 Data Quality Issues", "warning"),
        "important_features": ("⭐ Important Features", "info"),
        "correlations": ("🔗 Correlation Insights", "info"),
        "redundant_columns": ("🗑️ Redundant Columns", "warning"),
        "preprocessing_suggestions": ("🔧 Preprocessing Suggestions", "info"),
    }

    for key, (title, _) in sections.items():
        items = insights.get(key, [])
        if items:
            st.subheader(title)
            for item in items:
                st.markdown(item)
            st.markdown("---")

    # Export section
    st.subheader("⬇️ Export Results")

    quality = st.session_state.quality or data_quality_summary(df, target_col)
    report_md = generate_analysis_report(df, overview, quality, insights, target_col)

    col_d1, col_d2, col_d3, col_d4 = st.columns(4)

    with col_d1:
        st.download_button(
            "📄 Download Report (MD)",
            data=report_md,
            file_name="davl_analysis_report.md",
            mime="text/markdown",
        )

    with col_d2:
        csv_bytes = export_dataframe_csv(df)
        st.download_button(
            "📊 Download Dataset (CSV)",
            data=csv_bytes,
            file_name="dataset.csv",
            mime="text/csv",
        )

    with col_d3:
        if st.session_state.df_processed is not None:
            proc_csv = export_dataframe_csv(st.session_state.df_processed)
            st.download_button(
                "🛠️ Processed Data (CSV)",
                data=proc_csv,
                file_name="processed_dataset.csv",
                mime="text/csv",
            )

    with col_d4:
        insights_json = export_insights_json(insights)
        st.download_button(
            "💡 Insights (JSON)",
            data=insights_json,
            file_name="davl_insights.json",
            mime="application/json",
        )

    # Show full report preview
    with st.expander("📄 Preview Full Report"):
        st.markdown(report_md)
