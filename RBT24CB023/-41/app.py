import streamlit as st
import pandas as pd
from ml_pipeline import preprocess_data, run_models, detect_problem_type, apply_pca
from utils import plot_heatmap, plot_histogram, plot_boxplot, plot_scatter

st.set_page_config(page_title="Auto ML Dashboard", layout="wide")

st.title("Machine Learning Dashboard")

# Upload file
file = st.file_uploader("Upload CSV File", type=["csv"])

if file:
    df = pd.read_csv(file)

    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    st.subheader("📊 Dataset Preview")
    st.dataframe(df.head())

    st.write("Shape:", df.shape)
    st.write("Columns:", list(df.columns))

    # Target selection
    target = st.selectbox("Select Target Column", df.columns)

    # Sidebar controls
    st.sidebar.header("Controls")
    show_eda = st.sidebar.button("Run EDA")
    run_model_btn = st.sidebar.button("Run Models")

    # EDA Section
    if show_eda:
     st.header("📊 EDA")

    # Get numeric columns
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
    numeric_cols = [col for col in numeric_cols if "unnamed" not in col.lower()]

    if len(numeric_cols) == 0:
        st.warning("No numeric columns available for EDA")
    else:
        # Histogram
        st.subheader("Histogram")
        col = st.selectbox("Select column for histogram", numeric_cols)
        plot_histogram(df, col)

        # Boxplot
        st.subheader("Boxplot")
        plot_boxplot(df[numeric_cols])

        # Scatter Plot
        if len(numeric_cols) >= 2:
            st.subheader("Scatter Plot")
            x_col = st.selectbox("X-axis", numeric_cols, key="x")
            y_col = st.selectbox("Y-axis", numeric_cols, key="y")
            plot_scatter(df, x_col, y_col)

        # Heatmap
        st.subheader("Heatmap")
        plot_heatmap(df[numeric_cols])

        # ✅ PCA SECTION (ADD THIS)
        st.subheader("📉 PCA Visualization")

        from ml_pipeline import apply_pca
        from sklearn.preprocessing import StandardScaler
        import matplotlib.pyplot as plt

        try:
            df_clean = df[numeric_cols].dropna()

            if df_clean.shape[1] >= 2:
                scaler = StandardScaler()
                X_scaled = scaler.fit_transform(df_clean)

                X_pca = apply_pca(X_scaled)

                fig, ax = plt.subplots()
                ax.scatter(X_pca[:, 0], X_pca[:, 1])
                ax.set_xlabel("PC1")
                ax.set_ylabel("PC2")
                ax.set_title("PCA Plot")

                st.pyplot(fig)
            else:
                st.warning("Not enough columns for PCA")

        except Exception as e:
            st.error(f"PCA Error: {e}")

    # Model Section
    if run_model_btn:
        st.header("🤖 Model Training")

        with st.spinner("Training models..."):
            X, y = preprocess_data(df, target)
            problem_type = detect_problem_type(y)

            results = run_models(X, y, problem_type)

        st.subheader("📊 Results")
        st.write(results)

        # Bar chart
        st.bar_chart(results)

        best_model = max(results, key=results.get)
        st.success(f"🏆 Best Model: {best_model}")