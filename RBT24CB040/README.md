# DAVL — Data Analysis & Visualization Lab

A **production-ready**, Python-based full-stack Data Analysis Web Application built with **Streamlit**.  
Upload any CSV or Excel dataset and instantly receive comprehensive analysis, interactive visualizations, and actionable insights.

---

## 🚀 Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the application
```bash
streamlit run app.py
```

The app will open automatically at **http://localhost:8501**

---

## 📁 Project Structure

```
DAVL Project/
├── app.py                    # Main Streamlit entry point
├── requirements.txt          # All Python dependencies
├── README.md
└── modules/
    ├── __init__.py
    ├── data_loader.py        # CSV/Excel loading & preview
    ├── overview.py           # Shape, dtypes, memory, target detection
    ├── quality.py            # Missing values, duplicates, outliers, imbalance
    ├── preprocessing.py      # Imputation, encoding, scaling, feature selection
    ├── eda.py                # Univariate, bivariate, multivariate analysis
    ├── visualizations.py     # All chart generation (Plotly + Seaborn)
    ├── statistics.py         # Descriptive stats, correlation, covariance
    ├── pca_analysis.py       # PCA + scree plot + loadings
    ├── lda_analysis.py       # LDA (conditional on target variable)
    ├── factor_analysis.py    # Factor analysis + varimax rotation
    └── insights.py           # Auto-generated analyst insights & report
```

---

## 📊 Features

### 1. Dataset Upload
- Accepts **CSV** and **Excel** (.xlsx, .xls) files
- Instant preview with head/tail views
- Row, column, and cell count metrics

### 2. Dataset Overview
- Shape, data types, memory usage
- Unique values per column
- **Automatic target column detection** (heuristic + manual override)

### 3. Data Quality Analysis
- Missing value count & percentage with severity tags
- Duplicate row detection
- Constant & near-constant column identification
- High cardinality categorical detection
- **IQR + Z-score outlier detection**
- Class imbalance detection with ratio

### 4. Preprocessing Pipeline
- Missing value imputation (mean / median / mode)
- Duplicate removal
- One-hot & label encoding for categoricals
- **StandardScaler** feature scaling
- IQR-based outlier capping
- Variance threshold feature selection

### 5. Exploratory Data Analysis (EDA)
- Univariate: histogram + boxplot per column
- Bivariate: scatter with OLS trendline, violin by groups
- Multivariate: pairplot matrix + 3D scatter
- Distribution grid of all numeric features

### 6. Visualizations (Auto-generated)
- Histograms · Boxplots · Scatter with marginals
- Violin plots · Correlation heatmap (Plotly + Seaborn)
- Count plots · Bar charts · Missing value heatmap
- All charts downloadable as PNG

### 7. Statistical Summary
- Mean, median, mode, std, variance
- Skewness & kurtosis with interpretation
- **Shapiro-Wilk normality test**
- Pearson correlation matrix (styled)
- Covariance matrix
- High-correlation pair detection (|r| ≥ 0.8)

### 8. PCA Analysis
- Standardize → compute PCA
- Explained variance ratio table
- **Scree plot** + cumulative variance graph
- 2D & 3D PCA scatter plots
- Component loadings heatmap

### 9. LDA Analysis *(requires target column)*
- LDA projection into 1D/2D/3D
- Class separation histogram
- Discriminant coefficient heatmap
- Class means in LDA space

### 10. Factor Analysis
- **KMO** & Bartlett's sphericity tests
- Eigenvalue scree plot (Kaiser criterion)
- Varimax-rotated factor loadings heatmap
- Communalities table with interpretation
- Per-factor variance explained

### 11. Analyst Insights (Auto-generated)
- Important features by variance & target correlation
- Highly correlated pairs
- Data quality issues with severity
- Suggested preprocessing steps
- Downloadable analysis report (.txt)

---

## 📦 Tech Stack

| Layer | Technology |
|---|---|
| UI Framework | Streamlit |
| Data Processing | pandas, numpy |
| Visualization | plotly, matplotlib, seaborn |
| Machine Learning | scikit-learn |
| Statistical Analysis | scipy |
| Factor Analysis | factor_analyzer |
| File Support | openpyxl, xlrd |

---

## ⚙️ Requirements

- Python **3.9+**
- All packages listed in `requirements.txt`

---

## 🎨 Design

- Dark glassmorphism UI with gradient backgrounds
- Responsive layout with 10 organized analysis tabs
- Interactive Plotly charts with hover tooltips
- Downloadable charts, processed dataset, and reports

---

## 📄 License

MIT License — free to use and modify.
