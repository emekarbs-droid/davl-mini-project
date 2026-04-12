from fastapi import APIRouter, UploadFile, File, HTTPException
import pandas as pd
import numpy as np
from app_state import state
import io

router = APIRouter()

@router.post("/")
async def upload_csv(file: UploadFile = File(...)):
    if not (file.filename.endswith('.csv') or file.filename.endswith('.txt')):
        raise HTTPException(status_code=400, detail="Only CSV or TXT files are allowed")
    
    contents = await file.read()
    try:
        try:
            df = pd.read_csv(io.BytesIO(contents), encoding='utf-8')
        except UnicodeDecodeError:
            df = pd.read_csv(io.BytesIO(contents), encoding='windows-1252')
        state.df = df
        state.df.to_pickle("temp_state.pkl")
        return {
            "message": "File uploaded successfully",
            "columns": list(df.columns),
            "rows": len(df),
            "preview": df.head(10).replace({np.nan: None}).to_dict(orient="records")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
