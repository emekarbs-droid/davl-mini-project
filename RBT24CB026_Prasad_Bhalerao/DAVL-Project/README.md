# Data-Driven Financial Behavior Modeling and Prediction System

## Folder Structure
- `app.py` - Streamlit entrypoint and tab orchestration
- `modules/` - preprocessing, feature engineering, modeling, clustering, PCA, and transaction logic
- `utils/` - reusable Matplotlib plotting helpers
- `data/` - the two CSV datasets

## What this project does
- Cleans and analyzes noisy transaction data from `data/budgetwise_finance_dataset.csv`
- Builds statistical and ML modules on structured financial data from `data/IndianPersonalFinance.csv`
- Provides an interactive multi-tab Streamlit dashboard for exploration and prediction

## Virtual Environment Setup
Use the project venv and install dependencies there:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Modules included
- Data preprocessing (missing values, category/payment standardization, date parsing, amount cleaning, outlier removal)
- Statistical analysis (descriptive metrics, heatmap, scatter analysis)
- Regression (predict desired savings with R2 and RMSE)
- Classification (low/medium/high saver categories)
- Clustering (K-Means + Elbow method)
- PCA (2D projection with explained variance)
- Transaction trends (monthly and category-wise spending)

## Run locally
1. Install dependencies:

```bash
D:/Python/python.exe -m pip install -r requirements.txt
```

2. Start the dashboard:

```bash
D:/Python/python.exe -m streamlit run app.py
```

## Notes
- Sidebar filters (age, income, occupation, city tier) affect the structured dataset views.
- The transaction trend tab is based on cleaned transaction rows.
