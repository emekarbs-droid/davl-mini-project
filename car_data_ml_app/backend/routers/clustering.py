from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app_state import state
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from scipy.cluster.hierarchy import linkage, dendrogram

router = APIRouter()

class ClusteringRequest(BaseModel):
    n_clusters: int = 3

@router.post("/kmeans")
def train_kmeans(req: ClusteringRequest):
    if hasattr(state, "preprocessed_df") and state.preprocessed_df is not None:
        df = state.preprocessed_df
    else:
        if state.df is None:
            raise HTTPException(status_code=400, detail="No dataset uploaded")
        from services.data_utils import clean_dataset
        from services.ml_utils import handle_missing_values, encode_categorical
        df = clean_dataset(state.df)
        df = handle_missing_values(df, method="mean")
        df = encode_categorical(df)
        
    num_df = df.select_dtypes(include=[np.number]).dropna()
    if num_df.shape[1] < 2:
        raise HTTPException(status_code=400, detail="Not enough features")
        
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(num_df)
    
    # Calculate elbow curve points (k=1 to 10)
    inertia = []
    for k in range(1, min(11, len(scaled_data))):
        km = KMeans(n_clusters=k, random_state=42, n_init="auto")
        km.fit(scaled_data)
        inertia.append({"k": k, "inertia": float(km.inertia_)})
        
    # Fit requested clusters
    kmeans = KMeans(n_clusters=req.n_clusters, random_state=42, n_init="auto")
    labels = kmeans.fit_predict(scaled_data)
    
    # For UI, reduce to 2D
    pca = PCA(n_components=2)
    pca_result = pca.fit_transform(scaled_data)
    
    scatter = []
    n_samples = min(200, pca_result.shape[0])
    for i in range(n_samples):
        scatter.append({
            "x": float(pca_result[i, 0]),
            "y": float(pca_result[i, 1]),
            "cluster": int(labels[i])
        })
        
    return {
        "elbow": inertia,
        "scatter": scatter
    }

@router.get("/hierarchical")
def get_hierarchical():
    if state.df is None:
        raise HTTPException(status_code=400, detail="No dataset uploaded")
        
    from services.data_utils import clean_dataset
    from services.ml_utils import handle_missing_values, encode_categorical
    df = clean_dataset(state.df)
    df = handle_missing_values(df, method="mean")
    df = encode_categorical(df)
    
    num_df = df.select_dtypes(include=[np.number]).dropna()
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(num_df)
    
    # Limit samples for dendrogram visualization clarity
    sample_size = min(30, len(scaled_data))
    indices = np.random.choice(len(scaled_data), sample_size, replace=False)
    sampled_data = scaled_data[indices]
    
    Z = linkage(sampled_data, 'ward')
    dendro = dendrogram(Z, no_plot=True)
    
    # icoord is X coordinates of branches, dcoord is Y (distance)
    return {
        "icoord": dendro['icoord'],
        "dcoord": dendro['dcoord'],
        "ivl": dendro['ivl'], # leaf labels
        "leaves": dendro['leaves']
    }
