from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app_state import state
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

router = APIRouter()

class RegressionRequest(BaseModel):
    model_type: str = "linear" # "linear", "multiple", "polynomial", "ridge", "lasso"
    features: list[str] = []
    target: str = "price"

@router.post("/train")
def train_regression(req: RegressionRequest):
    # Use explicitly preprocessed df or clean df
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
        
    if req.target not in df.columns:
        raise HTTPException(status_code=400, detail=f"Target {req.target} not found in columns")

    available_features = req.features if req.features else list(df.select_dtypes(include=[np.number]).columns)
    if req.target in available_features:
        available_features.remove(req.target)
        
    if not available_features:
        raise HTTPException(status_code=400, detail="No numeric features available for regression")

    X = df[available_features]
    y = df[req.target]

    # Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Model
    features_transformed = False
    if req.model_type == "polynomial":
        poly = PolynomialFeatures(degree=2)
        X_train = poly.fit_transform(X_train)
        X_test = poly.transform(X_test)
        model = LinearRegression()
        features_transformed = True
    elif req.model_type == "ridge":
        model = Ridge(alpha=1.0)
    elif req.model_type == "lasso":
        model = Lasso(alpha=0.1)
    else:
        model = LinearRegression()

    if req.model_type == "linear" and len(available_features) > 1:
        # linear with 1 feature, multiple with >1
        if len(available_features) == 1:
            X_train = X_train.values.reshape(-1, 1)
            X_test = X_test.values.reshape(-1, 1)

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
        
    metrics = {
        "mse": float(mean_squared_error(y_test, y_pred)),
        "rmse": float(np.sqrt(mean_squared_error(y_test, y_pred))),
        "mae": float(mean_absolute_error(y_test, y_pred)),
        "r2": float(r2_score(y_test, y_pred))
    }
    
    # Clean metrics for JSON
    for k, v in metrics.items():
        if not np.isfinite(v):
            metrics[k] = 0.0

    n = len(X_test)
    p = X_test.shape[1]
    adj_r2 = float(1 - (1 - metrics["r2"]) * (n - 1) / (n - p - 1)) if (n - p - 1) > 0 else 0
    metrics["adjusted_r2"] = adj_r2 if np.isfinite(adj_r2) else 0.0

    # Feature importance (coefficients)
    importance = []
    if not features_transformed and hasattr(model, "coef_"):
        importance = [{"feature": f, "weight": float(c)} for f, c in zip(available_features, model.coef_)]
        importance = sorted(importance, key=lambda x: abs(x["weight"]), reverse=True)

    # Plot data (actual vs predicted)
    # Take a sample of 50 for visualization to keep payload small
    sample_size = min(50, len(y_test))
    actual_vs_pred = [{"actual": float(a), "predicted": float(p)} for a, p in list(zip(y_test, y_pred))[:sample_size]]

    return {
        "model": req.model_type,
        "metrics": metrics,
        "feature_importance": importance,
        "plot_data": actual_vs_pred
    }
