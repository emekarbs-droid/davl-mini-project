# ============================================
# IPL DATA ANALYSIS + ML (SINGLE CELL)
# ============================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ML Models
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

# Metrics
from sklearn.metrics import accuracy_score, mean_squared_error, r2_score

# ---------------------------
# LOAD DATA
# ---------------------------
matches = pd.read_csv("matches.csv")
deliveries = pd.read_csv("deliveries.csv")

print("Matches Data:")
print(matches.head())

# ---------------------------
# EDA
# ---------------------------
print("\nINFO:")
print(matches.info())

print("\nDESCRIPTION:")
print(matches.describe())

print("\nMISSING VALUES:")
print(matches.isnull().sum())

# ---------------------------
# DATA CLEANING
# ---------------------------
matches['winner'].fillna('No Result', inplace=True)
matches['player_of_match'].fillna('Unknown', inplace=True)

matches = matches.drop(columns=['umpire3'], errors='ignore')
matches.dropna(inplace=True)

# ---------------------------
# ENCODING
# ---------------------------
df = pd.get_dummies(matches, drop_first=True)

# ---------------------------
# HEATMAP
# ---------------------------
plt.figure(figsize=(10,6))
sns.heatmap(df.corr(), cmap='coolwarm')
plt.title("Heatmap")
plt.show()

# ---------------------------
# HISTOGRAM
# ---------------------------
df.hist(figsize=(12,8))
plt.show()

# ---------------------------
# BOXPLOT
# ---------------------------
plt.figure(figsize=(10,6))
sns.boxplot(data=df.select_dtypes(include=np.number))
plt.xticks(rotation=90)
plt.show()

# ---------------------------
# SCATTER PLOT
# ---------------------------
plt.scatter(df.iloc[:,0], df.iloc[:,1])
plt.title("Scatter Plot")
plt.show()

# ---------------------------
# PREPARE DATA
# ---------------------------
X = df.select_dtypes(include=np.number)

y = pd.get_dummies(matches['winner'], drop_first=True)
y = y.iloc[:,0]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ---------------------------
# LINEAR REGRESSION
# ---------------------------
lr = LinearRegression()
lr.fit(X_train, y_train)

y_pred_lr = lr.predict(X_test)

print("\nLinear Regression R2:", r2_score(y_test, y_pred_lr))
print("MSE:", mean_squared_error(y_test, y_pred_lr))

# ---------------------------
# LOGISTIC REGRESSION
# ---------------------------
log = LogisticRegression(max_iter=1000)
log.fit(X_train, y_train)

y_pred_log = log.predict(X_test)
log_acc = accuracy_score(y_test, y_pred_log)

print("\nLogistic Accuracy:", log_acc)

# ---------------------------
# DECISION TREE
# ---------------------------
dt = DecisionTreeClassifier()
dt.fit(X_train, y_train)

y_pred_dt = dt.predict(X_test)
dt_acc = accuracy_score(y_test, y_pred_dt)

print("Decision Tree Accuracy:", dt_acc)

# ---------------------------
# RANDOM FOREST
# ---------------------------
rf = RandomForestClassifier()
rf.fit(X_train, y_train)

y_pred_rf = rf.predict(X_test)
rf_acc = accuracy_score(y_test, y_pred_rf)

print("Random Forest Accuracy:", rf_acc)

# ---------------------------
# MODEL COMPARISON
# ---------------------------
results = {
    "Logistic Regression": log_acc,
    "Decision Tree": dt_acc,
    "Random Forest": rf_acc
}

print("\nModel Comparison:")
for model, score in results.items():
    print(model, ":", score)
