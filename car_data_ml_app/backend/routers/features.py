from fastapi import APIRouter, HTTPException
from app_state import state
import numpy as np
import pandas as pd
from sklearn.feature_selection import VarianceThreshold, SelectKBest, f_regression, RFE
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler

router = APIRouter()

@router.get("/rank")
def get_feature_ranking(target: str = "price"):
    if state.df is None:
        raise HTTPException(status_code=400, detail="No dataset uploaded")
    
    from services.data_utils import clean_dataset
    from services.ml_utils import handle_missing_values, encode_categorical
    
    df = clean_dataset(state.df)
    df = handle_missing_values(df)
    df = encode_categorical(df)
    
    if target not in df.columns:
        raise HTTPException(status_code=400, detail=f"Target {target} not found")
        
    num_df = df.select_dtypes(include=[np.number])
    X = num_df.drop(columns=[target])
    y = num_df[target]
    
    # Scale for consistent ranking
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # 1. Variance Threshold
    selector = VarianceThreshold()
    selector.fit(X_scaled)
    variances = selector.variances_
    
    # 2. Statistical Selection (F-Regression)
    k_best = SelectKBest(score_func=f_regression, k='all')
    k_best.fit(X_scaled, y)
    scores = k_best.scores_
    
    # 3. RFE (Recursive Feature Elimination)
    rfe = RFE(estimator=LinearRegression(), n_features_to_select=1)
    rfe.fit(X_scaled, y)
    rfe_ranking = rfe.ranking_
    
    results = []
    features = list(X.columns)
    for i in range(len(features)):
        results.append({
            "feature": features[i],
            "variance": float(variances[i]),
            "f_score": float(scores[i]),
            "rfe_rank": int(rfe_ranking[i]),
            "score": float(scores[i] / np.max(scores)) # normalized score
        })
        
    # Sort by score
    results = sorted(results, key=lambda x: x["score"], reverse=True)
    
    return {
        "rankings": results,
        "selected_rfe": [r["feature"] for r in results if r["rfe_rank"] <= 5]
    }
