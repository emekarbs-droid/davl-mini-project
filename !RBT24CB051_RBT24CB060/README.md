# DAVL Studio

## Team DAVL

This project was developed by:
- Ashish Gadhave (https://github.com/Ashish-Gd)
- Kaushal Wani   (https://github.com/kaushalrw34-ctrl)

DAVL Studio is a web-based Data Analysis and Machine Learning platform designed to simplify the process of exploring, visualizing, and understanding structured datasets. It provides an interactive interface where users can upload a CSV file and instantly perform advanced data analysis without writing code.

## Features

### 1. Automated Exploratory Data Analysis (EDA)
- Displays dataset overview (rows, columns, missing values)
- Identifies data quality and structure
- Generates correlation heatmaps to show relationships between variables

### 2. Data Visualization
- Histogram for understanding data distribution
- Box Plot for detecting outliers and spread
- Scatter Plot for analyzing relationships between variables
- Interactive column selection for dynamic visualization

### 3. Data Preprocessing
- Handles missing values automatically
- Detects and converts date columns
- Extracts numeric features for analysis

### 4. Dimensionality Reduction (PCA)
- Applies Principal Component Analysis (PCA)
- Reduces high-dimensional data into 2 components
- Visualizes data in a 2D projection
- Displays variance explained by each component

### 5. Machine Learning Models
- Linear Regression for prediction
- Logistic Regression for classification
- Decision Tree Classifier
- Random Forest Classifier

### 6. Model Evaluation & Comparison
- Calculates MSE and RMSE for regression
- Computes accuracy for classification models
- Displays a leaderboard ranking models based on performance
- Highlights the best-performing model

### 7. Automated Insights & Suggestions
- Summarizes key findings from the dataset
- Detects issues like missing values and high correlation
- Provides suggestions for improving data quality and model performance

### 8. Data Explorer
- Displays preview of dataset (first 10 rows)
- Shows missing values per column
- Helps users inspect raw data easily

## How It Works

1. The user uploads a CSV dataset through the interface.
2. The system reads and preprocesses the data (handling missing values and formatting).
3. It automatically performs EDA and generates visualizations.
4. PCA is applied to reduce dimensionality and visualize patterns.
5. Machine learning models are trained and evaluated on the dataset.
6. Results are displayed through charts, metrics, and model comparisons.
7. Finally, an automated summary provides insights and suggestions based on the analysis.

## Purpose

The goal of DAVL Studio is to make data analysis simple, fast, and accessible. It bridges the gap between raw data and meaningful insights by combining data science techniques with an intuitive web interface.

## Tech Stack

- Frontend: Streamlit
- Backend: Python
- Libraries:
  - Pandas, NumPy
  - Matplotlib, Seaborn
  - Scikit-learn


## Conclusion

DAVL Studio is a complete data analysis solution that integrates visualization, machine learning, and automated insights into a single platform. It enables users to explore data efficiently and make data-driven decisions with ease.
