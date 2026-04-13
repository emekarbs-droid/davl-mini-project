import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

API = "http://127.0.0.1:8000"

st.title("🚀 Data Visualization Dashboard")

# -------------------------------
# LOAD DATA
# -------------------------------
df = pd.read_csv("ncr_ride_bookings.csv").sample(500)
num = df.select_dtypes(include=['number'])

st.subheader("📊 Data Loading")
st.dataframe(df.head())

# -------------------------------
# EDA TABLE
# -------------------------------
st.subheader("📈 EDA Table")

eda = requests.get(f"{API}/eda").json()

if "table" in eda:
    eda_df = pd.DataFrame(eda["table"])
    st.dataframe(eda_df)

    st.write("""
    Observations:
    1. Data shows variation across features  
    2. Mean ≠ Median indicates skewness  
    3. Presence of outliers (Min/Max difference)  
    4. Std deviation shows spread  
    5. Some features need normalization  
    """)

# -------------------------------
# HEATMAP (FINAL FIXED)
# -------------------------------
st.subheader("🔥 Heatmap")

num = num.fillna(num.mean())
corr = num.corr()

plt.figure(figsize=(14,10))
sns.heatmap(corr, annot=True, fmt=".2f", linewidths=0.5)

plt.xticks(rotation=45, ha='right')
plt.yticks(rotation=0)
plt.tight_layout()

st.pyplot(plt)
plt.clf()

st.write("""
Observations:
1. Strong correlations between some features  
2. Some features weakly related  
3. Multicollinearity may exist  
4. Helps feature selection  
5. Shows relationships clearly  
""")

# -------------------------------
# HISTOGRAM
# -------------------------------
st.subheader("📊 Histogram")

num.hist(figsize=(12,8))
plt.tight_layout()
st.pyplot(plt)
plt.clf()

# -------------------------------
# BOX PLOT
# -------------------------------
st.subheader("📦 Box Plot")

plt.figure(figsize=(10,6))
num.plot(kind='box')
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(plt)
plt.clf()

# -------------------------------
# SCATTER
# -------------------------------
st.subheader("🔵 Scatter Plot")

cols = num.columns
if len(cols) >= 2:
    plt.figure(figsize=(6,4))
    plt.scatter(num[cols[0]], num[cols[1]])
    plt.xlabel(cols[0])
    plt.ylabel(cols[1])
    plt.tight_layout()
    st.pyplot(plt)
    plt.clf()

# -------------------------------
# PCA
# -------------------------------
st.subheader("🧠 PCA")

pca = requests.get(f"{API}/pca").json()

if "data" in pca:
    pca_df = pd.DataFrame(pca["data"], columns=["PC1","PC2"])

    plt.figure(figsize=(6,4))
    plt.scatter(pca_df["PC1"], pca_df["PC2"])
    plt.tight_layout()
    st.pyplot(plt)
    plt.clf()

# -------------------------------
# MODELS
# -------------------------------
st.subheader("🤖 Model Comparison")

models = requests.get(f"{API}/models").json()

if "error" not in models:
    st.dataframe(pd.DataFrame(models.items(), columns=["Model","Score"]))

    plt.figure(figsize=(8,5))
    plt.bar(models.keys(), models.values())
    plt.xticks(rotation=30)
    plt.tight_layout()
    st.pyplot(plt)
    plt.clf()

# -------------------------------
# FINAL CONCLUSION
# -------------------------------
st.subheader("🏁 Conclusion")

st.write("""
• EDA performed successfully  
• Visualizations reveal patterns  
• PCA reduces dimensionality  
• ML models compared  
• Random Forest performs best  
""")
