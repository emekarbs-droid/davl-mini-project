from fastapi import APIRouter, HTTPException
from app_state import state
import pandas as pd
import numpy as np
from services.data_utils import clean_dataset

router = APIRouter()

@router.get("/summary")
def get_eda_summary():
    if state.df is None:
        raise HTTPException(status_code=400, detail="No dataset uploaded")
    
    df = clean_dataset(state.df)
    num_df = df.select_dtypes(include=[np.number])
    
    # Descriptive Statistics
    desc_stats = num_df.describe().to_dict()
    
    # Fill NaNs in stats to prevent JSON issues
    for col in desc_stats:
        for stat_name in desc_stats[col]:
            if pd.isna(desc_stats[col][stat_name]):
                desc_stats[col][stat_name] = 0
    
    # Additional stats (Mode)
    for col in num_df.columns:
        mode_val = num_df[col].mode()
        desc_stats[col]['mode'] = mode_val.iloc[0] if not mode_val.empty else None

    # Correlation & Covariance
    corr_matrix = num_df.corr().replace({np.nan: 0}).to_dict()
    cov_matrix = num_df.cov().replace({np.nan: 0}).to_dict()
    mean_vector = num_df.mean().to_dict()

    # Categorical distributions for Dashboard
    cat_df = df.select_dtypes(include=['object', 'category'])
    distributions = {}
    for col in cat_df.columns:
        if cat_df[col].nunique() < 20: # Limit to reasonable size
            distributions[col] = cat_df[col].value_counts().to_dict()

    # Data for Boxplots (min, q1, median, q3, max)
    boxplots = {}
    for col in num_df.columns:
        q = num_df[col].quantile([0, 0.25, 0.5, 0.75, 1]).fillna(0).tolist()
        boxplots[col] = {
            "min": q[0],
            "q1": q[1],
            "median": q[2],
            "q3": q[3],
            "max": q[4]
        }

    # Auto Insights
    insights = []
    if 'price' in num_df.columns and 'horsepower' in num_df.columns:
        corr = num_df['price'].corr(num_df['horsepower'])
        if corr > 0.7:
            insights.append("Strong positive correlation found between Horsepower and Price.")
        elif corr > 0.4:
            insights.append("Higher horsepower generally leads to higher car prices.")
    
    if 'fuel_type' in df.columns:
        top_fuel = df['fuel_type'].mode().iloc[0]
        insights.append(f"{top_fuel} is the dominant fuel type in this dataset.")

    return {
        "stats": desc_stats,
        "correlation": corr_matrix,
        "covariance": cov_matrix,
        "mean_vector": mean_vector,
        "distributions": distributions,
        "boxplots": boxplots,
        "insights": insights,
        "columns": {
            "numeric": list(num_df.columns),
            "categorical": list(cat_df.columns)
        }
    }

@router.get("/scatter")
def get_scatter_data(x: str, y: str):
    if state.df is None:
        raise HTTPException(status_code=400, detail="No dataset uploaded")
    
    df = clean_dataset(state.df)
    if x not in df.columns or y not in df.columns:
        raise HTTPException(status_code=400, detail="Invalid columns selected")
        
    sampled_df = df[[x, y]].dropna().sample(min(500, len(df)))
    return sampled_df.to_dict(orient="records")
