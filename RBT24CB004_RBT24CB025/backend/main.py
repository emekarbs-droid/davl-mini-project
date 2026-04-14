from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes.analysis import router as analysis_router

app = FastAPI(title="Sales Data Analyzer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analysis_router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Sales Data Analyzer API"}
