# Sales Data Analyzer Web App

A full-stack Python application that allows users to upload a sales dataset and automatically generates a complete data analysis dashboard.

## Tech Stack
- Frontend: Streamlit
- Backend: FastAPI
- Data Science Libraries: `pandas`, `numpy`, `scikit-learn`, `plotly`

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the backend (FastAPI):
```bash
cd backend
uvicorn main:app --reload --port 8000
```
This runs the API locally at http://localhost:8000

3. Run the frontend (Streamlit) in another terminal:
```bash
streamlit run frontend/app.py
```
This serves the dashboard at http://localhost:8501
