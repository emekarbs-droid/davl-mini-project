import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df_cleaned = df.copy()
    
    # Handle missing values
    for col in df_cleaned.columns:
        if df_cleaned[col].dtype in ['int64', 'float64']:
            df_cleaned[col] = df_cleaned[col].fillna(df_cleaned[col].median())
        else:
            if not df_cleaned[col].mode().empty:
                df_cleaned[col] = df_cleaned[col].fillna(df_cleaned[col].mode()[0])
            
    # Outlier removal (IQR method) for numeric columns
    numeric_cols = df_cleaned.select_dtypes(include=['number']).columns
    for col in numeric_cols:
        Q1 = df_cleaned[col].quantile(0.25)
        Q3 = df_cleaned[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        # Filter outliers
        df_cleaned = df_cleaned[(df_cleaned[col] >= lower_bound) & (df_cleaned[col] <= upper_bound)]
        
    return df_cleaned

def encode_and_scale(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    # Returns (raw_encoded, scaled_encoded)
    df_encoded = df.copy()
    
    # One-hot encoding
    categorical_cols = df_encoded.select_dtypes(exclude=['number']).columns
    if len(categorical_cols) > 0:
        df_encoded = pd.get_dummies(df_encoded, columns=categorical_cols, drop_first=True)
    
    df_scaled = df_encoded.copy()
    
    # Z-score standardization
    numeric_cols = df_scaled.select_dtypes(include=['number']).columns
    if len(numeric_cols) > 0:
        scaler = StandardScaler()
        df_scaled[numeric_cols] = scaler.fit_transform(df_scaled[numeric_cols])
        
    return df_encoded, df_scaled
