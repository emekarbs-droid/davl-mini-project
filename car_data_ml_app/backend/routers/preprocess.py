from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app_state import state
from services.data_utils import clean_dataset
from services.ml_utils import handle_missing_values, remove_outliers, encode_categorical, scale_features

router = APIRouter()

class PreprocessOptions(BaseModel):
    imputation: str = "mean"
    outlier_method: str = "none" # "iqr", "z-score", "none"
    encode: bool = False
    scale: str = "none" # "standard", "minmax", "none"
    remove_duplicates: bool = True

@router.post("/")
def preprocess_data(options: PreprocessOptions):
    if state.df is None:
        raise HTTPException(status_code=400, detail="No dataset uploaded")
    
    # Start with cleaned names and numeric conversion
    df = clean_dataset(state.df)
    
    original_shape = df.shape
    
    if options.remove_duplicates:
        df.drop_duplicates(inplace=True)
        
    # Handle missing
    df = handle_missing_values(df, method=options.imputation)
    
    # Handle outliers
    if options.outlier_method in ["iqr", "z-score"]:
        df = remove_outliers(df, method=options.outlier_method)
        
    # Encode
    if options.encode:
        df = encode_categorical(df)
        
    # Scale
    if options.scale in ["standard", "minmax"]:
        df = scale_features(df, method=options.scale)
        
    state.preprocessed_df = df
    
    return {
        "message": "Data preprocessed successfully",
        "original_rows": original_shape[0],
        "original_cols": original_shape[1],
        "new_rows": df.shape[0],
        "new_cols": df.shape[1],
        "sample": df.head(5).to_dict(orient="records")
    }
