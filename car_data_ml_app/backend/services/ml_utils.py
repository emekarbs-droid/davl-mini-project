import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler

import pandas.api.types as ptypes

def handle_missing_values(df: pd.DataFrame, method="mean", cols=None):
    df = df.copy()
    if cols is None:
        cols = df.columns
    
    for col in cols:
        if not ptypes.is_numeric_dtype(df[col]):
            # Fill categorical with mode
            mode_val = df[col].mode().iloc[0] if not df[col].mode().empty else "Unknown"
            df[col] = df[col].fillna(mode_val)
        else:
            if method == "mean":
                df[col] = df[col].fillna(df[col].mean())
            elif method == "median":
                df[col] = df[col].fillna(df[col].median())
    return df

def remove_outliers(df: pd.DataFrame, method="iqr"):
    df = df.copy()
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    if method == "iqr":
        for col in numeric_cols:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]
    elif method == "z-score":
        from scipy import stats
        for col in numeric_cols:
            z_scores = np.abs(stats.zscore(df[col].dropna()))
            # Only keep rows where z-score is < 3
            # It's tricky with missing values, better handle missing first
            valid_idx = (np.abs(stats.zscore(df[col].fillna(df[col].mean()))) < 3)
            df = df[valid_idx]
            
    return df

def encode_categorical(df: pd.DataFrame):
    df = df.copy()
    cat_cols = df.select_dtypes(include=['object', 'category']).columns
    # Using simple Label Encoding / pandas get_dummies
    df = pd.get_dummies(df, columns=cat_cols, drop_first=True)
    return df

def scale_features(df: pd.DataFrame, method="standard"):
    df = df.copy()
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    if method == "standard":
        scaler = StandardScaler()
    else:
        scaler = MinMaxScaler()
        
    df[numeric_cols] = scaler.fit_transform(df[numeric_cols])
    return df
