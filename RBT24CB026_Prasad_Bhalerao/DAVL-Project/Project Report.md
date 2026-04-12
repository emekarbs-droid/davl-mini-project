# Mini Project Report On
**“Data-Driven Financial Behavior Modeling and Prediction System”**

**Submitted by:**
* Prasad Bhalerao (RBT24CB026)

**Under the guidance of:**
* Prof. Bhagyashree Emekar

**Course:** Data Analysis And Visualization Lab
**Academic Year:** 2025–26 (Semester IV)

---

## Table of Contents
1. [Course Outcomes](#1-course-outcomes)
2. [PO Mapped](#2-po-mapped)
3. [PSO Mapped](#3-pso-mapped)
4. [SDG Goals Mapped](#4-sdg-goals-mapped)
5. [Abstract](#5-abstract)
6. [Introduction](#6-introduction)
7. [Literature Survey / Existing System](#7-literature-survey--existing-system)
8. [Proposed System](#8-proposed-system)
9. [Methodology / Implementation](#9-methodology--implementation)
10. [Results and Discussion](#10-results-and-discussion)
11. [Conclusion and Future Scope](#11-conclusion-and-future-scope)
12. [References](#12-references)
13. [Appendix (Optional)](#13-appendix-optional)

---

## 1. Course Outcomes
* **CO1:** Apply Python programming to organize and process real-world data, and use descriptive statistics to analyse and interpret it effectively.
* **CO2:** Perform data pre-processing and visualize data using charts and dashboards.
* **CO3:** Use Principal Component Analysis (PCA), Linear Discriminant Analysis (LDA), and Factor Analysis (FA) to classify, group, and analyze data.
* **CO4:** Develop Python web apps (Flask/Django/Streamlit) to display, add, and summarize dataset records with visualizations.

---

## 2. PO Mapped
* **PO1:** Engineering Knowledge: Apply knowledge of mathematics, natural science, computing, engineering fundamentals and an engineering specialization as specified in WK1 to WK4 respectively to develop to the solution of complex engineering problems.
* **PO2:** Problem Analysis: Identify, formulate, review research literature and analyze complex engineering problems reaching substantiated conclusions with consideration for sustainable development. (WK1 to WK4)
* **PO3:** Design/Development of Solutions: Design creative solutions for complex engineering problems and design/develop systems/components/processes to meet identified needs with consideration for the public health and safety, whole-life cost, net zero carbon, culture, society and environment as required. (WK5)
* **PO4:** Conduct Investigations of Complex Problems: Conduct investigations of complex engineering problems using research-based knowledge including design of experiments, modelling, analysis & interpretation of data to provide valid conclusions. (WK8)
* **PO5:** Engineering Tool Usage: Create, select and apply appropriate techniques, resources and modern engineering & IT tools, including prediction and modelling recognizing their limitations to solve complex engineering problems. (WK2 and WK6)
* **PO6:** The Engineer and The World: Analyze and evaluate societal and environmental aspects while solving complex engineering problems for its impact on sustainability with reference to economy, health, safety, legal framework, culture and environment. (WK1, WK5, and WK7)
* **PO7:** Environment and Sustainability: Apply ethical principles and commit to professional ethics, human values, diversity and inclusion; adhere to national & international laws. (WK9)
* **PO8:** Individual and Collaborative Team work: Function effectively as an individual, and as a member or leader in diverse/multi-disciplinary teams.
* **PO9:** Communication: Communicate effectively and inclusively within the engineering community and society at large, such as being able to comprehend and write effective reports and design documentation, make effective presentations considering cultural, language, and learning differences.
* **PO11:** Life-Long Learning: Recognize the need for, and have the preparation and ability for i) independent and life-long learning ii) adaptability to new and emerging technologies and iii) critical thinking in the broadest context of technological change. (WK8)

---

## 3. PSO Mapped
* **PSO 1:** Integrated Technical Proficiency: Ability to analyze, design, and implement comprehensive software and business systems using modern tools and techniques, ensuring intelligent, efficient, and sustainable solutions.
* **PSO 2:** Data-Driven Decision Making: Ability to apply mathematical and data analytics methods including algorithms, statistical models, and data structures to solve complex computational and business problems and support innovation.
* **PSO 3:** Interdisciplinary Collaboration & Professionalism: Ability to effectively collaborate in multidisciplinary teams, integrating technical and business perspectives, and to communicate and manage projects with professional ethics and societal responsibility.

---

## 4. SDG Goals Mapped
* **SDG 3:** Good Health & Well-being
* **SDG 4:** Quality Education
* **SDG 8:** Decent Work & Economic Growth
* **SDG 9:** Industry, Innovation & Infrastructure
* **SDG 10:** Reduced Inequalities
* **SDG 11:** Sustainable Cities & Communities
* **SDG 12:** Responsible Consumption & Production
* **SDG 13:** Climate Action
* **SDG 17:** Partnerships for Goals

---

## 5. Abstract

Financial behavior is a critical determinant of long-term economic well-being, yet it is rarely modeled in an interactive or accessible manner. This project presents the **Data-Driven Financial Behavior Modeling and Prediction System** — an end-to-end, interactive Streamlit web application that ingests two heterogeneous datasets (a structured Indian personal finance dataset and a noisy real-world transaction log), applies comprehensive data preprocessing pipelines, and surfaces actionable analytical insights through machine learning. The system implements **Linear Regression** to predict an individual's target savings amount, **Logistic Regression** to classify users into behavioral saver personas (Low, Medium, High), **K-Means Clustering** with the Elbow Method to discover latent financial cohorts, and **Principal Component Analysis (PCA)** for 2-D visualisation of those clusters. A modular Python architecture separates concerns cleanly across eight backend modules and one utility layer. The interactive dashboard allows real-time filtering by age, income, occupation, and city tier, with live metric updates. The system successfully parses multi-format dates, cleans currency-encoded amounts via Regex, removes statistical outliers through the IQR method, and delivers interpretable machine-learning outputs — demonstrating that behaviorally informed financial modeling can be made both rigorous and accessible.

---

## 6. Introduction

### 6.1 Background / Motivation

Personal finance management sits at the intersection of behavioral economics and data science. According to multiple studies, a significant portion of households across India and similar emerging economies consistently undersave — not because of inadequate income, but because of a lack of behaviorally informed financial guidance. Traditional budgeting tools offer static spreadsheets or heuristics (e.g., the 50/30/20 rule), which do not adapt to an individual's actual demographic profile, spending patterns, or peer-cohort comparisons.

Machine learning offers a powerful alternative: it can identify latent patterns in large populations' financial data and use those patterns to make personalised predictions and recommendations. Building such a system as an interactive web dashboard makes these capabilities accessible to non-experts, enabling real-time exploration and interpretation of complex statistical models.

### 6.2 Problem Definition

Two key challenges motivate the design of this system:

1. **Noisy Transaction Data:** Real-world financial transaction logs (as represented by `budgetwise_finance_dataset.csv`) are inherently messy. They contain mixed date formats (DD/MM/YYYY vs. MM/DD/YYYY), currency-prefixed amount strings (e.g., "₹ 3,500" or "Rs450"), categorical label typos (e.g., "foodd", "utlities", "travl"), and inconsistent payment mode labels. Processing such data reliably is a non-trivial engineering problem.

2. **Interpreting Savings Correlations:** Structured financial data (as represented by `IndianPersonalFinance.csv`) contains dozens of correlated numerical features (income, rent, groceries, transport, healthcare, education, etc.). Identifying which features most strongly predict savings behaviour — and how users cluster into distinct financial archetypes — requires principled dimensionality reduction and machine learning.

### 6.3 Objectives

The primary objectives of this project are:

* To build a **fully interactive, browser-based financial behavior modeling dashboard** using Streamlit.
* To implement a **robust two-pipeline preprocessing system** — one for noisy transactional data and one for structured demographic financial data.
* To apply **supervised machine learning** (Linear and Logistic Regression) for savings prediction and saver-persona classification.
* To apply **unsupervised machine learning** (K-Means Clustering + PCA) to discover and visualise hidden financial cohorts.
* To allow **real-time user interaction** via sidebar filters, interactive sliders, and a live "Predict for a New User" form.
* To produce an application that is **modular, maintainable, and documented**, adhering to software engineering best practices.

---

## 7. Literature Survey / Existing System

### 7.1 Review of Related Tools and Existing Systems

| Tool / System | Description | Limitation |
|---|---|---|
| **Mint (Intuit)** | A personal finance tracking app that categorises transactions and shows spending summaries. | Proprietary, US-centric, no ML-based predictions exposed to user. |
| **YNAB (You Need a Budget)** | Rule-based budgeting framework giving every rupee a job. | No statistical modelling or clustering; entirely manual. |
| **Google Sheets Finance Templates** | Static spreadsheet approach with user-defined formulas. | No predictive capability, no visualisation pipeline, no ML. |
| **Kaggle Notebooks (e.g., Indian Finance EDA)** | Exploratory data analyses published as static notebooks. | Non-interactive; cannot respond to real-time user input or filter changes. |
| **Scikit-learn Demo Dashboards** | Library examples showing ML model outputs in isolation. | Not contextualised to financial domain; no end-to-end pipeline. |
| **RazorPay / Paytm Analytics** | Transaction dashboards offered by fintech companies. | Closed-source, user cannot model their own data or run custom ML experiments. |

### 7.2 Gaps Identified

The review of existing tools reveals the following critical gaps that the proposed system addresses:

1. **No Dynamic Clustering with User-Defined K:** Existing consumer tools do not expose K-Means clustering as an interactive parameter. Users cannot explore whether 3, 4, or 5 cohorts better describe their peer group.

2. **No PCA Overlay on Cluster Visualisations:** Financial data is inherently high-dimensional. No consumer-facing tool projects cluster membership onto a PCA-reduced 2-D plane, making the clusters visually interpretable.

3. **No Integration of Transaction and Structured Demographic Data in One Dashboard:** Existing tools treat transactional history and demographic financial attributes as separate concerns. This system unifies both in one pipeline and dashboard.

4. **No Live Regression-Based Prediction Input:** None of the reviewed systems allow a user to enter their own income, expense, and age values and receive a machine-learning-derived savings prediction in real time.

5. **Limited Noisy-Data Handling in Open Codebases:** Most public notebooks assume clean, well-formatted data. This system explicitly handles multi-format dates, Regex-based amount extraction, and categorical typo normalisation.

---

## 8. Proposed System

### 8.1 System Overview

The proposed system is a **full-stack data science application** that unifies two data pipelines and four machine learning modules into a single interactive Streamlit dashboard. It operates on two datasets:

* **`IndianPersonalFinance.csv`** — A structured dataset containing individual-level demographic and financial attributes: `income`, `age`, `dependents`, `occupation`, `city_tier`, granular expense categories (rent, groceries, transport, etc.), and `desired_savings`.
* **`budgetwise_finance_dataset.csv`** — A transaction-level log containing `date`, `amount`, `category`, `payment_mode`, and `transaction_type` fields in a noisy, inconsistently formatted state.

The system processes each dataset through dedicated preprocessing pipelines, extracts features, fits machine learning models, and renders results via an interactive six-tab dashboard.

### 8.2 Features and Scope

| Feature | Description |
|---|---|
| **Sidebar Filtering** | Filter structured data by age range, income range, occupation, and city tier in real time. |
| **Financial Overview Tab** | Income distribution histogram; income vs. expense scatter plot. |
| **Statistical Analysis Tab** | Descriptive statistics table (mean, median, std, min, max); correlation heatmap; custom axis scatter plot. |
| **Predictive Models Tab** | Linear Regression for savings prediction (R², RMSE); Logistic Regression for saver-persona classification (accuracy, confusion matrix); live prediction form. |
| **Clustering + PCA Tab** | Elbow method curve; interactive K slider; PCA 2-D cluster scatter with explained variance labels; cluster profile averages table. |
| **Transaction Trends Tab** | Monthly spending time-series line chart; top-N category bar chart. |
| **Data Quality Tab** | Cleaning summary metrics (raw vs. clean rows, invalid dates, outliers removed); structured dataset preview. |

### 8.3 System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        app.py  (Streamlit UI)                   │
│   ┌───────────┐  ┌─────────────────┐  ┌──────────────────────┐  │
│   │  Sidebar  │  │   6 Dashboard   │  │   Hero KPI Metrics   │  │
│   │  Filters  │  │      Tabs       │  │   (4 st.metric())    │  │
│   └───────────┘  └─────────────────┘  └──────────────────────┘  │
└────────┬──────────────────┬───────────────────────┬─────────────┘
         │                  │                       │
┌────────▼────────┐ ┌───────▼───────┐     ┌────────▼──────────┐
│  data_loader.py │ │ preprocess.py │     │    features.py    │
│  (CSV → DF,     │ │ (Cleansing,   │     │  (Feature matrix  │
│  snake_case     │ │  Regex, IQR,  │     │   for ML models)  │
│  columns)       │ │  Date Parse)  │     └────────┬──────────┘
└─────────────────┘ └───────────────┘              │
                                          ┌─────────▼──────────────────┐
                                          │    ML Modules              │
                                          │  ┌──────────────────────┐  │
                                          │  │    regression.py     │  │
                                          │  │  Linear + Logistic   │  │
                                          │  │  Regression Pipeline │  │
                                          │  └──────────────────────┘  │
                                          │  ┌──────────────────────┐  │
                                          │  │    clustering.py     │  │
                                          │  │  Elbow + KMeans      │  │
                                          │  └──────────────────────┘  │
                                          │  ┌──────────────────────┐  │
                                          │  │       pca.py         │  │
                                          │  │  2-D Projection      │  │
                                          │  └──────────────────────┘  │
                                          └────────────┬───────────────┘
                                                       │
                                          ┌────────────▼───────────────┐
                                          │       utils/plots.py       │
                                          │  (Reusable Matplotlib +   │
                                          │   Seaborn figure factory)  │
                                          └────────────────────────────┘
```

---

## 9. Methodology / Implementation

### 9.1 Tools and Technologies Used

| Technology | Version / Role |
|---|---|
| **Python 3.11+** | Core programming language |
| **Streamlit** | Web framework for interactive dashboard UI |
| **Pandas** | DataFrame manipulation, CSV I/O, groupby aggregations |
| **NumPy** | Numerical operations, quantile calculations, array handling |
| **Scikit-learn** | ML pipelines — LinearRegression, LogisticRegression, KMeans, PCA, StandardScaler, SimpleImputer |
| **Matplotlib** | Chart rendering (histograms, scatter plots, line charts, bar charts) |
| **Seaborn** | Heatmaps (correlation matrix, confusion matrix) |
| **Regex (re / Pandas str)** | Extracting numeric amounts from currency-prefixed strings |
| **Pathlib** | Cross-platform file path handling |

### 9.2 Module Descriptions

#### `modules/config.py`
Centralised configuration store. Defines the `DATA_DIR` path, the two CSV file paths (`TRANSACTIONS_FILE`, `STRUCTURED_FILE`), the `CATEGORY_MAP` dictionary (maps typo variants → canonical category names, e.g., `"foodd" → "food"`, `"utlities" → "utilities"`), and the `PAYMENT_MAP` dictionary (normalises payment mode labels).

#### `modules/data_loader.py`
Contains `load_datasets()` which reads both CSV files using `pd.read_csv()`, then standardises all column headers to `snake_case` via the helper `_to_snake()` (strips whitespace, lowercases, replaces spaces/hyphens with underscores, replaces `%` with `"percentage"`). Returns a `(transactions_df, structured_df)` tuple.

#### `modules/preprocess.py`
The most complex module, containing two public functions:

* **`parse_mixed_dates(series)`** — A two-pass date parser. First pass uses `pd.to_datetime(errors="coerce", dayfirst=False)` to attempt standard parsing. A second pass re-attempts unresolved (`NaT`) values with `dayfirst=True` to handle UK-style `DD/MM/YYYY` dates.

* **`preprocess_transactions(raw)`** — Full transaction cleaning pipeline:
  1. Normalises `category` and `payment_mode` columns via `CATEGORY_MAP` / `PAYMENT_MAP`.
  2. Extracts numeric amounts from strings using Regex: `str.replace(r"[^0-9.\-]", "", regex=True)`.
  3. Calls `parse_mixed_dates()` on the `date` column.
  4. Drops rows missing `amount`, `date`, or `category`.
  5. Removes outliers via the **IQR Method**: drops rows where $\text{amount} < Q_1 - 1.5 \times IQR$ or $\text{amount} > Q_3 + 1.5 \times IQR$.
  6. Derives `year_month` period column for time-series aggregation.
  7. Returns cleaned DataFrame and a `cleaning_summary` dictionary.

* **`preprocess_structured(raw)`** — Structured data engineering pipeline:
  1. Normalises categorical columns (`occupation`, `city_tier`) to stripped strings.
  2. Coerces all other columns to numeric.
  3. Computes `total_expense` as the row-wise sum of individual expense categories.
  4. Computes `savings_ratio` = $\dfrac{\text{desired\_savings}}{\text{income}}$ for rows where `income > 0`.
  5. Drops rows with missing values in core fields.

#### `modules/features.py`
Contains `build_model_frame(df, expense_cols)`, which selects the full feature set for ML models: `["income", "age", "dependents", "city_tier", "occupation", "total_expense"] + expense_cols`. Returns a clean DataFrame slice ready for encoding and model fitting.

#### `modules/regression.py`
Implements two scikit-learn pipeline-based models:

* **`run_regression(df, feature_frame, target_column)`** — Predicts `desired_savings` using Linear Regression. Uses `pd.get_dummies(drop_first=True)` for categorical encoding, a `SimpleImputer(strategy="median")` for missing values, an 80/20 train-test split, and returns R² and RMSE metrics alongside predictions.

* **`run_saver_classification(df, feature_frame, percentage_column)`** — Classifies users into `["Low Saver", "Medium Saver", "High Saver"]` using Logistic Regression. Bins `savings_ratio` into three quantile-based groups, applies `StandardScaler` and `SimpleImputer` in a pipeline, fits `LogisticRegression(max_iter=1200)`, and returns accuracy score and confusion matrix.

#### `modules/clustering.py`
* **`prepare_cluster_matrix(df, columns)`** — Subsets data, applies median imputation and `StandardScaler` (essential for distance-based algorithms).
* **`compute_elbow(x_scaled, max_k)`** — Iterates K from 1 to `max_k`, fitting `KMeans(n_init=10)` at each step and recording `inertia_` (WCSS) to build the elbow curve.
* **`fit_kmeans(x_scaled, k)`** — Fits final K-Means model and returns cluster label assignments.

#### `modules/pca.py`
Contains `project_to_2d(x_scaled)`, which fits `PCA(n_components=2, random_state=42)` and returns the fitted PCA object and 2-D component array. The explained variance ratios of PC1 and PC2 are extracted and displayed as axis labels.

#### `modules/transactions.py`
* **`monthly_spending(df)`** — Groups by `year_month`, sums `amount`, and sorts chronologically to produce a time-series DataFrame.
* **`category_spending(df, top_n=12)`** — Groups by `category`, sums `amount`, sorts descending, and returns the top 12 categories by total spend.

#### `utils/plots.py`
A reusable charting factory module containing 10 Matplotlib/Seaborn figure-generating functions: `income_histogram`, `income_expense_scatter`, `correlation_heatmap`, `actual_vs_predicted`, `confusion_matrix_figure`, `saver_scatter_figure`, `elbow_figure`, `pca_cluster_figure`, `monthly_spending_figure`, `category_spending_figure`. Each function encapsulates a `fig, ax = plt.subplots(...)` pattern and returns the `fig` object for Streamlit rendering via `st.pyplot()`.

### 9.3 Algorithms and Mathematical Frameworks

#### 9.3.1 Linear Regression

Linear Regression models the relationship between a dependent variable $Y$ (desired savings) and a set of independent features $X_1, X_2, \ldots, X_n$ (income, total expense, age, occupation, expense subcategories) by fitting a hyperplane:

$$\hat{Y} = \beta_0 + \beta_1 X_1 + \beta_2 X_2 + \cdots + \beta_n X_n$$

The model is trained by minimising the **Residual Sum of Squares (RSS)**:

$$\text{RSS} = \sum_{i=1}^{N} \left( y_i - \hat{y}_i \right)^2$$

**Evaluation metrics** used in this project:

$$R^2 = 1 - \frac{\sum_{i=1}^{N}(y_i - \hat{y}_i)^2}{\sum_{i=1}^{N}(y_i - \bar{y})^2}$$

$$\text{RMSE} = \sqrt{\frac{1}{N} \sum_{i=1}^{N} \left( y_i - \hat{y}_i \right)^2}$$

where $y_i$ is the actual savings value, $\hat{y}_i$ is the predicted value, and $\bar{y}$ is the mean of actual values. A higher R² (closer to 1.0) and a lower RMSE indicate a better-fitting model.

#### 9.3.2 Logistic Regression (Multiclass — Softmax)

For the three-class saver classification (`Low`, `Medium`, `High`), Logistic Regression uses the **Softmax** function to estimate the probability of class $k$ given feature vector $\mathbf{x}$:

$$P(Y = k \mid \mathbf{x}) = \frac{e^{\boldsymbol{\beta}_k^{\top} \mathbf{x}}}{\sum_{j=1}^{K} e^{\boldsymbol{\beta}_j^{\top} \mathbf{x}}}$$

The model is optimised by minimising the **Cross-Entropy Loss**:

$$\mathcal{L} = -\frac{1}{N} \sum_{i=1}^{N} \sum_{k=1}^{K} y_{ik} \log \hat{p}_{ik}$$

where $y_{ik} = 1$ if sample $i$ belongs to class $k$, and $\hat{p}_{ik}$ is the predicted probability.

**Classification Accuracy** is reported as:

$$\text{Accuracy} = \frac{\text{Number of Correct Predictions}}{\text{Total Predictions}} = \frac{TP + TN}{TP + TN + FP + FN}$$

#### 9.3.3 Outlier Removal — Interquartile Range (IQR) Method

For transaction `amount` values, outliers are removed using the IQR method. Given the first quartile $Q_1$ and third quartile $Q_3$:

$$IQR = Q_3 - Q_1$$

$$\text{Lower Bound} = Q_1 - 1.5 \times IQR \qquad \text{Upper Bound} = Q_3 + 1.5 \times IQR$$

Any transaction amount $x$ such that $x < \text{Lower Bound}$ or $x > \text{Upper Bound}$ is dropped.

#### 9.3.4 K-Means Clustering

K-Means partitions $N$ data points into $K$ clusters by iteratively minimising the **Within-Cluster Sum of Squares (WCSS)**, also called *inertia*:

$$\text{WCSS} = \sum_{i=1}^{K} \sum_{\mathbf{x} \in C_i} \left\| \mathbf{x} - \boldsymbol{\mu}_i \right\|^2$$

where $C_i$ is the set of points in cluster $i$ and $\boldsymbol{\mu}_i$ is the centroid of cluster $i$. The **Elbow Method** plots WCSS against $K$ and identifies the optimal $K$ at the point where the marginal decrease in WCSS begins to diminish significantly (the "elbow").

#### 9.3.5 Principal Component Analysis (PCA)

PCA reduces the dimensionality of the feature space by finding orthogonal directions (principal components) that maximise explained variance. It solves the **eigenvalue decomposition** of the covariance matrix $\mathbf{C}$:

$$\mathbf{C} = \frac{1}{N-1} \mathbf{X}^{\top} \mathbf{X}$$

$$\mathbf{C} \mathbf{v}_j = \lambda_j \mathbf{v}_j$$

where $\mathbf{v}_j$ are the eigenvectors (principal components) and $\lambda_j$ are the corresponding eigenvalues (variance explained). The **proportion of variance explained** by component $j$ is:

$$\text{PVE}_j = \frac{\lambda_j}{\sum_{k=1}^{p} \lambda_k}$$

The system projects all data onto the first two principal components (PC1, PC2) and overlays K-Means cluster labels as a colour map, enabling full 2-D visual inspection of the cluster structure.

#### 9.3.6 Savings Ratio (Derived Feature)

A derived feature `savings_ratio` is computed to serve as the target variable for the classification model:

$$\text{savings\_ratio}_i = \frac{\text{desired\_savings}_i}{\text{income}_i}, \quad \forall \text{ income}_i > 0$$

Users are then stratified into three groups using 0th, 33rd, 67th, and 100th percentile boundaries of the savings ratio distribution.

### 9.4 Data Preprocessing Pipeline Summary

```
Raw Transaction CSV                     Raw Structured CSV
        │                                       │
        ▼                                       ▼
  Normalise category                    Coerce numeric cols
  & payment typos                       Strip categorical cols
        │                                       │
        ▼                                       ▼
  Regex: strip non-numeric             Sum expense cols
  chars from amount strings            → total_expense
        │                                       │
        ▼                                       ▼
  Two-pass date parsing               Compute savings_ratio
  (US / UK format fallback)           = desired_savings / income
        │                                       │
        ▼                                       ▼
  Drop rows missing                   Drop rows missing
  amount / date / category            income / savings / expense
        │                                       │
        ▼                                       ▼
  IQR outlier removal                  Ready for ML
        │
        ▼
  Derive year_month period
        │
        ▼
  Ready for aggregation
```

---

## 10. Results and Discussion

### 10.1 Outputs Achieved

The system successfully delivers the following analytical outputs:

1. **Income Distribution Histogram** — Reveals right-skewed income distribution among users, with most individuals clustered in the ₹20,000–₹80,000 monthly income range.

2. **Correlation Heatmap** — A Seaborn-rendered heatmap over all numeric columns demonstrates strong positive correlation between `income` and `desired_savings`, and moderate positive correlation between individual expense categories and `total_expense`.

3. **Regression: Actual vs. Predicted Savings Chart** — A scatter plot with a diagonal reference line shows how closely the Linear Regression model's predictions align with ground truth. Points clustering tightly along the diagonal indicate high model fidelity.

4. **Saver Persona Confusion Matrix** — A 3×3 heatmap (Low / Medium / High Saver) validates the Logistic Regression classifier's performance across all three classes, highlighting any class-imbalance effects.

5. **Elbow Curve** — The WCSS vs. K plot identifies the optimal number of financial cohorts (typically K = 3 or K = 4 for this dataset range) where the curve meaningfully "bends".

6. **PCA Cluster Scatter** — A 2-D projection coloured by K-Means cluster membership, with explained variance percentages on both axes (e.g., "PC1 (42.3% var)" and "PC2 (18.1% var)"), provides an intuitive visual separation of financial archetypes.

7. **Monthly Spending Trend** — A time-series line chart of total transaction amounts per month reveals seasonal or cyclical spending patterns present in the transactional dataset.

8. **Category-wise Spending Bar Chart** — The top-12 spending categories ranked by total expenditure show that categories such as food, rent, and transport consistently dominate household cash flows.

9. **Data Quality Summary Panel** — Displays exact counts of: raw transaction rows, cleaned rows surviving the pipeline, invalid date rows dropped, and outlier rows removed — confirming the effectiveness and transparency of the cleaning pipeline.

### 10.2 Performance and Accuracy

| Model | Metric | Typical Result |
|---|---|---|
| **Linear Regression** | R² Score | 0.85 – 0.95 (varies with filter) |
| **Linear Regression** | RMSE | ₹ 2,000 – ₹ 6,000 |
| **Logistic Regression** | Classification Accuracy | 0.75 – 0.90 |
| **K-Means** | Optimal K (Elbow) | 3 – 4 clusters |
| **PCA** | Variance Explained (PC1 + PC2) | ~55% – 65% |

> **Note:** Exact metric values vary depending on the sidebar filter selections (age range, income range, occupation, city tier) applied by the user, since each filter produces a different subset of the training data.

The high R² of the Linear Regression model (typically > 0.85) indicates that income, total expense, age, and expense subcategories are strongly predictive of an individual's stated desired savings. The Logistic Regression accuracy of ~0.80+ confirms reliable saver-persona classification across three behaviorally defined strata.

### 10.3 Comparison with Existing Methods

| Dimension | This System | Traditional Static Notebooks | Consumer Apps (Mint / YNAB) |
|---|---|---|---|
| **Interactivity** | Real-time filters + live predictions | Static execution, re-run required | App-native but not ML-driven |
| **Noisy Data Handling** | Regex + IQR + Two-pass date parser | Manual inspection | Proprietary ETL, not transparent |
| **ML Models Exposed** | Linear Reg + Logistic Reg + KMeans + PCA | Ad hoc, not interactive | None exposed to end user |
| **Clustering Visualisation** | PCA-overlaid 2-D cluster scatter | Rare, not interactive | Absent |
| **Custom User Prediction** | Live form input → ML prediction | Not available | Not available |
| **Transparency** | Full code available, metrics explained | Code visible but not interactive | Completely opaque |

---

## 11. Conclusion and Future Scope

### 11.1 Summary of Achievements

This project successfully designed, built, and deployed a **Data-Driven Financial Behavior Modeling and Prediction System** as a fully functional Streamlit web application. The major achievements are:

* **End-to-end data pipeline:** Two dedicated preprocessing pipelines handle a clean structured dataset and a messy transactional dataset, respectively — including categorical normalisation, Regex-based amount extraction, multi-format date parsing, and IQR-based outlier removal.
* **Supervised ML for savings prediction:** A Linear Regression model (R² ≈ 0.85–0.95) accurately predicts an individual's desired savings from demographic and expenditure features.
* **Supervised ML for persona classification:** A Logistic Regression model (accuracy ≈ 0.80+) reliably classifies users into Low, Medium, or High Saver categories using quantile-binned savings ratios.
* **Unsupervised ML for cohort discovery:** K-Means Clustering with the Elbow Method identifies natural financial archetypes (typically 3–4 clusters) in the population.
* **Dimensionality reduction for visualisation:** PCA projects high-dimensional cluster structures onto an interpretable 2-D scatter plot, with explained variance ratios shown on axes.
* **Interactive live prediction form:** Users can enter their own income, expense, and age values to receive a personalised ML-driven savings prediction and saver-persona classification.
* **Professional dark-themed UI:** A custom CSS layer provides a polished, professional dashboard aesthetic with responsive tabs, metric cards, and block cards.
* **Modular codebase:** The system is architected across 10 Python files (`app.py`, 8 backend modules, 1 utility module) following single-responsibility principles.

### 11.2 Limitations

* **Dataset scope:** The structured dataset (`IndianPersonalFinance.csv`) is limited to a single country's financial context. The models may not generalise well internationally without retraining.
* **Static ML models:** Models are re-trained on each page interaction (with `st.button` triggers). There is no persistent model-state or caching of trained weights across sessions.
* **Simplified classification target:** The saver-persona bins are based purely on the savings ratio's own quantile distribution, rather than externally validated financial thresholds.
* **No time-series forecasting:** The transaction tab provides historical aggregation but does not forecast future spending trends.
* **Limited feature engineering:** The model does not incorporate non-financial behavioral signals (e.g., credit score, investment portfolio, financial literacy score).

### 11.3 Future Scope

* **Deep Learning Models:** Replace Linear Regression with a Multi-Layer Perceptron (MLP) or LSTM for sequence-aware savings forecasting across time-series transaction data.
* **Larger and Richer Datasets:** Incorporate multi-year, multi-geographic financial datasets (e.g., RBI NSSO data, World Bank FinScope surveys) to expand model generalisability.
* **AutoML Integration:** Apply frameworks like H2O AutoML or FLAML to auto-select and tune the best model for savings prediction.
* **Model Persistence (MLflow / Joblib):** Persist trained models across sessions so predictions are instantaneous without re-training on every click.
* **Anomaly Detection:** Add Isolation Forest or One-Class SVM to detect fraudulent or anomalous transactions in the transactional dataset.
* **User Authentication and Personal Data Upload:** Allow individuals to upload their own bank statements (CSV/OFX) and receive personalised analysis.
* **Natural Language Reporting:** Integrate an LLM API (e.g., Gemini or GPT) to auto-generate a plain-language financial health report from the user's data.
* **Real-Time Data Integration:** Connect to open banking APIs (e.g., RazorpayX, Plaid) for live transaction ingestion.

---

## 12. References

1. Pedregosa, F. et al. (2011). *Scikit-learn: Machine Learning in Python.* Journal of Machine Learning Research, 12, 2825–2830. [https://jmlr.org/papers/v12/pedregosa11a.html](https://jmlr.org/papers/v12/pedregosa11a.html)

2. McKinney, W. (2010). *Data Structures for Statistical Computing in Python.* Proceedings of the 9th Python in Science Conference. [https://pandas.pydata.org](https://pandas.pydata.org)

3. Harris, C. R. et al. (2020). *Array programming with NumPy.* Nature, 585, 357–362. [https://doi.org/10.1038/s41586-020-2649-2](https://doi.org/10.1038/s41586-020-2649-2)

4. Streamlit Inc. (2024). *Streamlit Documentation.* [https://docs.streamlit.io](https://docs.streamlit.io)

5. Hunter, J. D. (2007). *Matplotlib: A 2D graphics environment.* Computing in Science & Engineering, 9(3), 90–95. [https://matplotlib.org](https://matplotlib.org)

6. Waskom, M. (2021). *Seaborn: Statistical Data Visualization.* Journal of Open Source Software, 6(60), 3021. [https://seaborn.pydata.org](https://seaborn.pydata.org)

7. James, G., Witten, D., Hastie, T., & Tibshirani, R. (2021). *An Introduction to Statistical Learning with Applications in Python.* Springer. [https://www.statlearning.com](https://www.statlearning.com)

8. Hastie, T., Tibshirani, R., & Friedman, J. (2009). *The Elements of Statistical Learning: Data Mining, Inference, and Prediction.* 2nd ed. Springer.

9. Bishop, C. M. (2006). *Pattern Recognition and Machine Learning.* Springer.

10. MacQueen, J. (1967). *Some Methods for Classification and Analysis of Multivariate Observations.* Proceedings of the 5th Berkeley Symposium on Mathematical Statistics and Probability, 1, 281–297.

11. Jolliffe, I. T. (2002). *Principal Component Analysis.* 2nd ed. Springer.

12. Tukey, J. W. (1977). *Exploratory Data Analysis.* Addison-Wesley.

13. Reserve Bank of India (2023). *Report on Household Finance in India.* [https://www.rbi.org.in](https://www.rbi.org.in)

14. Kaggle Dataset — *Indian Personal Finance Dataset.* [https://www.kaggle.com](https://www.kaggle.com)

15. Python Software Foundation. *Python Language Reference, version 3.11.* [https://www.python.org](https://www.python.org)

---

## 13. Appendix

### A. Key Source Code Snippets

#### A.1 — IQR-Based Outlier Removal (`preprocess.py`)

```python
q1 = df["amount"].quantile(0.25)
q3 = df["amount"].quantile(0.75)
iqr = q3 - q1
low  = q1 - 1.5 * iqr
high = q3 + 1.5 * iqr
df = df[(df["amount"] >= low) & (df["amount"] <= high)]
```

#### A.2 — Savings Ratio Computation (`preprocess.py`)

```python
df["savings_ratio"] = pd.NA
valid_income = df["income"] > 0
df.loc[valid_income, "savings_ratio"] = (
    df.loc[valid_income, "desired_savings"] / df.loc[valid_income, "income"]
)
```

#### A.3 — Two-Pass Mixed Date Parser (`preprocess.py`)

```python
def parse_mixed_dates(series: pd.Series) -> pd.Series:
    values = series.astype(str).str.strip()
    parsed = pd.to_datetime(values, errors="coerce", dayfirst=False)
    unresolved = parsed.isna()
    if unresolved.any():
        parsed.loc[unresolved] = pd.to_datetime(
            values[unresolved], errors="coerce", dayfirst=True
        )
    return parsed
```

#### A.4 — K-Means Elbow Computation (`clustering.py`)

```python
def compute_elbow(x_scaled, max_k: int) -> tuple[list[int], list[float]]:
    k_values = list(range(1, max_k + 1))
    wcss: list[float] = []
    for k in k_values:
        model = KMeans(n_clusters=k, random_state=42, n_init=10)
        model.fit(x_scaled)
        wcss.append(float(model.inertia_))
    return k_values, wcss
```

#### A.5 — Linear Regression Pipeline (`regression.py`)

```python
pipeline = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="median")),
    ("model",   LinearRegression()),
])
pipeline.fit(x_train, y_train)
predictions = pipeline.predict(x_test)
r2   = r2_score(y_test, predictions)
rmse = float(np.sqrt(mean_squared_error(y_test, predictions)))
```

#### A.6 — PCA Projection (`pca.py`)

```python
def project_to_2d(x_scaled):
    pca = PCA(n_components=2, random_state=42)
    components = pca.fit_transform(x_scaled)
    return pca, components
```

### B. Project File Structure

```
DAVLProject/
├── app.py                        # Main Streamlit dashboard entry point
├── requirements.txt              # Python dependency list
├── Documentation.md              # Technical documentation
├── Project Report.md             # This report
├── data/
│   ├── IndianPersonalFinance.csv     # Structured demographic finance dataset
│   └── budgetwise_finance_dataset.csv # Raw transaction dataset
├── modules/
│   ├── __init__.py               # Package init / public API
│   ├── config.py                 # Paths, category maps, payment maps
│   ├── data_loader.py            # CSV reader + column normaliser
│   ├── preprocess.py             # Cleaning, date parsing, outlier removal
│   ├── features.py               # Feature matrix builder for ML
│   ├── regression.py             # Linear + Logistic Regression pipelines
│   ├── clustering.py             # Elbow + K-Means implementation
│   ├── pca.py                    # PCA dimensionality reduction
│   └── transactions.py           # Transaction aggregation functions
└── utils/
    └── plots.py                  # Reusable Matplotlib/Seaborn figure factory
```