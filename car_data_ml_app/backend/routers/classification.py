from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app_state import state
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

router = APIRouter()

class ClassificationRequest(BaseModel):
    features: list[str] = []
    target_column: str = "price"

@router.post("/train")
def train_classification(req: ClassificationRequest):
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

    if req.target_column not in df.columns:
        raise HTTPException(status_code=400, detail=f"Target {req.target_column} not found in columns")
        
    # Create price categories
    q1 = df[req.target_column].quantile(0.33)
    q3 = df[req.target_column].quantile(0.66)
    
    def categorize(val):
        if val <= q1: return 'Low'
        elif val <= q3: return 'Medium'
        else: return 'High'
        
    df['price_category'] = df[req.target_column].apply(categorize)

    available_features = req.features if req.features else list(df.select_dtypes(include=[np.number]).columns)
    if req.target_column in available_features:
        available_features.remove(req.target_column)

    X = df[available_features]
    y = df['price_category']

    # Standardize
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    
    acc = accuracy_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred, labels=['Low', 'Medium', 'High'])

    # Decision Boundary Visualization (Reduce to 2D for plotting)
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_scaled)
    
    model_2d = LogisticRegression(max_iter=1000)
    model_2d.fit(X_pca, y)
    
    # Meshgrid for background
    x_min, x_max = X_pca[:, 0].min() - 1, X_pca[:, 0].max() + 1
    y_min, y_max = X_pca[:, 1].min() - 1, X_pca[:, 1].max() + 1
    xx, yy = np.meshgrid(np.linspace(x_min, x_max, 30), np.linspace(y_min, y_max, 30))
    grid = np.c_[xx.ravel(), yy.ravel()]
    probs = model_2d.predict(grid)
    
    mesh = []
    for i in range(len(grid)):
        mesh.append({
            "x": float(grid[i,0]),
            "y": float(grid[i,1]),
            "label": str(probs[i])
        })

    # Sample scatter for actual points
    scatter = []
    n_samples = min(200, len(X_pca))
    indices = np.random.choice(len(X_pca), n_samples, replace=False)
    for idx in indices:
        scatter.append({
            "x": float(X_pca[idx, 0]),
            "y": float(X_pca[idx, 1]),
            "label": str(y.iloc[idx])
        })

    # Sigmoid Curve data (1D)
    model_1d = LogisticRegression(max_iter=1000)
    X_1d = X_pca[:, 0].reshape(-1, 1)
    model_1d.fit(X_1d, (y == 'High').astype(int)) # Probability of 'High'
    
    curve_x = np.linspace(X_1d.min(), X_1d.max(), 50)
    curve_y = model_1d.predict_proba(curve_x.reshape(-1, 1))[:, 1]
    
    sigmoid_data = [{"x": float(curve_x[i]), "prob": float(curve_y[i])} for i in range(len(curve_x))]
    
    return {
        "accuracy": float(acc),
        "confusion_matrix": cm.tolist(),
        "labels": ['Low', 'Medium', 'High'],
        "decision_mesh": mesh,
        "scatter": scatter,
        "sigmoid": sigmoid_data
    }
