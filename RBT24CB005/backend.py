i# ================================
# COMPLETE AIRLINES ML DASHBOARD
# ================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA

from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import accuracy_score

# ---------------------------
# TITLE
# ---------------------------
st.title("✈️ Airlines ML Dashboard (Complete)")

# ---------------------------
# LOAD DATA
# ---------------------------
df = pd.read_csv("Airlines.csv")

st.subheader("Dataset Preview")
st.dataframe(df.head())

# ---------------------------
# ENCODING
# ---------------------------
le = LabelEncoder()
for col in df.select_dtypes(include='object').columns:
    df[col] = le.fit_transform(df[col])

# ---------------------------
# EDA
# ---------------------------
st.header("📊 Exploratory Data Analysis")

# Histogram
st.subheader("Histogram")
fig1, ax1 = plt.subplots()
df['Length'].hist(ax=ax1)
ax1.set_title("Flight Length Distribution")
st.pyplot(fig1)

# Boxplot
st.subheader("Boxplot")
fig2, ax2 = plt.subplots()
sns.boxplot(data=df, ax=ax2)
plt.xticks(rotation=90)
st.pyplot(fig2)

# Scatter
st.subheader("Scatter Plot (Time vs Length)")
fig3, ax3 = plt.subplots()
ax3.scatter(df['Time'], df['Length'])
ax3.set_xlabel("Time")
ax3.set_ylabel("Length")
st.pyplot(fig3)

# Heatmap
st.subheader("Heatmap")
fig4, ax4 = plt.subplots()
sns.heatmap(df.corr(), ax=ax4)
st.pyplot(fig4)

# Pairplot
st.subheader("Pair Plot")
df_sample = df.sample(min(500, len(df)))
pair = sns.pairplot(df_sample[['Flight','Time','Length','Delay']], hue='Delay')
st.pyplot(pair.fig)

# ---------------------------
# PCA
# ---------------------------
st.header("📉 PCA")

X = df.drop('Delay', axis=1)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

pca = PCA(n_components=3)
pca_result = pca.fit_transform(X_scaled)

explained_var = pca.explained_variance_ratio_

# PCA Bar Graph
fig5, ax5 = plt.subplots()
components = ['PC1','PC2','PC3']
ax5.bar(components, explained_var)
ax5.set_title("PCA Explained Variance")
st.pyplot(fig5)

# PCA Scatter
st.subheader("PCA Scatter Plot")
fig6, ax6 = plt.subplots()
scatter = ax6.scatter(pca_result[:,0], pca_result[:,1], c=df['Delay'], cmap='viridis')
ax6.set_xlabel("PC1")
ax6.set_ylabel("PC2")
plt.colorbar(scatter)
st.pyplot(fig6)

# ---------------------------
# MODEL TRAINING
# ---------------------------
st.header("🤖 Model Training & Comparison")

X = df.drop('Delay', axis=1)
y = df['Delay']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

results = {}

# Linear Regression
lr = LinearRegression()
lr.fit(X_train, y_train)
lr_pred = (lr.predict(X_test) > 0.5).astype(int)
results["Linear Regression"] = accuracy_score(y_test, lr_pred)

# Logistic Regression
log = LogisticRegression(max_iter=200, solver='liblinear')
log.fit(X_train, y_train)
log_pred = log.predict(X_test)
results["Logistic Regression"] = accuracy_score(y_test, log_pred)

# Decision Tree
dt = DecisionTreeClassifier()
dt.fit(X_train, y_train)
dt_pred = dt.predict(X_test)
results["Decision Tree"] = accuracy_score(y_test, dt_pred)

# Random Forest
rf = RandomForestClassifier(n_estimators=50)
rf.fit(X_train, y_train)
rf_pred = rf.predict(X_test)
results["Random Forest"] = accuracy_score(y_test, rf_pred)

# ---------------------------
# RESULTS DISPLAY
# ---------------------------
st.subheader("📊 Model Accuracy")

for model, acc in results.items():
    st.write(f"{model}: {acc:.4f}")

# Comparison Graph
fig7, ax7 = plt.subplots()
ax7.bar(results.keys(), results.values())
plt.xticks(rotation=30)
ax7.set_title("Model Comparison")
st.pyplot(fig7)

# Best Model
best_model = max(results, key=results.get)
st.success(f"🏆 Best Model: {best_model}")
