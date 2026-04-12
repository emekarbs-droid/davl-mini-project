import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg') # No popups locally
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from flask import Flask, render_template

app = Flask(__name__)

# Ensure directories exist
os.makedirs('static/images', exist_ok=True)
os.makedirs('templates', exist_ok=True)

print("Starting to load BSE SENSEX dataset...")
df_original = pd.read_csv("BSE SENSEX.csv")
missing_before = df_original.isnull().sum().to_dict()

df = df_original.copy()
df.ffill(inplace=True)
df['Date'] = pd.to_datetime(df['Date'])
df.sort_values('Date', inplace=True)
df['Daily_Return'] = df['Close'].pct_change() * 100
missing_after = df.isnull().sum().to_dict()

import io
# Data Info captured manually for display
buffer = io.StringIO()
df.info(buf=buffer)
info_str = buffer.getvalue()

def generate_eda_plot():
    if not os.path.exists('static/images/eda_close.png'):
        plt.figure(figsize=(10, 5))
        plt.plot(df['Date'], df['Close'], color='blue', linewidth=1.5)
        plt.title('SENSEX Closing Price Over Time', fontsize=14, color='white')
        plt.xlabel('Date', color='white')
        plt.ylabel('Closing Price (INR)', color='white')
        plt.tick_params(colors='white')
        plt.tight_layout()
        plt.savefig('static/images/eda_close.png', transparent=True)
        plt.close()
        
    if not os.path.exists('static/images/eda_return.png'):
        plt.figure(figsize=(10, 5))
        sns.histplot(df['Daily_Return'].dropna(), bins=50, kde=True, color='cyan')
        plt.title('Distribution of Daily Returns %', fontsize=14, color='white')
        plt.xlabel('Daily Return (%)', color='white')
        plt.ylabel('Frequency', color='white')
        plt.tick_params(colors='white')
        plt.tight_layout()
        plt.savefig('static/images/eda_return.png', transparent=True)
        plt.close()

def generate_corr_plot():
    if not os.path.exists('static/images/corr.png'):
        numeric_cols = ['Open', 'High', 'Low', 'Close', 'Daily_Return']
        corr_matrix = df[numeric_cols].corr()
        plt.figure(figsize=(8, 6))
        sns.heatmap(corr_matrix, annot=True, cmap='RdPu', fmt=".2f")
        plt.title('Correlation Matrix of Features', fontsize=14, color='white')
        plt.tick_params(colors='white')
        plt.tight_layout()
        plt.savefig('static/images/corr.png', transparent=False)
        plt.close()

def generate_pair_plot():
    if not os.path.exists('static/images/pair.png'):
        sample_df = df[['Open', 'High', 'Low', 'Close']].dropna().sample(n=min(500, len(df)), random_state=42)
        sns.pairplot(sample_df, corner=True, diag_kind="kde", plot_kws={'alpha':0.5, 'color':'#ff007f'})
        plt.tight_layout()
        plt.savefig('static/images/pair.png', transparent=False)
        plt.close()

def generate_pca_plot():
    features = ['Open', 'High', 'Low']
    X_pca = df[features].dropna()
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_pca)
    pca = PCA(n_components=2)
    principal_components = pca.fit_transform(X_scaled)
    
    if not os.path.exists('static/images/pca.png'):
        pca_df = pd.DataFrame(data=principal_components, columns=['PC1', 'PC2'])
        plt.figure(figsize=(8, 6))
        plt.scatter(pca_df['PC1'], pca_df['PC2'], alpha=0.6, c='#00ffcc')
        plt.title('2D PCA of SENSEX Features', fontsize=14, color='white')
        plt.xlabel('Principal Component 1', color='white')
        plt.ylabel('Principal Component 2', color='white')
        plt.grid(color='white', alpha=0.1)
        plt.tick_params(colors='white')
        plt.tight_layout()
        plt.savefig('static/images/pca.png', transparent=True)
        plt.close()
    return pca.explained_variance_ratio_.tolist()

def generate_lr_plot():
    df_model = df.dropna().copy()
    X = df_model[['Open', 'High', 'Low']]
    y = df_model['Close']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, shuffle=False)
    
    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    
    if not os.path.exists('static/images/lr.png'):
        plt.figure(figsize=(10, 5))
        test_dates = df_model.loc[X_test.index, 'Date']
        plt.plot(test_dates, y_test, label='Actual Close', color='#00ffcc', alpha=0.8)
        plt.plot(test_dates, y_pred, label='Predicted Close', color='#ff007f', linestyle='--', alpha=0.8)
        plt.title('Linear Regression: Actual vs Predicted', fontsize=14, color='white')
        plt.xlabel('Date', color='white')
        plt.ylabel('Closing Price', color='white')
        plt.legend()
        plt.tick_params(colors='white')
        plt.tight_layout()
        plt.savefig('static/images/lr.png', transparent=True)
        plt.close()
        
    mse = mean_squared_error(y_test, y_pred)
    return {
        'rmse': round(np.sqrt(mse), 2),
        'mae': round(mean_absolute_error(y_test, y_pred), 2),
        'r2': round(r2_score(y_test, y_pred), 4)
    }

print("Running Machine Learning Models & Generating Images...")
generate_eda_plot()
generate_corr_plot()
generate_pair_plot()
pca_var = generate_pca_plot()
lr_metrics = generate_lr_plot()
print("Images fully generated and saved to /static/images")

@app.route('/')
def index():
    df_head = df_original.head().to_html(classes='glass-table', index=False)
    df_tail = df_original.tail().to_html(classes='glass-table', index=False)
    desc = df.describe().round(2).to_html(classes='glass-table')
    
    return render_template('index.html', 
                            head=df_head, 
                            tail=df_tail, 
                            desc=desc,
                            info_str=info_str,
                            pca_var=pca_var,
                            lr_metrics=lr_metrics,
                            missing_before=missing_before,
                            missing_after=missing_after)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
