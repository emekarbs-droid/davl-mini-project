# 📊 DAVL — Data Analysis & Visualization Lab

A powerful Python-based full-stack Data Analysis Web Application that performs complete dataset analysis after user upload. Built with Streamlit for a seamless single-command experience.

![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red?logo=streamlit)
![License](https://img.shields.io/badge/License-MIT-green)

---

## ✨ Features

### 📊 Dataset Upload & Overview
- CSV and Excel file support
- Dataset preview (head, tail, sample)
- Shape, data types, memory usage, unique values
- Auto target column detection

### 🔍 Data Quality Analysis
- Missing values (count & percentage)
- Duplicate row detection
- Constant columns
- High cardinality columns
- Outlier detection (IQR method)
- Class imbalance detection

### 🛠️ Preprocessing Pipeline
- Handle missing values (auto/mean/median/mode/drop)
- Remove duplicates
- Categorical encoding (Label / One-Hot)
- Feature scaling (StandardScaler)
- Outlier handling (IQR clipping/removal)
- Automated feature selection

### 📈 Exploratory Data Analysis
- Univariate analysis (numeric + categorical)
- Bivariate analysis (scatter, grouped box)
- Multivariate analysis (pair plots)
- Correlation analysis (Pearson/Spearman/Kendall)
- Distribution analysis (normality tests)

### 📉 Visualizations (Interactive)
- Histogram, Boxplot, Scatterplot
- Pair plot, Correlation Heatmap
- Count plot, Bar chart, Violin plot
- Missing values heatmap

### 📐 Statistical Summary
- Mean, Median, Mode, Std Dev, Variance
- Skewness, Kurtosis
- Correlation & Covariance matrices
- Normality tests (Shapiro-Wilk, D'Agostino)

### 🧮 PCA Analysis
- Standardized PCA computation
- Explained variance ratio & scree plot
- 2D/3D PCA scatter plots
- Cumulative variance graph
- Component loadings heatmap

### 📉 LDA Analysis
- Conditional on target variable existence
- LDA projection (2D/3D)
- Class separation visualization
- Discriminant weights

### 🔬 Factor Analysis
- Bartlett's test & KMO measure
- Optimal factor determination
- Factor loadings (with rotation)
- Communalities table

### 💡 Auto-Generated Insights
- Important features ranked
- Highly correlated variable detection
- Redundant column identification
- Data quality issue summary
- Preprocessing recommendations

### ⬇️ Export
- Download processed dataset (CSV)
- Download analysis report (Markdown)
- Export insights (JSON)

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9 or higher

### Installation

```bash
# Clone or navigate to project directory
cd "Davl mini project"

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

---

## 📁 Project Structure

```
Davl mini project/
├── app.py                    # Main Streamlit entry point
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── assets/
│   └── style.css             # Custom dark theme CSS
└── src/
    ├── __init__.py
    ├── data_handler.py       # Upload, preview, overview
    ├── data_quality.py       # Quality analysis module
    ├── preprocessing.py      # Data preprocessing pipeline
    ├── eda.py                # Exploratory data analysis
    ├── visualizations.py     # Plotly chart generation
    ├── statistics.py         # Statistical computations
    ├── pca_analysis.py       # PCA analysis module
    ├── lda_analysis.py       # LDA analysis module
    ├── factor_analysis.py    # Factor analysis module
    ├── insights.py           # Auto-generated insights
    └── report_export.py      # Export & download utility
```

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| Frontend | Streamlit |
| Data Processing | pandas, numpy |
| Visualization | Plotly, Seaborn, Matplotlib |
| Machine Learning | scikit-learn |
| Statistics | scipy |
| Factor Analysis | factor_analyzer |

---

## 📝 License

MIT License — feel free to use and modify.
