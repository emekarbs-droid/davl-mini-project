from fastapi import FastAPI
import pandas as pd

from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, r2_score

from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

app = FastAPI()

# -------------------------------
# LOAD DATA
# -------------------------------
try:
    df = pd.read_csv("ncr_ride_bookings.csv")
    df = df.sample(min(1000, len(df)))
    df = df.ffill().bfill()

    encoded_df = df.copy()
    le = LabelEncoder()

    for col in encoded_df.select_dtypes(include='object').columns:
        encoded_df[col] = le.fit_transform(encoded_df[col])

except Exception as e:
    df = None
    encoded_df = None
    error_msg = str(e)

@app.get("/")
def home():
    return {"message": "Backend running 🚀"}

# -------------------------------
# EDA TABLE
# -------------------------------
@app.get("/eda")
def eda():
    try:
        num = df.select_dtypes(include='number')

        eda_table = pd.DataFrame({
            "Feature": num.columns,
            "Mean": num.mean().values,
            "Median": num.median().values,
            "Std Dev": num.std().values,
            "Min": num.min().values,
            "Max": num.max().values
        })

        return {"table": eda_table.to_dict(orient="records")}

    except Exception as e:
        return {"error": str(e)}

# -------------------------------
# PCA
# -------------------------------
@app.get("/pca")
def pca():
    try:
        num = encoded_df.select_dtypes(include='number')
        num = num.fillna(num.mean())

        scaler = StandardScaler()
        scaled = scaler.fit_transform(num)

        pca = PCA(n_components=2)
        result = pca.fit_transform(scaled)

        return {
            "data": result.tolist(),
            "variance": pca.explained_variance_ratio_.tolist()
        }

    except Exception as e:
        return {"error": str(e)}

# -------------------------------
# MODELS
# -------------------------------
@app.get("/models")
def models():
    try:
        num = encoded_df.select_dtypes(include='number').dropna()

        X = num.iloc[:, :-1]
        y = num.iloc[:, -1]

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        lr = LinearRegression().fit(X_train, y_train)
        lr_score = r2_score(y_test, lr.predict(X_test))

        log = LogisticRegression(max_iter=200).fit(X_train, y_train)
        log_score = accuracy_score(y_test, log.predict(X_test))

        dt = DecisionTreeClassifier().fit(X_train, y_train)
        dt_score = accuracy_score(y_test, dt.predict(X_test))

        rf = RandomForestClassifier().fit(X_train, y_train)
        rf_score = accuracy_score(y_test, rf.predict(X_test))

        return {
            "Linear Regression": float(lr_score),
            "Logistic Regression": float(log_score),
            "Decision Tree": float(dt_score),
            "Random Forest": float(rf_score)
        }

    except Exception as e:
        return {"error": str(e)}