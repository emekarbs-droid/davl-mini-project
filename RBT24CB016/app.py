import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.linear_model import LinearRegression
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import r2_score

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Airline Dashboard", layout="wide")

st.title("✈ Airline Passenger Satisfaction Dashboard")

# ---------------- LOAD DATA ----------------
try:
    df = pd.read_csv("airline.csv", encoding='latin1')
except:
    st.error("Dataset not found. Please upload airline.csv")
    st.stop()

# ---------------- CLEAN DATA ----------------
df = df.drop_duplicates()

for col in df.columns:
    if df[col].dtype == "object":
        df[col] = df[col].fillna("Unknown")
    else:
        df[col] = df[col].fillna(0)

# Encode categorical
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()

for col in df.select_dtypes(include='object').columns:
    try:
        df[col] = le.fit_transform(df[col])
    except:
        pass

# ---------------- SIDEBAR ----------------
menu = st.sidebar.radio("Select Option", [
    "Home",
    "EDA",
    "Correlation",
    "Regression",
    "PCA",
    "Clustering"
])

# ---------------- HOME ----------------
if menu == "Home":
    st.subheader("Dataset Preview")
    st.write(df.head())
    st.write("Shape:", df.shape)

# ---------------- EDA ----------------
elif menu == "EDA":
    st.subheader("Histograms (Numerical Features)")

    num_df = df.select_dtypes(include=['int64','float64'])

    fig, ax = plt.subplots(figsize=(12,8))
    num_df.hist(ax=ax, bins=20)

    plt.tight_layout()
    st.pyplot(fig)

# ---------------- CORRELATION ----------------
elif menu == "Correlation":
    st.subheader("Correlation Heatmap")

    fig, ax = plt.subplots(figsize=(10,6))
    sns.heatmap(df.corr(), cmap="coolwarm", ax=ax)

    st.pyplot(fig)

# ---------------- REGRESSION ----------------
elif menu == "Regression":
    st.subheader("Linear Regression")

    col1 = st.selectbox("Select X", df.columns)
    col2 = st.selectbox("Select Y", df.columns)

    try:
        X = df[[col1]]
        Y = df[col2]

        model = LinearRegression()
        model.fit(X, Y)
        pred = model.predict(X)

        score = r2_score(Y, pred)
        st.write("R² Score:", score)
    except:
        st.error("Invalid column selection")

# ---------------- PCA ----------------
elif menu == "PCA":
    st.subheader("PCA Result")

    try:
        pca = PCA(n_components=2)
        result = pca.fit_transform(df)

        st.write(result)
    except:
        st.error("PCA failed")

# ---------------- CLUSTERING ----------------
elif menu == "Clustering":
    st.subheader("K-Means Clustering")

    k = st.slider("Select clusters", 2, 10, 3)

    try:
        model = KMeans(n_clusters=k, n_init=10)
        df["Cluster"] = model.fit_predict(df)

        st.write(df.head())
        st.scatter_chart(df["Cluster"])
    except:
        st.error("Clustering failed")
