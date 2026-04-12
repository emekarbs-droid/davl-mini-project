from fastapi import APIRouter, HTTPException
from app_state import state
from services.data_utils import clean_dataset
import numpy as np
import pandas as pd

router = APIRouter()

@router.get("/summary")
def get_summary():
    if state.df is None:
        raise HTTPException(status_code=400, detail="No dataset uploaded")
    
    df = clean_dataset(state.df)
    
    # Select numeric columns
    numeric_df = df.select_dtypes(include=[np.number])
    
    summary = {}
    for col in numeric_df.columns:
        summary[col] = {
            "mean": numeric_df[col].mean(),
            "median": numeric_df[col].median(),
            "mode": numeric_df[col].mode().iloc[0] if not numeric_df[col].mode().empty else None,
            "variance": numeric_df[col].var(),
            "std_dev": numeric_df[col].std()
        }
        
        # Replace NaN with None for JSON serialization
        for k, v in summary[col].items():
            if pd.isna(v):
                summary[col][k] = None

    # Covariance and Correlation Matrix
    cov_matrix = numeric_df.cov().to_dict()
    corr_matrix = numeric_df.corr().to_dict()
    
    return {
        "summary": summary,
        "covariance": cov_matrix,
        "correlation": corr_matrix
    }
