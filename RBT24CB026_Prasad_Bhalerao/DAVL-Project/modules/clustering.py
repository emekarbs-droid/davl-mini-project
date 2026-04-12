import pandas as pd
from sklearn.cluster import KMeans
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


def prepare_cluster_matrix(df: pd.DataFrame, columns: list[str]) -> tuple[pd.DataFrame, object, object]:
    """
    Subsets the data for clustering and applies median imputation and standard scaling.
    Scaling is crucial for distance-based algorithms like K-Means.
    """
    frame = df[columns].copy()
    pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )
    transformed = pipeline.fit_transform(frame)
    return frame, pipeline, transformed


def compute_elbow(x_scaled, max_k: int) -> tuple[list[int], list[float]]:
    """
    Calculates the Within-Cluster Sum of Squares (WCSS) for multiple K values.
    This helps visually identify the 'elbow' point to determine the optimal cluster count.
    """
    k_values = list(range(1, max_k + 1))
    wcss: list[float] = []
    for k in k_values:
        model = KMeans(n_clusters=k, random_state=42, n_init=10)
        model.fit(x_scaled)
        wcss.append(float(model.inertia_))
    return k_values, wcss


def fit_kmeans(x_scaled, k: int) -> tuple[KMeans, object]:
    model = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = model.fit_predict(x_scaled)
    return model, labels
