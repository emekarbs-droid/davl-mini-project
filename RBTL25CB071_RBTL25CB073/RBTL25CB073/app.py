from flask import Flask, render_template
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.decomposition import PCA
from sklearn.metrics import mean_squared_error, r2_score

app = Flask(__name__)

# Create output folder if not exists
os.makedirs("static/output", exist_ok=True)

# Load dataset
df = pd.read_csv("smartphones.csv")

# Fill missing values
df = df.fillna(df.select_dtypes(include='number').mean())

# Select numeric columns
numeric_df = df.select_dtypes(include='number')

# Target column (last numeric column)
target = numeric_df.columns[-1]

# Features and target
X = numeric_df.drop(columns=[target])
y = numeric_df[target]

# Train test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ---------------- HEATMAP ----------------
plt.figure(figsize=(8,6))
sns.heatmap(numeric_df.corr(), annot=True)
plt.savefig("static/output/heatmap.png")
plt.close()

# ---------------- HISTOGRAM ----------------
numeric_df.hist(figsize=(10,8))
plt.savefig("static/output/histogram.png")
plt.close()

# ---------------- BOX PLOT ----------------
plt.figure(figsize=(10,6))
sns.boxplot(data=numeric_df)
plt.savefig("static/output/boxplot.png")
plt.close()

# ---------------- SCATTER PLOT ----------------
if len(numeric_df.columns) >= 2:
    plt.figure(figsize=(6,4))
    plt.scatter(numeric_df.iloc[:,0], numeric_df.iloc[:,1])
    plt.xlabel(numeric_df.columns[0])
    plt.ylabel(numeric_df.columns[1])
    plt.savefig("static/output/scatter.png")
    plt.close()

# ---------------- PCA ----------------
pca = PCA(n_components=2)
pca_result = pca.fit_transform(X)

plt.figure(figsize=(6,4))
plt.scatter(pca_result[:,0], pca_result[:,1])
plt.savefig("static/output/pca.png")
plt.close()

# ---------------- LINEAR REGRESSION ----------------
lr = LinearRegression()
lr.fit(X_train, y_train)
lr_pred = lr.predict(X_test)
lr_score = r2_score(y_test, lr_pred)

# ---------------- LOGISTIC REGRESSION ----------------
y_class = (y > y.mean()).astype(int)

X_train2, X_test2, y_train2, y_test2 = train_test_split(X, y_class, test_size=0.2, random_state=42)

log_model = LogisticRegression(max_iter=1000)
log_model.fit(X_train2, y_train2)
log_score = log_model.score(X_test2, y_test2)

# ---------------- DECISION TREE ----------------
dt = DecisionTreeRegressor()
dt.fit(X_train, y_train)
dt_pred = dt.predict(X_test)
dt_score = r2_score(y_test, dt_pred)

# ---------------- RANDOM FOREST ----------------
rf = RandomForestRegressor()
rf.fit(X_train, y_train)
rf_pred = rf.predict(X_test)
rf_score = r2_score(y_test, rf_pred)

# ---------------- MODEL COMPARISON ----------------
models = ['Linear Regression', 'Logistic Regression', 'Decision Tree', 'Random Forest']
scores = [lr_score, log_score, dt_score, rf_score]

plt.figure(figsize=(8,5))
plt.bar(models, scores)
plt.savefig("static/output/model_comparison.png")
plt.close()

@app.route('/')
def home():
    return render_template(
        'index.html',
        rows=df.head().to_html(),
        lr=round(lr_score,2),
        log=round(log_score,2),
        dt=round(dt_score,2),
        rf=round(rf_score,2)
    )

if __name__ == '__main__':
    app.run(debug=True)