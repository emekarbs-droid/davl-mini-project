"""
Financial behavior modeling modules.

This package contains the core business logic, statistical models, and ML routines 
for the Financial Behavior Analysis system. 

Modules:
- clustering: K-Means clustering, Elbow method curve generation.
- config: Configuration and categorical mappings.
- data_loader: Functions to read and validate the source CSV data.
- features: Feature engineering for ML modeling.
- pca: Principal Component Analysis routines.
- preprocess: Data cleaning, formatting, and outlier handling.
- regression: Predictive modeling for Savings and Logistic Classification.
- transactions: Group-by aggregations for the real-world transactions.
"""

__all__ = [
    "clustering",
    "config",
    "data_loader",
    "features",
    "pca",
    "preprocess",
    "regression",
    "transactions",
]
