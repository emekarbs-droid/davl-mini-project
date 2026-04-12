import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import accuracy_score, r2_score, mean_squared_error

st.set_page_config(page_title="ML Explorer", layout="wide")

st.title("ML Explorer")
st.write("Data Loading, EDA, PCA, LDA, ML Models and Comparison")

# ----------------------------
# Sidebar - Upload Section
# ----------------------------
st.sidebar.header("Upload Data")
uploaded_file = st.sidebar.file_uploader(
    "Choose a CSV or Excel file",
    type=["csv", "xlsx"]
)

# Optional built-in datasets
dataset_option = st.sidebar.selectbox(
    "Or select built-in dataset",
    ["None", "heart.csv", "diabetes.csv"]
)

df = None

if uploaded_file is not None:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
    st.sidebar.success(f"Loaded: {uploaded_file.name}")

elif dataset_option != "None":
    try:
        if dataset_option.endswith(".csv"):
            df = pd.read_csv(dataset_option)
        st.sidebar.success(f"Loaded: {dataset_option}")
    except:
        st.sidebar.error(f"{dataset_option} file not found in project folder.")

if df is not None:
    # ----------------------------
    # Data Preview
    # ----------------------------
    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    st.subheader("Dataset Information")
    col1, col2 = st.columns(2)

    with col1:
        st.write("Shape:", df.shape)
        st.write("Columns:", list(df.columns))

    with col2:
        st.write("Missing Values")
        st.write(df.isnull().sum())

    st.subheader("Summary Statistics")
    st.dataframe(df.describe(include="all"))

    # ----------------------------
    # Main Interface
    # ----------------------------
    st.subheader("Train Machine Learning Models")

    target_col = st.selectbox("Select Target Column", df.columns)

    feature_cols = st.multiselect(
        "Select Features",
        [col for col in df.columns if col != target_col],
        default=[col for col in df.columns if col != target_col][:4]
    )

    task_type = st.radio("Select ML Task Type", ["Classification", "Regression"], horizontal=True)

    if task_type == "Classification":
        algorithm = st.selectbox(
            "Select Algorithm",
            ["Logistic Regression", "Decision Tree", "Random Forest", "LDA"]
        )
    else:
        algorithm = st.selectbox(
            "Select Algorithm",
            ["Linear Regression"]
        )

    # ----------------------------
    # Prepare data
    # ----------------------------
    if len(feature_cols) > 0:
        model_df = df[feature_cols + [target_col]].copy()

        # Fill missing values
        for col in model_df.columns:
            if model_df[col].dtype == "object":
                model_df[col] = model_df[col].fillna(model_df[col].mode()[0])
            else:
                model_df[col] = model_df[col].fillna(model_df[col].median())

        # Encode categorical columns
        encoders = {}
        for col in model_df.columns:
            if model_df[col].dtype == "object":
                le = LabelEncoder()
                model_df[col] = le.fit_transform(model_df[col].astype(str))
                encoders[col] = le

        X = model_df[feature_cols]
        y = model_df[target_col]

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # ----------------------------
        # EDA Section
        # ----------------------------
        st.subheader("EDA Visualizations")

        num_df = model_df.select_dtypes(include=np.number)

        if not num_df.empty:
            st.markdown("### Correlation Heatmap")
            fig, ax = plt.subplots(figsize=(12, 8))
            sns.heatmap(num_df.corr(), annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
            plt.xticks(rotation=45, ha="right")
            plt.yticks(rotation=0)
            plt.tight_layout()
            st.pyplot(fig)

        hist_col = st.selectbox("Select Column for Histogram", feature_cols, key="hist")
        fig, ax = plt.subplots()
        sns.histplot(model_df[hist_col], kde=True, ax=ax)
        ax.set_title(f"Histogram of {hist_col}")
        st.pyplot(fig)

        box_col = st.selectbox("Select Column for Box Plot", feature_cols, key="box")
        fig, ax = plt.subplots()
        sns.boxplot(x=model_df[box_col], ax=ax)
        ax.set_title(f"Box Plot of {box_col}")
        st.pyplot(fig)

        scatter_x = st.selectbox("Select X Axis", feature_cols, key="scatter_x")
        scatter_y = st.selectbox("Select Y Axis", feature_cols, key="scatter_y")

        fig, ax = plt.subplots()
        sns.scatterplot(x=model_df[scatter_x], y=model_df[scatter_y], ax=ax)
        ax.set_title(f"Scatter Plot: {scatter_x} vs {scatter_y}")
        st.pyplot(fig)

        # ----------------------------
        # PCA
        # ----------------------------
        st.subheader("PCA Visualization")
        try:
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            pca = PCA(n_components=2)
            X_pca = pca.fit_transform(X_scaled)                        

            fig, ax = plt.subplots()
            ax.scatter(X_pca[:, 0], X_pca[:, 1])
            ax.set_xlabel("PC1")
            ax.set_ylabel("PC2")
            ax.set_title("PCA Plot")
            st.pyplot(fig)
        except Exception as e:
            st.warning(f"PCA could not be generated: {e}")

        # ----------------------------
        # LDA Visualization
        # ----------------------------
        st.subheader("LDA Visualization")
        try:
            if task_type == "Classification" and len(np.unique(y)) > 1:
                lda_vis = LinearDiscriminantAnalysis(n_components=1)
                X_lda = lda_vis.fit_transform(X, y)

                fig, ax = plt.subplots()
                ax.scatter(X_lda[:, 0], y)
                ax.set_xlabel("LDA Component")
                ax.set_ylabel("Target")
                ax.set_title("LDA Plot")
                st.pyplot(fig)
            else:
                st.info("LDA visualization is available for classification datasets.")
        except Exception as e:
            st.warning(f"LDA could not be generated: {e}")

        # ----------------------------
        # Selected Algorithm Result
        # ----------------------------
        st.subheader("Selected Model Result")

        if task_type == "Classification":
            try:
                if algorithm == "Logistic Regression":
                    model = LogisticRegression(max_iter=1000)
                elif algorithm == "Decision Tree":
                    model = DecisionTreeClassifier(random_state=42)
                elif algorithm == "Random Forest":
                    model = RandomForestClassifier(random_state=42)
                elif algorithm == "LDA":
                    model = LinearDiscriminantAnalysis()

                model.fit(X_train, y_train)
                pred = model.predict(X_test)
                score = accuracy_score(y_test, pred)

                st.write(f"**{algorithm} Accuracy:** {score:.4f}")
            except Exception as e:
                st.error(f"{algorithm} could not run: {e}")

        else:
            try:
                model = LinearRegression()
                model.fit(X_train, y_train)
                pred = model.predict(X_test)
                r2 = r2_score(y_test, pred)
                mse = mean_squared_error(y_test, pred)

                st.write(f"**Linear Regression R² Score:** {r2:.4f}")
                st.write(f"**Linear Regression MSE:** {mse:.4f}")
            except Exception as e:
                st.error(f"Linear Regression could not run: {e}")

        # ----------------------------
        # Model Comparison
        # ----------------------------
        st.subheader("Model Comparison")

        if task_type == "Classification":
            comparison_results = []

            try:
                log_model = LogisticRegression(max_iter=1000)
                log_model.fit(X_train, y_train)
                pred_log = log_model.predict(X_test)
                log_score = accuracy_score(y_test, pred_log)
                comparison_results.append(["Logistic Regression", log_score])
            except:
                comparison_results.append(["Logistic Regression", 0])

            try:
                dt_model = DecisionTreeClassifier(random_state=42)
                dt_model.fit(X_train, y_train)
                pred_dt = dt_model.predict(X_test)
                dt_score = accuracy_score(y_test, pred_dt)
                comparison_results.append(["Decision Tree", dt_score])
            except:
                comparison_results.append(["Decision Tree", 0])

            try:
                rf_model = RandomForestClassifier(random_state=42)
                rf_model.fit(X_train, y_train)
                pred_rf = rf_model.predict(X_test)
                rf_score = accuracy_score(y_test, pred_rf)
                comparison_results.append(["Random Forest", rf_score])
            except:
                comparison_results.append(["Random Forest", 0])

            try:
                lda_model = LinearDiscriminantAnalysis()
                lda_model.fit(X_train, y_train)
                pred_lda = lda_model.predict(X_test)
                lda_score = accuracy_score(y_test, pred_lda)
                comparison_results.append(["LDA", lda_score])
            except:
                comparison_results.append(["LDA", 0])

            results_df = pd.DataFrame(comparison_results, columns=["Model", "Accuracy"])
            st.dataframe(results_df)

            fig, ax = plt.subplots()
            sns.barplot(x="Model", y="Accuracy", data=results_df, ax=ax)
            ax.set_title("Classification Model Comparison")
            plt.xticks(rotation=15)
            plt.tight_layout()
            st.pyplot(fig)

        else:
            comparison_results = []

            try:
                lr_model = LinearRegression()
                lr_model.fit(X_train, y_train)
                pred_lr = lr_model.predict(X_test)
                lr_score = r2_score(y_test, pred_lr)
                comparison_results.append(["Linear Regression", lr_score])
            except:
                comparison_results.append(["Linear Regression", 0])

            results_df = pd.DataFrame(comparison_results, columns=["Model", "Score"])
            st.dataframe(results_df)

            fig, ax = plt.subplots()
            sns.barplot(x="Model", y="Score", data=results_df, ax=ax)
            ax.set_title("Regression Model Comparison")
            plt.tight_layout()
            st.pyplot(fig)

    else:
        st.warning("Please select at least one feature.")

else:
    st.info("Upload a dataset from the sidebar or place heart.csv / diabetes.csv in the same folder.")