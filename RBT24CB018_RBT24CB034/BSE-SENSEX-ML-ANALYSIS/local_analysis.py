import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

print("--- 1️⃣ Objective: Data Loading ---")
df = pd.read_csv("BSE SENSEX.csv")
print(df.head())
print("\n--- Dataset Info ---")
df.info()

print("\n--- 2️⃣ Objective: Data Preprocessing ---")
print("Missing values before:", df.isnull().sum().to_dict())
df.ffill(inplace=True)
df['Date'] = pd.to_datetime(df['Date'])
df.sort_values('Date', inplace=True)
print("Missing values after:", df.isnull().sum().to_dict())

print("\n--- 3️⃣ Objective: EDA & Statistical Analysis ---")
df['Daily_Return'] = df['Close'].pct_change() * 100
print(df['Daily_Return'].describe())

print("\n--- 4️⃣ Objective: Correlation ---")
numeric_cols = ['Open', 'High', 'Low', 'Close', 'Daily_Return']
corr = df[numeric_cols].corr()
print(corr)

print("\n--- 5️⃣ Objective: PCA ---")
features = ['Open', 'High', 'Low']
X_pca = df[features].dropna()
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_pca)
pca = PCA(n_components=2)
pca.fit(X_scaled)
print("PCA Explained Variance:", pca.explained_variance_ratio_)

print("\n--- 6️⃣ Objective: Linear Regression ---")
df_model = df.dropna().copy()
X = df_model[['Open', 'High', 'Low']]
y = df_model['Close']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, shuffle=False)

model = LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
print(f"RMSE: {np.sqrt(mean_squared_error(y_test, y_pred)):.2f}")
print(f"MAE: {mean_absolute_error(y_test, y_pred):.2f}")
print(f"R2 : {r2_score(y_test, y_pred):.4f}")
