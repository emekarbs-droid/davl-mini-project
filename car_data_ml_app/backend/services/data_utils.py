import pandas as pd
import numpy as np
import re

def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    df_clean = df.copy()
    
    # Map common column name patterns to standardized ones
    col_mapping = {}
    used_names = set()
    for col in df_clean.columns:
        lower_col = col.lower()
        new_name = None
        if "price" in lower_col:
            new_name = "price"
        elif "horse" in lower_col or "hp" in lower_col:
            new_name = "horsepower"
        elif "cc" in lower_col or "engine" in lower_col or "capacity" in lower_col:
            new_name = "engine"
        elif "mileage" in lower_col or "km/l" in lower_col:
            new_name = "mileage"
        elif "performance" in lower_col or "0 - 100" in lower_col:
            new_name = "acceleration"
        elif "speed" in lower_col:
            new_name = "top_speed"
        elif "torque" in lower_col:
            new_name = "torque"
            
        if new_name and new_name not in used_names:
            col_mapping[col] = new_name
            used_names.add(new_name)
            
    df_clean.rename(columns=col_mapping, inplace=True)
    
    # Function to extract numeric value from string
    def extract_numeric(val):
        if pd.isna(val):
            return np.nan
        if isinstance(val, (int, float)):
            return val
        
        val = str(val).strip()
        # Remove '$', ',', and units like 'hp', 'cc', 'km/h', 'sec', 'Nm'
        val = re.sub(r'[^\d\.-]', '', val)
        if '-' in val:
            # Handle ranges like '70-85' by taking the first one
            val = val.split('-')[0]
        try:
            return float(val) if val else np.nan
        except ValueError:
            return np.nan

    # Apply to specific columns if they exist
    numeric_cols_to_clean = ["price", "horsepower", "engine", "mileage", "acceleration", "top_speed", "torque"]
    for col in numeric_cols_to_clean:
        if col in df_clean.columns:
            df_clean[col] = df_clean[col].apply(extract_numeric)

    return df_clean
