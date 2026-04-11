from fastapi import APIRouter, File, UploadFile, Form
from backend.utils.helpers import load_data
from backend.services.preprocessing import clean_data, encode_and_scale
from backend.services.eda import get_eda_stats, get_distribution_plots
from backend.services.pca import perform_pca
from backend.services.clustering import perform_clustering
from backend.services.regression import perform_regression

router = APIRouter()

@router.post("/analyze")
async def analyze_data(file: UploadFile = File(...), target_column: str = Form(None)):
    try:
        contents = await file.read()
        df = load_data(contents, file.filename)
        
        if df.empty:
            return {"error": "Uploaded file is empty"}
            
        columns = list(df.columns)
        
        # EDA
        eda_results = get_eda_stats(df)
        dist_plots = get_distribution_plots(df)
        
        # Preprocessing
        df_cleaned = clean_data(df)
        df_encoded, df_scaled = encode_and_scale(df_cleaned)
        
        # Models
        pca_results = perform_pca(df_scaled)
        clustering_results = perform_clustering(df_scaled)
        
        regression_results = None
        if target_column and target_column in df.columns:
            if target_column in df_scaled.columns:
                regression_results = perform_regression(df_scaled, target_column)
            else:
                regression_results = {"error": "Target column must be numerical for regression."}
                
        return {
            "status": "success",
            "columns": columns,
            "eda": eda_results,
            "distribution_plots": dist_plots,
            "pca": pca_results,
            "clustering": clustering_results,
            "regression": regression_results
        }
    except Exception as e:
        return {"error": str(e)}
