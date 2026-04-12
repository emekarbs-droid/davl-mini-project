import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA

from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor

from sklearn.metrics import accuracy_score, r2_score


def preprocess_data(df, target):
    df = df.copy()

    # Drop missing values
    df = df.dropna()

    # Encode categorical
    le = LabelEncoder()
    for col in df.select_dtypes(include='object').columns:
        df[col] = le.fit_transform(df[col])

    X = df.drop(target, axis=1)
    y = df[target]

    # Scale
    scaler = StandardScaler()
    X = scaler.fit_transform(X)

    return X, y


def detect_problem_type(y):
    if y.nunique() <= 10:
        return "classification"
    return "regression"


def run_models(X, y, problem_type):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    results = {}

    if problem_type == "classification":
        # Logistic
        log = LogisticRegression(max_iter=200)
        log.fit(X_train, y_train)
        pred = log.predict(X_test)
        results["Logistic Regression"] = accuracy_score(y_test, pred)

        # Decision Tree
        dt = DecisionTreeClassifier()
        dt.fit(X_train, y_train)
        pred = dt.predict(X_test)
        results["Decision Tree"] = accuracy_score(y_test, pred)

        # Random Forest
        rf = RandomForestClassifier()
        rf.fit(X_train, y_train)
        pred = rf.predict(X_test)
        results["Random Forest"] = accuracy_score(y_test, pred)

    else:
        # Linear Regression
        lr = LinearRegression()
        lr.fit(X_train, y_train)
        pred = lr.predict(X_test)
        results["Linear Regression"] = r2_score(y_test, pred)

        # Random Forest Regressor
        rf = RandomForestRegressor()
        rf.fit(X_train, y_train)
        pred = rf.predict(X_test)
        results["Random Forest Regressor"] = r2_score(y_test, pred)

    return results


def apply_pca(X):
    pca = PCA(n_components=2)
    return pca.fit_transform(X)