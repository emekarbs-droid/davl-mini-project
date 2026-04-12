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
# 🎯 Title
# ---------------------------
st.title("✈️ Airlines ML Dashboard (Complete)")

# ---------------------------
# 📂 Load Dataset
# ---------------------------
df = pd.read_csv("Airlines.csv")

st.subheader("Dataset Preview")
st.write(df.head())

# ---------------------------
# 🔄 Encode categorical
# ---------------------------
le = LabelEncoder()
for col in df.select_dtypes(include='object').columns:
    df[col] = le.fit_transform(df[col])

# ---------------------------
# 📊 EDA SECTION
# ---------------------------
st.header("📊 Exploratory Data Analysis")

# Histogram
st.subheader("Histogram")
fig1 = plt.figure()
df['Length'].hist()
plt.title("Flight Length Distribution")
st.pyplot(fig1)

# Boxplot
st.subheader("Boxplot")
fig2 = plt.figure()
df.plot(kind='box')
st.pyplot(fig2)

# Scatter Plot
st.subheader("Scatter Plot (Time vs Length)")
fig3 = plt.figure()
plt.scatter(df['Time'], df['Length'])
plt.xlabel("Time")
plt.ylabel("Length")
st.pyplot(fig3)

# Heatmap
st.subheader("Heatmap")
fig4 = plt.figure()
sns.heatmap(df.corr())
st.pyplot(fig4)

# Pair Plot (sample)
st.subheader("Pair Plot")
df_sample = df.sample(1000)
pair = sns.pairplot(df_sample[['Flight','Time','Length','Delay']], hue='Delay')
st.pyplot(pair)

# ---------------------------
# 📉 PCA
# ---------------------------
st.header("📉 PCA")

X = df.drop('Delay', axis=1)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

pca = PCA(n_components=3)
pca_result = pca.fit_transform(X_scaled)

explained_var = pca.explained_variance_ratio_

# Bar graph
fig5 = plt.figure()
components = ['PC1','PC2','PC3']
plt.bar(components, explained_var)
plt.title("PCA Variance")
st.pyplot(fig5)

# ---------------------------
# 🤖 MODELS
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
# 📊 Show Results
# ---------------------------
st.subheader("Model Accuracy")

for model, acc in results.items():
    st.write(f"{model}: {acc:.4f}")

# ---------------------------
# 📊 Comparison Graph
# ---------------------------
fig6 = plt.figure()
plt.bar(results.keys(), results.values())
plt.xticks(rotation=30)
plt.title("Model Comparison")
st.pyplot(fig6)

# ---------------------------
# 🏆 Best Model
# ---------------------------
best_model = max(results, key=results.get)
