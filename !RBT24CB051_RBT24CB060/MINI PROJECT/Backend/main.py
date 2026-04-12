from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np
from io import StringIO
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA, FactorAnalysis
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, mean_squared_error
from scipy.stats import skew
import warnings
warnings.filterwarnings("ignore")

app = FastAPI(title="DAVL Studio API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"status": "DAVL Studio API is running"}


@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    # ── Read CSV ──────────────────────────────────────────────────────────────
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are accepted.")

    content = await file.read()
    try:
        df = pd.read_csv(StringIO(content.decode("utf-8")))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse CSV: {str(e)}")

    total_rows, total_columns = df.shape

    # ── Missing values ────────────────────────────────────────────────────────
    missing_values = df.isnull().sum().to_dict()
    missing_values = {k: int(v) for k, v in missing_values.items()}
    total_missing = int(df.isnull().sum().sum())

    # ── Detect and validate numeric columns ───────────────────────────────────
    for col in df.columns:
        if "date" in col.lower():
            df[col] = pd.to_datetime(df[col], errors="coerce")

    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()

    # Remove zero-variance columns
    numeric_cols = [c for c in numeric_cols if df[c].std() > 0]

    if len(numeric_cols) < 2:
        raise HTTPException(
            status_code=400,
            detail="CSV must have at least 2 numeric columns with non-zero variance."
        )

    # ── Prepare data ──────────────────────────────────────────────────────────
    numeric_df = df[numeric_cols].copy()
    numeric_df = numeric_df.fillna(numeric_df.mean())

    feature_cols = numeric_cols[:-1]
    target_col = numeric_cols[-1]

    X = numeric_df[feature_cols].values
    y = numeric_df[target_col].values

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # ── Correlation matrix ────────────────────────────────────────────────────
    corr_matrix = numeric_df.corr().values.tolist()
    corr_cols = numeric_cols

    # Top correlated pair (excluding diagonal) — fix: copy before fill_diagonal
    corr_abs = numeric_df.corr().abs()
    corr_abs_copy = corr_abs.values.copy()
    np.fill_diagonal(corr_abs_copy, 0)
    top_pair_idx = np.unravel_index(corr_abs_copy.argmax(), corr_abs_copy.shape)
    top_pair = [
        corr_cols[top_pair_idx[0]],
        corr_cols[top_pair_idx[1]],
        float(numeric_df.corr().iloc[top_pair_idx[0], top_pair_idx[1]])
    ]

    # High correlation count (|r| > 0.75, excluding diagonal)
    high_corr_count = int(
        ((corr_abs_copy > 0.75)).sum() // 2
    )

    # Top predictor of target
    target_corrs = numeric_df[feature_cols].corrwith(numeric_df[target_col]).abs()
    top_predictor = [target_corrs.idxmax(), float(target_corrs.max())]

    # ── PCA ───────────────────────────────────────────────────────────────────
    n_pca = min(2, X_scaled.shape[1])
    pca = PCA(n_components=n_pca)
    X_pca = pca.fit_transform(X_scaled)
    variance_explained = (pca.explained_variance_ratio_ * 100).tolist()
    total_variance = float(sum(variance_explained))
    pca_projected = X_pca.tolist()

    # ── LDA ───────────────────────────────────────────────────────────────────
    y_mean = float(np.mean(y))
    labels = (y >= y_mean).astype(int).tolist()
    y_binary = np.array(labels)

    lda = LinearDiscriminantAnalysis(n_components=1)
    X_lda = lda.fit_transform(X_scaled, y_binary)
    lda_projected = X_lda.flatten().tolist()
    lda_accuracy = float(lda.score(X_scaled, y_binary))
    lda_threshold = float(np.mean(lda_projected))
    lda_components = 1

    # ── Factor Analysis ───────────────────────────────────────────────────────
    n_fa = min(2, X_scaled.shape[1])
    fa = FactorAnalysis(n_components=n_fa, random_state=42)
    fa.fit(X_scaled)
    fa_loadings = fa.components_.T.tolist()

    top_feature_per_factor = []
    for f in range(n_fa):
        col_loadings = np.abs(fa.components_[f])
        best_idx = int(np.argmax(col_loadings))
        top_feature_per_factor.append([
            feature_cols[best_idx],
            float(fa.components_[f][best_idx])
        ])

    # ── Linear Regression ─────────────────────────────────────────────────────
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42
    )
    lr = LinearRegression()
    lr.fit(X_train, y_train)
    y_pred = lr.predict(X_test)
    mse = float(mean_squared_error(y_test, y_pred))
    rmse = float(np.sqrt(mse))
    r2 = float(lr.score(X_test, y_test))

    # ── Classification ────────────────────────────────────────────────────────
    Xc_train, Xc_test, yc_train, yc_test = train_test_split(
        X_scaled, y_binary, test_size=0.2, random_state=42
    )

    log_clf = LogisticRegression(max_iter=1000, random_state=42)
    log_clf.fit(Xc_train, yc_train)
    acc_log = float(accuracy_score(yc_test, log_clf.predict(Xc_test)))

    dt_clf = DecisionTreeClassifier(max_depth=4, random_state=42)
    dt_clf.fit(Xc_train, yc_train)
    acc_dt = float(accuracy_score(yc_test, dt_clf.predict(Xc_test)))

    rf_clf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_clf.fit(Xc_train, yc_train)
    acc_rf = float(accuracy_score(yc_test, rf_clf.predict(Xc_test)))

    models = sorted([
        {"name": "Logistic Regression", "accuracy": acc_log},
        {"name": "Decision Tree", "accuracy": acc_dt},
        {"name": "Random Forest", "accuracy": acc_rf},
    ], key=lambda x: x["accuracy"], reverse=True)

    # ── Target stats ──────────────────────────────────────────────────────────
    target_skew = float(skew(y))
    target_values = y.tolist()

    # ── Build response ────────────────────────────────────────────────────────
    return {
        "correlation": {
            "matrix": corr_matrix,
            "columns": corr_cols,
            "topPair": top_pair,
            "highCorrCount": high_corr_count,
            "topPredictorOfTarget": top_predictor,
        },
        "pca": {
            "projected": pca_projected,
            "varianceExplained": variance_explained,
            "totalVariance": total_variance,
        },
        "lda": {
            "projected": lda_projected,
            "labels": labels,
            "accuracy": lda_accuracy,
            "threshold": lda_threshold,
            "ldComponents": lda_components,
        },
        "factorAnalysis": {
            "loadings": fa_loadings,
            "topFeaturePerFactor": top_feature_per_factor,
        },
        "regression": {
            "predictions": y_pred.tolist(),
            "actuals": y_test.tolist(),
            "mse": mse,
            "rmse": rmse,
            "r2": r2,
        },
        "classification": {
            "models": models,
        },
        "target": {
            "mean": float(np.mean(y)),
            "std": float(np.std(y)),
            "skew": target_skew,
            "values": target_values,
            "name": target_col,
        },
        "missingValues": missing_values,
        "totalRows": int(total_rows),
        "totalColumns": int(total_columns),
        "totalMissing": total_missing,
    }