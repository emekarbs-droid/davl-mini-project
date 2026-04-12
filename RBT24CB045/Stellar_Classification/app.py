import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import zscore
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder, StandardScaler


st.set_page_config(page_title="Stellar Classification", layout="wide")


@st.cache_data
def load_dataset(path: str) -> pd.DataFrame:
    data = pd.read_csv(path)
    data.replace(r"^\s*$", np.nan, regex=True, inplace=True)
    data.replace(-9999, np.nan, inplace=True)
    return data


@st.cache_resource
def build_artifacts(data: pd.DataFrame):
    df = data.copy()

    # Remove IDs/metadata that are not useful for predictive learning.
    drop_cols = [
        "object_ID",
        "run_ID",
        "rerun_ID",
        "cam_col",
        "field_ID",
        "plate_ID",
        "MJD",
        "fiber_ID",
        "spec_obj_ID",
    ]
    df.drop(columns=drop_cols, errors="ignore", inplace=True)

    if "class" not in df.columns:
        raise ValueError("The dataset must contain a 'class' column.")

    y = df["class"].astype(str)
    X = df.drop(columns=["class"]).select_dtypes(include=[np.number])

    # Keep only complete rows for training consistency.
    train_df = X.copy()
    train_df["class"] = y
    train_df = train_df.dropna()

    y_clean = train_df["class"]
    X_clean = train_df.drop(columns=["class"])

    if X_clean.empty:
        raise ValueError("No numeric training features available after cleaning.")

    le = LabelEncoder()
    y_encoded = le.fit_transform(y_clean)

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_clean)

    model = LogisticRegression(max_iter=1500)
    model.fit(X_scaled, y_encoded)

    pca = PCA(n_components=2, random_state=42)
    X_pca = pca.fit_transform(X_scaled)

    lda_model = None
    X_lda = None
    if len(np.unique(y_encoded)) >= 2:
        max_lda_components = min(2, X_scaled.shape[1], len(np.unique(y_encoded)) - 1)
        if max_lda_components >= 1:
            lda_model = LinearDiscriminantAnalysis(n_components=max_lda_components)
            X_lda = lda_model.fit_transform(X_scaled, y_encoded)

    z = np.abs(zscore(X_scaled, nan_policy="omit"))
    outliers = (z > 3).any(axis=1)

    cluster_count = min(3, len(np.unique(y_encoded)))
    kmeans = KMeans(n_clusters=cluster_count, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(X_scaled)

    return {
        "df_clean": df,
        "X": X_clean,
        "y": y_clean,
        "y_encoded": y_encoded,
        "scaler": scaler,
        "encoder": le,
        "model": model,
        "pca": pca,
        "X_pca": X_pca,
        "lda": lda_model,
        "X_lda": X_lda,
        "outliers": outliers,
        "clusters": clusters,
    }


st.title("Stellar Object Classification Dashboard")
st.write("Interactive exploration of the dataset and class prediction from user-provided feature values.")

try:
    raw_df = load_dataset("your_dataset.csv")
    artifacts = build_artifacts(raw_df)
except Exception as exc:
    st.error(f"Failed to prepare dataset or model: {exc}")
    st.stop()

X = artifacts["X"]
y = artifacts["y"]
y_encoded = artifacts["y_encoded"]
scaler = artifacts["scaler"]
encoder = artifacts["encoder"]
model = artifacts["model"]
pca = artifacts["pca"]
X_pca = artifacts["X_pca"]
X_lda = artifacts["X_lda"]
outliers = artifacts["outliers"]
clusters = artifacts["clusters"]

st.markdown("---")
st.header("Data Visualizations")
st.caption("Each chart includes a short explanation so you can quickly understand what it represents.")

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(
    [
        "Feature Histograms",
        "Class Distribution",
        "Correlation Heatmap",
        "Redshift by Class",
        "PCA Projection",
        "LDA Projection",
        "Outliers and Clusters",
    ]
)

with tab1:
    st.subheader("Feature Histograms")
    st.caption("Shows the distribution of each numeric feature and where values are concentrated.")
    n_cols = 3
    n_rows = int(np.ceil(len(X.columns) / n_cols))
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 4 * n_rows))
    axes = np.array(axes).reshape(-1)
    for i, feature in enumerate(X.columns):
        sns.histplot(X[feature], bins=30, kde=True, ax=axes[i], color="#2E86AB")
        axes[i].set_title(feature)
    for i in range(len(X.columns), len(axes)):
        axes[i].axis("off")
    fig.tight_layout()
    st.pyplot(fig)

with tab2:
    st.subheader("Class Distribution")
    st.caption("Displays sample counts by class to show whether classes are balanced.")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.countplot(x=y, hue=y, palette="viridis", legend=False, ax=ax)
    ax.set_xlabel("Class")
    ax.set_ylabel("Count")
    ax.set_title("Class Frequency")
    st.pyplot(fig)

with tab3:
    st.subheader("Correlation Heatmap")
    st.caption("Shows feature-to-feature linear relationships; stronger colors mean stronger correlation.")
    fig, ax = plt.subplots(figsize=(11, 8))
    sns.heatmap(X.corr(numeric_only=True), cmap="coolwarm", center=0, ax=ax)
    ax.set_title("Feature Correlation Matrix")
    st.pyplot(fig)

with tab4:
    st.subheader("Redshift by Class")
    st.caption("Compares the spread of redshift values across classes.")
    fig, ax = plt.subplots(figsize=(9, 5))
    if "red_shift" in X.columns:
        sns.boxplot(x=y, y=X["red_shift"], hue=y, palette="Set2", legend=False, ax=ax)
        ax.set_xlabel("Class")
        ax.set_ylabel("Red Shift")
        ax.set_title("Red Shift Distribution by Class")
    else:
        ax.text(0.5, 0.5, "Column 'red_shift' is not available.", ha="center", va="center")
        ax.set_axis_off()
    st.pyplot(fig)

with tab5:
    st.subheader("PCA Projection")
    st.caption("Projects all features into 2 dimensions while preserving most variance.")
    fig, ax = plt.subplots(figsize=(8, 6))
    scatter = ax.scatter(X_pca[:, 0], X_pca[:, 1], c=y_encoded, cmap="tab10", s=16, alpha=0.85)
    ax.set_xlabel("PC1")
    ax.set_ylabel("PC2")
    ax.set_title("PCA 2D Projection")
    fig.colorbar(scatter, ax=ax)
    st.pyplot(fig)
    st.write("Explained variance ratio:", np.round(pca.explained_variance_ratio_, 4).tolist())
    st.write("Total explained variance:", float(np.sum(pca.explained_variance_ratio_)))

with tab6:
    st.subheader("LDA Projection")
    st.caption("Supervised projection that emphasizes separation between known classes.")
    fig, ax = plt.subplots(figsize=(8, 6))
    if X_lda is None:
        ax.text(0.5, 0.5, "LDA is unavailable (needs at least 2 classes).", ha="center", va="center")
        ax.set_axis_off()
    elif X_lda.shape[1] == 1:
        ax.scatter(X_lda[:, 0], np.zeros_like(X_lda[:, 0]), c=y_encoded, cmap="tab10", s=16, alpha=0.85)
        ax.set_xlabel("LD1")
        ax.set_ylabel("Baseline")
        ax.set_title("LDA 1D Projection")
    else:
        scatter = ax.scatter(X_lda[:, 0], X_lda[:, 1], c=y_encoded, cmap="tab10", s=16, alpha=0.85)
        ax.set_xlabel("LD1")
        ax.set_ylabel("LD2")
        ax.set_title("LDA 2D Projection")
        fig.colorbar(scatter, ax=ax)
    st.pyplot(fig)

with tab7:
    st.subheader("Outliers and Clusters")
    st.caption("Shows outlier count and unsupervised cluster structure in PCA space.")

    left, right = st.columns(2)

    with left:
        st.metric("Detected outliers", int(np.sum(outliers)))
        fig, ax = plt.subplots(figsize=(7, 5))
        sns.boxplot(data=X, ax=ax)
        ax.tick_params(axis="x", rotation=90)
        ax.set_title("Feature-Wise Outlier View")
        st.pyplot(fig)

    with right:
        fig, ax = plt.subplots(figsize=(7, 5))
        ax.scatter(X_pca[:, 0], X_pca[:, 1], c=clusters, cmap="tab10", s=16, alpha=0.85)
        ax.set_title("KMeans Clusters on PCA")
        ax.set_xlabel("PC1")
        ax.set_ylabel("PC2")
        st.pyplot(fig)

st.markdown("---")
st.header("Prediction System")
st.caption("Enter only the most important features. Remaining features are auto-filled with dataset averages.")

default_values = X.mean(numeric_only=True).to_dict()

# Rank features using average absolute logistic regression coefficients.
feature_importance = np.abs(model.coef_).mean(axis=0)
importance_df = pd.DataFrame(
    {"Feature": X.columns, "Importance": feature_importance}
).sort_values("Importance", ascending=False)

top_k = min(8, len(X.columns))
selected_features = importance_df["Feature"].head(top_k).tolist()

st.write(f"Using top {top_k} features for manual input:")
st.dataframe(importance_df.head(top_k).reset_index(drop=True), use_container_width=True)

with st.form("predict_form"):
    columns = st.columns(4)
    user_values = {}
    for idx, feature in enumerate(selected_features):
        with columns[idx % 4]:
            user_values[feature] = st.number_input(
                label=feature,
                value=float(default_values.get(feature, 0.0)),
                format="%.6f",
                key=f"input_{idx}_{feature}",
            )

    submit_prediction = st.form_submit_button("Predict")

if submit_prediction:
    try:
        full_input = default_values.copy()
        full_input.update(user_values)
        user_df = pd.DataFrame([full_input], columns=X.columns)
        user_arr = user_df.to_numpy(dtype=np.float64)

        if not np.isfinite(user_arr).all():
            st.error("Input contains invalid numeric values.")
        else:
            user_scaled = scaler.transform(user_df)
            pred_encoded = model.predict(user_scaled)
            pred_label = encoder.inverse_transform(pred_encoded)[0]
            pred_prob = model.predict_proba(user_scaled)[0]

            st.success(f"Predicted class: {pred_label}")

            conf_df = pd.DataFrame(
                {
                    "Class": encoder.classes_,
                    "Confidence (%)": np.round(pred_prob * 100, 2),
                }
            ).sort_values("Confidence (%)", ascending=False)
            st.subheader("Confidence by Class")
            st.dataframe(conf_df, use_container_width=True)

    except Exception as exc:
        st.error(f"Prediction failed: {exc}")

st.markdown("---")
st.subheader("Reference Table: Mean Feature Values by Class")
mean_table = raw_df.groupby("class").mean(numeric_only=True).round(3)
st.dataframe(mean_table, use_container_width=True)

