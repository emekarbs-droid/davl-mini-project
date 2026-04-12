import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

from sklearn.metrics import accuracy_score, r2_score, confusion_matrix

st.set_page_config(page_title="ML Explorer", layout="centered")

st.title("🚀 ML Explorer Dashboard")

# ---------------- LOAD ----------------
@st.cache_data
def load_data():
    df = pd.read_csv("Food_Nutrition_Dataset.csv")
    df.columns = df.columns.str.strip().str.replace(" ", "_")
    return df

df = load_data()
df = df.select_dtypes(include=np.number).dropna()

st.subheader("Dataset Preview")
st.dataframe(df.head())

# ---------------- CONFIG ----------------
st.subheader("⚙️ Configuration")

target = st.selectbox("Select Target", df.columns)

features = st.multiselect(
    "Select Features",
    [col for col in df.columns if col != target],
    default=[col for col in df.columns if col != target][:3]
)

main_section = st.selectbox(
    "Select Section",
    ["EDA", "PCA", "Regression", "Classification", "Model Comparison"]
)

# ================== EDA ==================
if main_section == "EDA" and len(features) > 0:

    st.subheader("📊 EDA")

    eda_type = st.selectbox(
        "Choose Visualization",
        ["Heatmap", "Histogram", "Boxplot", "Scatter"]
    )

    if eda_type == "Heatmap":
        fig, ax = plt.subplots(figsize=(5,3))
        sns.heatmap(df[features].corr(), annot=True, cmap="coolwarm", ax=ax)
        st.pyplot(fig, use_container_width=False)

    elif eda_type == "Histogram":
        col = st.selectbox("Select Column", features)
        fig, ax = plt.subplots(figsize=(5,3))
        sns.histplot(df[col], kde=True, ax=ax)
        ax.set_title(f"Histogram of {col}")
        st.pyplot(fig, use_container_width=False)

    elif eda_type == "Boxplot":
        col = st.selectbox("Select Column", features)
        fig, ax = plt.subplots(figsize=(5,3))
        sns.boxplot(x=df[col], ax=ax)
        ax.set_title(f"Boxplot of {col}")
        st.pyplot(fig, use_container_width=False)

    elif eda_type == "Scatter":
        x_col = st.selectbox("X-axis", features)
        y_col = st.selectbox("Y-axis", features)
        fig, ax = plt.subplots(figsize=(5,3))
        ax.scatter(df[x_col], df[y_col])
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)
        ax.set_title(f"Scatter Plot: {x_col} vs {y_col}")
        st.pyplot(fig, use_container_width=False)

# ================== PCA ==================
elif main_section == "PCA" and len(features) >= 2:

    st.subheader("📉 PCA")

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df[features])

    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_scaled)

    fig, ax = plt.subplots(figsize=(5,3))
    ax.scatter(X_pca[:, 0], X_pca[:, 1])
    ax.set_title("PCA Plot")
    ax.set_xlabel("PC1")
    ax.set_ylabel("PC2")
    st.pyplot(fig, use_container_width=False)

# ================== REGRESSION ==================
elif main_section == "Regression" and len(features) > 0:

    st.subheader("📈 Regression")

    X = df[features]
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model_type = st.selectbox("Select Model", ["Linear Regression"])

    if model_type == "Linear Regression":
        model = LinearRegression()
        model.fit(X_train, y_train)
        pred = model.predict(X_test)

        st.success(f"R² Score: {r2_score(y_test, pred):.4f}")

        reg_graph = st.selectbox(
            "Select Graph",
            ["Actual vs Predicted", "Residual Plot"]
        )

        if reg_graph == "Actual vs Predicted":
            fig, ax = plt.subplots(figsize=(5,3))
            ax.scatter(y_test, pred)
            ax.set_xlabel("Actual Values")
            ax.set_ylabel("Predicted Values")
            ax.set_title("Actual vs Predicted")
            st.pyplot(fig, use_container_width=False)

        elif reg_graph == "Residual Plot":
            fig, ax = plt.subplots(figsize=(5,3))
            ax.scatter(pred, y_test - pred)
            ax.axhline(0)
            ax.set_xlabel("Predicted Values")
            ax.set_ylabel("Residuals")
            ax.set_title("Residual Plot")
            st.pyplot(fig, use_container_width=False)

# ================== CLASSIFICATION ==================
elif main_section == "Classification" and len(features) > 0:

    st.subheader("📊 Classification")

    X = df[features]
    y = pd.qcut(df[target], q=3, labels=False, duplicates='drop')

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model_type = st.selectbox(
        "Select Model",
        ["Logistic Regression", "Decision Tree", "Random Forest", "LDA"]
    )

    # ---- Logistic ----
    if model_type == "Logistic Regression":
        model = LogisticRegression(max_iter=1000)
        model.fit(X_train, y_train)
        pred = model.predict(X_test)

        st.success(f"Accuracy: {accuracy_score(y_test, pred):.4f}")

        graph = st.selectbox("Graph", ["Confusion Matrix", "Actual vs Predicted"])

        if graph == "Confusion Matrix":
            cm = confusion_matrix(y_test, pred)
            fig, ax = plt.subplots(figsize=(4,3))
            sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=ax)
            ax.set_xlabel("Predicted")
            ax.set_ylabel("Actual")
            ax.set_title("Confusion Matrix")
            st.pyplot(fig, use_container_width=False)

        elif graph == "Actual vs Predicted":
            fig, ax = plt.subplots(figsize=(5,3))
            ax.scatter(y_test, pred)
            ax.set_xlabel("Actual Values")
            ax.set_ylabel("Predicted Values")
            ax.set_title("Actual vs Predicted")
            st.pyplot(fig, use_container_width=False)

    # ---- Decision Tree ----
    elif model_type == "Decision Tree":
        model = DecisionTreeClassifier()
        model.fit(X_train, y_train)
        pred = model.predict(X_test)

        st.success(f"Accuracy: {accuracy_score(y_test, pred):.4f}")

        graph = st.selectbox("Graph", ["Feature Importance", "Tree"])

        if graph == "Feature Importance":
            fig, ax = plt.subplots(figsize=(5,3))
            ax.bar(features, model.feature_importances_)
            ax.set_ylabel("Importance")
            ax.set_title("Feature Importance")
            st.pyplot(fig, use_container_width=False)

        elif graph == "Tree":
            fig, ax = plt.subplots(figsize=(6,4))
            plot_tree(model, ax=ax)
            st.pyplot(fig, use_container_width=False)

    # ---- Random Forest ----
    elif model_type == "Random Forest":
        model = RandomForestClassifier()
        model.fit(X_train, y_train)
        pred = model.predict(X_test)

        st.success(f"Accuracy: {accuracy_score(y_test, pred):.4f}")

        fig, ax = plt.subplots(figsize=(5,3))
        ax.bar(features, model.feature_importances_)
        ax.set_ylabel("Importance")
        ax.set_title("Feature Importance")
        st.pyplot(fig, use_container_width=False)

    # ---- LDA ----
    elif model_type == "LDA":
        model = LinearDiscriminantAnalysis()
        model.fit(X_train, y_train)
        pred = model.predict(X_test)

        st.success(f"Accuracy: {accuracy_score(y_test, pred):.4f}")

        # LDA Projection Plot
        X_lda = model.transform(X_train)
        fig, ax = plt.subplots(figsize=(5,3))
        scatter = ax.scatter(X_lda[:, 0], X_lda[:, 1], c=y_train, cmap='viridis')
        ax.set_xlabel("LD1")
        ax.set_ylabel("LD2")
        ax.set_title("LDA Projection")
        plt.colorbar(scatter, ax=ax)
        st.pyplot(fig, use_container_width=False)

# ================== MODEL COMPARISON ==================
elif main_section == "Model Comparison" and len(features) > 0:

    st.subheader("📊 Model Comparison")

    X = df[features]
    y = pd.qcut(df[target], q=3, labels=False, duplicates='drop')

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    models = {
        "Logistic": LogisticRegression(max_iter=1000),
        "Decision Tree": DecisionTreeClassifier(),
        "Random Forest": RandomForestClassifier(),
        "LDA": LinearDiscriminantAnalysis()
    }

    results = {}

    for name, model in models.items():
        model.fit(X_train, y_train)
        pred = model.predict(X_test)
        results[name] = accuracy_score(y_test, pred)

    fig, ax = plt.subplots(figsize=(5,3))
    ax.bar(results.keys(), results.values())
    ax.set_ylabel("Accuracy")
    ax.set_title("Model Accuracy Comparison")
    st.pyplot(fig, use_container_width=False)

st.success("✅ Done!")