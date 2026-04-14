# Financial Behavior Modeling System - Documentation

## 1. Project Overview
This project is a comprehensive, interactive data science application that analyzes financial behavior. It contrasts and integrates insights from two distinct datasets:
- **IndianPersonalFinance.csv (Structured Dataset):** Contains clean, demographic, and financial details (income, expenses, savings) of individuals.
- **budgetwise_finance_dataset.csv (Transaction Dataset):** Contains raw, real-world, noisy transaction records requiring substantial cleaning.

The app uses **Streamlit** to provide an interactive dashboard with modular Python backend logic.

## 2. System Architecture & Modular Design
Following best practices for maintainability, the application is broken down into specific modules:
- `app.py`: The main Streamlit user interface and tab orchestration featuring a strictly professional Dark Theme.
- `modules/__init__.py`: Package initialization defining public APIs and documenting module inventory.
- `modules/config.py`: Centralized configuration, paths, and mapping dictionaries.
- `modules/data_loader.py`: Handles reading CSVs and standardizing column names.
- `modules/preprocess.py`: Contains complex logic for data cleaning, date parsing, outlier removal, and derived feature calculations.
- `modules/features.py`: Prepares the matrices of features for machine learning.
- `modules/regression.py`: Implements Linear Regression (for predicting target savings) and Logistic Regression (for classification of saver types).
- `modules/clustering.py`: Implements the Elbow method and K-Means clustering to identity sub-groups.
- `modules/pca.py`: Handles Principal Component Analysis (PCA) to project high-dimensional clusters onto a 2D plane for visualization.
- `modules/transactions.py`: Extracts and aggregates time-series and categorical intelligence from raw transactions.
- `utils/plots.py`: Reusable Matplotlib charting functions.

## 3. Data Processing Pipeline
### Transaction Cleaning
- **Categorical Normalization:** Corrects common typos in categories (e.g., "foodd" -> "food") and standardizes payment modes.
- **Amount Extraction:** Uses Regex to strip currency symbols (e.g., "₹", "Rs", text noise) to cast strings into numeric arrays.
- **Date Handling:** Parses mixed format dates gracefully (US vs UK styles).
- **Outlier Mitigation:** Removes excessive bounds using the Interquartile Range (IQR) method (e.g., removing amounts beyond Q3 + 1.5*IQR).

### Structured Data Engineering
- **Total Expense Calculation:** Sums across multiple granular expense columns.
- **Savings Ratio:** Creates an auxiliary feature `(desired_savings / income)` for deeper analysis.

## 4. Machine Learning Models Explained
### 4.1. Linear Regression (Predicting Savings)
- **Goal:** To predict an individual's `desired_savings` based on features like `income`, `total_expense`, `age`, and specific expenditures.
- **Equation:** Linear Regression models the linear relationship between the target $Y$ (savings) and the features $X$ using coefficients $\beta$:
  $$ Y = \beta_0 + \beta_1 X_1 + \beta_2 X_2 + \dots + \beta_n X_n + \epsilon $$
- **Process:** Data is imputed to handle missing values, dummified for categorical columns, and piped into a `LinearRegression` model.
- **Metrics:** Evaluated via **R² Score** (explains variance) and **RMSE** (absolute error margin).

### 4.2. Logistic Regression (Classification of Savers)
- **Goal:** To classify users into behavioral tranches: `Low Saver`, `Medium Saver`, and `High Saver`.
- **Equation:** Uses the sigmoid function (for binary/multinomial modeling) to predict the probability $P$ of belonging to a "Saver" class:
  $$ P(Y=k|X) = \frac{1}{1 + e^{-(\beta_0 + \beta X)}} $$
- **Process:** Users are binned into labels using quantiles of their savings percentage. A `LogisticRegression` model with a standard scaler evaluates these categories. An accuracy score and Confusion Matrix validate the classification performance.

### 4.3. K-Means Clustering & Elbow Method
- **Goal:** To segment users into anonymous behavioral cohorts based on similarities without explicit labels.
- **Equation:** K-Means iteratively minimizes the Within-Cluster Sum of Squares (WCSS), where $C_i$ is the cluster and $\mu_i$ is the centroid:
  $$ WCSS = \sum_{i=1}^{K} \sum_{x \in C_i} || x - \mu_i ||^2 $$
- **Elbow Method:** Fits K-Means across a range of *K* clusters, calculating the Within-Cluster-Sum-of-Squares (WCSS). The point where the variance graph "bends" (elbow) highlights the optimal `K`.
- **K-Means:** Re-assigns the selected `K` to generate cluster IDs for data records.

### 4.4. PCA (Principal Component Analysis)
- **Goal:** Dimensionality reduction.
- **Equation:** Maximizes variance by solving the eigenvalue problem for the covariance matrix $C$:
  $$ C v = \lambda v $$
  *(where $v$ represents the principal components/eigenvectors and $\lambda$ represents the variance explained/eigenvalues).*
- **Process:** Since the structured dataset contains dozens of features, visualizing the K-Means clusters would normally be impossible visually. PCA mathematically condenses this multi-dimensional space into Principal Component 1 (PC1) and PC2, retaining as much mathematical variance as possible contextually, allowing a clean 2D scatter plot projection.

## 5. UI & Interactivity
Built entirely on Streamlit, the system allows the user to deeply customize parameters via sidebar filters (like Income ranges, Age, City Tier). The visual structure implements a custom CSS layer utilizing a hero-card header layout, providing an embedded "web app" feel.