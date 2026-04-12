import pandas as pd
import json
import plotly.express as px

def get_eda_stats(df: pd.DataFrame) -> dict:
    numeric_df = df.select_dtypes(include=['number'])
    
    stats = {}
    for col in numeric_df.columns:
        stats[col] = {
            "mean": float(numeric_df[col].mean()),
            "median": float(numeric_df[col].median()),
            "std": float(numeric_df[col].std())
        }
    
    corr_matrix = numeric_df.corr().to_dict()
    
    # Generate Heatmap figure JSON
    fig_corr = px.imshow(numeric_df.corr(), text_auto=True, title="Correlation Heatmap", aspect="auto")
    corr_fig_json = fig_corr.to_json()
    
    return {
        "statistics": stats,
        "correlation_matrix": corr_matrix,
        "correlation_fig": json.loads(corr_fig_json)
    }

def get_distribution_plots(df: pd.DataFrame) -> dict:
    numeric_cols = df.select_dtypes(include=['number']).columns
    plots = {}
    for col in numeric_cols[:5]: # limit to 5 to avoid heavy payload
        # Histogram
        fig_hist = px.histogram(df, x=col, title=f"Distribution of {col}")
        plots[f"{col}_hist"] = json.loads(fig_hist.to_json())
        
        # Boxplot
        fig_box = px.box(df, y=col, title=f"Boxplot of {col}")
        plots[f"{col}_box"] = json.loads(fig_box.to_json())
        
    return plots
