from fastapi import APIRouter, HTTPException
from app_state import state
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

router = APIRouter()

@router.get("/")
def get_pca():
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
        
    num_df = df.select_dtypes(include=[np.number]).dropna(axis=1, how='any') # ensure no nan
    
    if num_df.shape[1] < 2:
        raise HTTPException(status_code=400, detail="Not enough features for PCA")
        
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(num_df)
    
    pca = PCA()
    pca.fit(scaled_data)
    transformed = pca.transform(scaled_data)
    
    eigenvalues = pca.explained_variance_.tolist()
    explained_variance = pca.explained_variance_ratio_.tolist()
    
    components = pca.components_.tolist()
    
    # Prepare 2d scatter points
    scatter_points = []
    # Sample down to 200 points for frontend rendering speed if large
    n_samples = min(200, transformed.shape[0])
    for i in range(n_samples):
        scatter_points.append({
            "pc1": float(transformed[i, 0]),
            "pc2": float(transformed[i, 1] if transformed.shape[1] > 1 else 0)
        })
        
    scree_points = [{"component": i+1, "variance": float(v)} for i, v in enumerate(explained_variance)]
    
    return {
        "eigenvalues": [float(e) for e in eigenvalues],
        "explained_variance": [float(v) for v in explained_variance],
        "scree": scree_points,
        "scatter": scatter_points
    }
