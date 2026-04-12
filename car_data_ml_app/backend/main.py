from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import upload, analyze, preprocess, regression, classification, pca, clustering, eda, features

app = FastAPI(title="Car Dataset ML API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router, prefix="/api/upload", tags=["Upload"])
app.include_router(analyze.router, prefix="/api/analyze", tags=["Analyze"])
app.include_router(preprocess.router, prefix="/api/preprocess", tags=["Preprocess"])
app.include_router(regression.router, prefix="/api/regression", tags=["Regression"])
app.include_router(classification.router, prefix="/api/classification", tags=["Classification"])
app.include_router(pca.router, prefix="/api/pca", tags=["PCA"])
app.include_router(clustering.router, prefix="/api/clustering", tags=["Clustering"])
app.include_router(eda.router, prefix="/api/eda", tags=["EDA"])
app.include_router(features.router, prefix="/api/features", tags=["Features"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Car Dataset ML API"}
