from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


def run_regression(df: pd.DataFrame, feature_frame: pd.DataFrame, target_column: str) -> dict:
    """
    Sets up the Linear Regression process using imputed median values 
    to train on standard user data.
    Returns model context and calculated R2 / RMSE metrics.
    """
    x = pd.get_dummies(feature_frame, drop_first=True)
    y = df[target_column]

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
    pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("model", LinearRegression()),
        ]
    )
    pipeline.fit(x_train, y_train)
    predictions = pipeline.predict(x_test)

    return {
        "model": pipeline,
        "x_test": x_test,
        "y_test": y_test,
        "predictions": predictions,
        "r2": r2_score(y_test, predictions),
        "rmse": float(np.sqrt(mean_squared_error(y_test, predictions))),
    }


def run_saver_classification(df: pd.DataFrame, feature_frame: pd.DataFrame, percentage_column: str) -> dict:
    x = pd.get_dummies(feature_frame, drop_first=True)

    bins = df[percentage_column].quantile([0, 1 / 3, 2 / 3, 1]).values
    bins = np.unique(bins)
    if len(bins) < 4:
        return {"available": False}

    labels = ["Low Saver", "Medium Saver", "High Saver"]
    y = pd.cut(df[percentage_column], bins=bins, labels=labels, include_lowest=True)

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42, stratify=y)
    pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler(with_mean=False)),
            ("model", LogisticRegression(max_iter=1200)),
        ]
    )
    pipeline.fit(x_train, y_train)
    predictions = pipeline.predict(x_test)

    return {
        "available": True,
        "model": pipeline,
        "labels": labels,
        "x_test": x_test,
        "y_test": y_test,
        "predictions": predictions,
        "accuracy": accuracy_score(y_test, predictions),
        "confusion_matrix": confusion_matrix(y_test, predictions, labels=labels),
    }
