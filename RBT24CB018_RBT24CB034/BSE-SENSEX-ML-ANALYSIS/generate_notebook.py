import json

notebook = {
  "cells": [],
  "metadata": {
    "colab": {"name": "SENSEX_Analysis.ipynb", "provenance": []},
    "kernelspec": {"display_name": "Python 3", "name": "python3"},
    "language_info": {"name": "python"}
  },
  "nbformat": 4,
  "nbformat_minor": 0
}

def add_md(text):
    notebook["cells"].append({"cell_type": "markdown", "metadata": {}, "source": [text]})

def add_code(code):
    notebook["cells"].append({"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": [line + '\n' for line in code.split('\n')]})

add_md("# End-to-End SENSEX Analysis\nThis notebook fulfills all 6 objectives on the provided `BSE SENSEX.csv`.")
add_md("## 1️⃣ Objective: Data Loading and Understanding")
add_code("""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Ensure the 'BSE SENSEX.csv' file is uploaded to your Colab environment
df = pd.read_csv("BSE SENSEX.csv")

display(df.head())
print("\\n--- Dataset Info ---")
df.info()
print("\\n--- Summary Statistics ---")
display(df.describe())""")

add_md("## 2️⃣ Objective: Data Preprocessing and Cleaning")
add_code("""print("Missing values:")
display(df.isnull().sum())

# Handling missing values
df.fillna(method='ffill', inplace=True)

# Data transformation
df['Date'] = pd.to_datetime(df['Date'])
df.sort_values('Date', inplace=True)

print("\\nData after preprocessing:")
display(df.head())""")

add_md("## 3️⃣ Objective: Exploratory Data Analysis (EDA)")
add_code("""sns.set_theme(style="whitegrid")

plt.figure(figsize=(14, 6))
plt.plot(df['Date'], df['Close'], color='blue')
plt.title('SENSEX Closing Price Over Time', fontsize=16)
plt.xlabel('Date')
plt.ylabel('Closing Price')
plt.show()

# Daily Returns
df['Daily_Return'] = df['Close'].pct_change() * 100
plt.figure(figsize=(10, 5))
sns.histplot(df['Daily_Return'].dropna(), bins=50, kde=True, color='green')
plt.title('Daily Returns Distribution', fontsize=16)
plt.show()""")

add_md("## 4️⃣ Objective: Identify Relationships Between Features")
add_code("""numeric_cols = ['Open', 'High', 'Low', 'Close', 'Daily_Return']
corr_matrix = df[numeric_cols].corr()

plt.figure(figsize=(8, 6))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Correlation Matrix')
plt.show()

sample_df = df[['Open', 'High', 'Low', 'Close']].dropna().sample(n=min(500, len(df)), random_state=42)
sns.pairplot(sample_df, corner=True)
plt.show()""")

add_md("## 5️⃣ Objective: Dimensionality Reduction (PCA)")
add_code("""from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

features = ['Open', 'High', 'Low']
X_pca_input = df[features].dropna()

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_pca_input)

pca = PCA(n_components=2)
principal_components = pca.fit_transform(X_scaled)
pca_df = pd.DataFrame(data=principal_components, columns=['PC1', 'PC2'])

print("Explained Variance Ratio:", pca.explained_variance_ratio_)

plt.figure(figsize=(8, 6))
plt.scatter(pca_df['PC1'], pca_df['PC2'], alpha=0.5, c='purple')
plt.title('PCA of Features')
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.show()""")

add_md("## 6️⃣ Objective: Build a Prediction Model (Linear Regression)")
add_code("""from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

df_model = df.dropna().copy()
X = df_model[['Open', 'High', 'Low']]
y = df_model['Close']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, shuffle=False)

model = LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"RMSE: {rmse:.2f}")
print(f"MAE: {mae:.2f}")
print(f"R-squared: {r2:.4f}")

plt.figure(figsize=(14, 6))
plt.plot(df_model['Date'].iloc[X_test.index], y_test, label='Actual')
plt.plot(df_model['Date'].iloc[X_test.index], y_pred, label='Predicted', linestyle='--')
plt.title('Actual vs Predicted Closing Price')
plt.legend()
plt.show()""")

with open("SENSEX_Analysis.ipynb", "w", encoding='utf-8') as f:
    json.dump(notebook, f, indent=2)
print("Notebook created successfully!")
