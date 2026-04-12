import pytest
from fastapi.testclient import TestClient
from backend.main import app
import json

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Sales Data Analyzer API"}

def test_analyze_data_empty():
    response = client.post(
        "/api/analyze",
        files={"file": ("empty.csv", b"", "text/csv")}
    )
    # The API catches an empty dataframe
    assert "error" in response.json()
    assert response.json()["error"] == "Uploaded file is empty"

def test_analyze_data_valid():
    # Providing enough data rows to allow clustering (and train/test split if target chosen)
    csv_data = """ColA,ColB,Target
10,20,30
12,22,32
11,21,31
15,25,35
16,26,36
14,24,34
19,29,39
20,30,40
18,28,38
22,32,42
"""
    response = client.post(
        "/api/analyze",
        data={"target_column": "Target"},
        files={"file": ("test.csv", csv_data.encode('utf-8'), "text/csv")}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "ColA" in data["columns"]
    
    # Check that EDA and Regression pipelines executed successfully
    assert "eda" in data
    assert "statistics" in data["eda"]
    assert "regression" in data
    assert "metrics" in data["regression"]
