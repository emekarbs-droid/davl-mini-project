import os
import io
import traceback
from flask import Flask, render_template, request, send_file, flash, redirect, url_for
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from factor_analyzer import FactorAnalyzer

app = Flask(__name__)
app.secret_key = "super_secret_key"

# Simple global cache for download functionality
processed_df_cache = None

# ================================
# Data Processing Modules
# ================================

def preprocess_data(df):
    """Safely handles mixed data types by scaling only numerics and safely encoding categoricals."""
    processed_df = df.copy()
    
    # 1. Separate numerical and categorical
    num_cols = processed_df.select_dtypes(include=[np.number]).columns
    cat_cols = processed_df.select_dtypes(exclude=[np.number]).columns
    
    # 2. Impute missing values
    for col in num_cols:
        if processed_df[col].isnull().sum() > 0:
            processed_df[col] = processed_df[col].fillna(processed_df[col].median())
            
    for col in cat_cols:
        if processed_df[col].isnull().sum() > 0:
            processed_df[col] = processed_df[col].fillna(processed_df[col].mode()[0])
            
    # 3. Handle duplicates
    processed_df = processed_df.drop_duplicates().reset_index(drop=True)
    
    # 4. Scale ONLY originally numeric columns
    if len(num_cols) > 0:
        scaler = StandardScaler()
        processed_df[num_cols] = scaler.fit_transform(processed_df[num_cols])
        
    # 5. Encode Categorical Columns (do not scale them)
    for col in cat_cols:
        le = LabelEncoder()
        processed_df[col] = le.fit_transform(processed_df[col].astype(str))
        
    return processed_df

def generate_insights(raw_df, processed_df):
    """Auto-generate rule-based insights."""
    insights = []
    
    missing_pct = (raw_df.isnull().sum() / len(raw_df)) * 100
    high_missing = missing_pct[missing_pct > 20]
    if not high_missing.empty:
        insights.append(f"<div class='metric-card' style='border-left: 4px solid #ef4444; margin-bottom:15px;'><h4>High Missing Values</h4><p>Columns {list(high_missing.index)} have over 20% missing data.</p></div>")
        
    constants = [col for col in raw_df.columns if raw_df[col].nunique() <= 1]
    if constants:
        insights.append(f"<div class='metric-card' style='border-left: 4px solid #f59e0b; margin-bottom:15px;'><h4>Constant Columns</h4><p>{constants} have no variance and might be redundant.</p></div>")
        
    numeric_processed = processed_df.select_dtypes(include=[np.number])
    if len(numeric_processed.columns) > 1:
        corr = numeric_processed.corr().abs()
        upper = corr.where(np.triu(np.ones(corr.shape), k=1).astype(bool))
        high_corr = [column for column in upper.columns if any(upper[column] > 0.8)]
        if high_corr:
            insights.append(f"<div class='metric-card' style='border-left: 4px solid #10b981; margin-bottom:15px;'><h4>High Correlation</h4><p>{high_corr} are highly correlated (>0.8 magnitude) with other variables.</p></div>")
            
    if not numeric_processed.empty:
        skewness = numeric_processed.skew()
        high_skew = skewness[abs(skewness) > 1.0]
        if not high_skew.empty:
            insights.append(f"<div class='metric-card' style='border-left: 4px solid #8b5cf6; margin-bottom:15px;'><h4>Highly Skewed Features</h4><p>{list(high_skew.index)} have substantial skewness.</p></div>")
    
    return insights

# ================================
# Flask Routes
# ================================

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    global processed_df_cache
    
    if 'file' not in request.files:
        flash('No file part', 'error')
        return redirect(url_for('index'))
        
    file = request.files['file']
    if file.filename == '':
        flash('No selected file', 'error')
        return redirect(url_for('index'))
        
    # Retrieve target column for LDA
    lda_target = request.form.get('target_column')
        
    try:
        # Load Dataset safely
        if file.filename.endswith('.csv'):
            raw_df = pd.read_csv(file)
        else:
            raw_df = pd.read_excel(file)
            
        if raw_df.empty:
            flash("The dataset is empty.", "error")
            return redirect(url_for('index'))

        # Run safe Preprocessing
        processed_df = preprocess_data(raw_df)
        processed_df_cache = processed_df # save to cache for download

        # Context dict to pass to results.html
        context = {
            'data_preview': raw_df.head(10).to_html(classes=['table', 'table-striped'], index=False),
            'processed_preview': processed_df.head(10).to_html(classes=['table', 'table-striped'], index=False),
            'shape': raw_df.shape,
            'memory_mb': round(raw_df.memory_usage(deep=True).sum() / (1024 * 1024), 2),
            'dtypes': pd.DataFrame({"Data Type": raw_df.dtypes.astype(str)}).to_html(classes=['table', 'table-striped']),
            'summary_stats': processed_df.describe().T.to_html(classes=['table', 'table-striped']),
            'insights': generate_insights(raw_df, processed_df)
        }

        # Data Quality Section
        missing = raw_df.isnull().sum()
        missing_df = pd.DataFrame({"Missing Count": missing, "Missing %": (missing / len(raw_df)) * 100})
        missing_df = missing_df[missing_df["Missing Count"] > 0]
        context['missing_data'] = missing_df.to_html(classes=['table', 'table-striped']) if not missing_df.empty else None
        
        if missing.sum() > 0:
            try:
                fig_miss = px.imshow(raw_df.isnull(), aspect="auto", color_continuous_scale='gray', title="Missing Value Patterns")
                context['missing_heatmap'] = fig_miss.to_html(full_html=False, include_plotlyjs='cdn')
            except Exception as e:
                context['missing_heatmap'] = f"<div class='error-msg'>Could not plot heatmap: {e}</div>"
        else:
            context['missing_heatmap'] = "<p>No missing values detected.</p>"

        # Determine strictly numeric subset from processed dataframe
        X_numeric = processed_df.select_dtypes(include=['number'])

        # EDA Visualizations
        if not X_numeric.empty:
            num_cats = X_numeric.columns.tolist()
            try:
                fig_hist = px.histogram(raw_df, x=num_cats[0], title=f"Distribution of {num_cats[0]}")
                context['eda_hist'] = fig_hist.to_html(full_html=False, include_plotlyjs='cdn')
            except Exception as e:
                context['eda_hist'] = f"<div class='error-msg'>Could not plot histogram: {e}</div>"
        
            if len(num_cats) > 1:
                try:
                    fig_scatter = px.scatter(raw_df, x=num_cats[0], y=num_cats[1], title=f"Scatter: {num_cats[0]} vs {num_cats[1]}")
                    context['eda_scatter'] = fig_scatter.to_html(full_html=False, include_plotlyjs='cdn')
                    
                    # Correlation Heatmap on numeric only
                    corr_df = X_numeric.corr()
                    fig_corr = px.imshow(corr_df, aspect="auto", color_continuous_scale="RdBu_r", title="Correlation Heatmap (Numeric Only)")
                    context['stats_corr'] = fig_corr.to_html(full_html=False, include_plotlyjs='cdn')
                except Exception as e:
                    context['eda_scatter'] = f"<div class='error-msg'>Could not construct scatter or correlation: {e}</div>"

        # PCA Component (Apply ONLY on numeric features)
        df_numeric = raw_df.select_dtypes(include=['number'])
        
        # Handle missing values: fill with mean, drop any entirely-NaN columns and remaining NaNs
        df_numeric = df_numeric.fillna(df_numeric.mean())
        df_numeric = df_numeric.dropna(axis=1, how='all').dropna()
        
        if df_numeric.empty or df_numeric.shape[1] < 2:
            context['pca_err'] = "No numeric features available for PCA. PCA requires at least 2 numeric columns."
        else:
            try:
                # Apply StandardScaler
                pca_scaler = StandardScaler()
                df_numeric_scaled = pca_scaler.fit_transform(df_numeric)
                
                # Apply PCA
                pca = PCA()
                pca_comps = pca.fit_transform(df_numeric_scaled)
                exp_var = pca.explained_variance_ratio_ * 100
                cum_var = np.cumsum(exp_var)
                
                fig_scree = go.Figure()
                fig_scree.add_trace(go.Bar(x=[f"PC{i+1}" for i in range(len(exp_var))], y=exp_var, name="Individual Variance"))
                fig_scree.add_trace(go.Scatter(x=[f"PC{i+1}" for i in range(len(exp_var))], y=cum_var, mode='lines+markers', name="Cumulative Variance"))
                fig_scree.update_layout(title="PCA Scree Plot", yaxis_title="Variance Explained (%)")
                context['pca_scree'] = fig_scree.to_html(full_html=False, include_plotlyjs='cdn')
                
                if pca_comps.shape[1] >= 2:
                    pca_df = pd.DataFrame(pca_comps[:, :2], columns=['PC1', 'PC2'])
                    fig_pca_scatter = px.scatter(pca_df, x='PC1', y='PC2', title="PCA PC1 vs PC2")
                    context['pca_scatter'] = fig_pca_scatter.to_html(full_html=False, include_plotlyjs='cdn')
            except Exception as e:
                context['pca_err'] = f"PCA failed during execution: {str(e)}"

        # LDA Component
        if not lda_target:
            context['lda_err'] = "Target column not provided. You must explicitly select a target column in the upload portal to run LDA."
        elif lda_target not in raw_df.columns:
            context['lda_err'] = f"The provided target column '{lda_target}' was not found in the dataset."
        else:
            y_raw = raw_df[lda_target]
            if y_raw.nunique() < 2:
                context['lda_err'] = "Target column must have at least 2 distinct classes."
            else:
                # Use ONLY numeric features for LDA
                X_lda = processed_df.select_dtypes(include=['number'])
                # Drop target column from X if it accidentally falls into numeric features
                if lda_target in X_lda.columns:
                    X_lda = X_lda.drop(columns=[lda_target])
                
                if X_lda.empty or X_lda.shape[1] == 0:
                    context['lda_err'] = "No numeric feature columns available to predict the target for LDA."
                else:
                    try:
                        # Encode categorical target strictly using LabelEncoder
                        y_encoded = LabelEncoder().fit_transform(y_raw.astype(str))
                        
                        lda = LinearDiscriminantAnalysis()
                        lda_comps = lda.fit_transform(X_lda, y_encoded)
                        
                        if lda_comps.shape[1] == 1:
                            lda_df = pd.DataFrame({'LD1': lda_comps[:, 0], 'Target': y_raw.astype(str)})
                            fig_lda = px.histogram(lda_df, x='LD1', color='Target', title=f"1D LDA (Target: {lda_target})")
                        else:
                            lda_df = pd.DataFrame({'LD1': lda_comps[:, 0], 'LD2': lda_comps[:, 1], 'Target': y_raw.astype(str)})
                            fig_lda = px.scatter(lda_df, x='LD1', y='LD2', color='Target', title=f"2D LDA (Target: {lda_target})")
                        context['lda_plot'] = fig_lda.to_html(full_html=False, include_plotlyjs='cdn')
                    except Exception as e:
                        context['lda_err'] = f"LDA execution failed computationally: {str(e)}"

        # Factor Analysis Component
        X_fa = processed_df.select_dtypes(include=['number']).dropna()
        if X_fa.shape[1] >= 2:
            try:
                n_factors = min(3, X_fa.shape[1])
                fa = FactorAnalyzer(n_factors=n_factors, rotation='varimax')
                fa.fit(X_fa)
                
                loadings_df = pd.DataFrame(fa.loadings_, index=X_fa.columns, columns=[f"Factor {i+1}" for i in range(n_factors)])
                fig_fa = px.imshow(loadings_df, text_auto=".2f", aspect="auto", color_continuous_scale="Viridis", title="Factor Loadings Heatmap")
                context['fa_plot'] = fig_fa.to_html(full_html=False, include_plotlyjs='cdn')
            except Exception as e:
                context['fa_err'] = f"Factor Analysis failed: {str(e)}"
        else:
            context['fa_err'] = "Not enough numeric data for Factor Analysis."

        return render_template('results.html', **context)

    except Exception as e:
        traceback.print_exc()
        flash(f'An error occurred processing the file: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/download')
def download():
    global processed_df_cache
    if processed_df_cache is None:
        return "No data processed", 400
        
    buffer = io.BytesIO()
    processed_df_cache.to_csv(buffer, index=False)
    buffer.seek(0)
    
    return send_file(
        buffer,
        as_attachment=True,
        download_name="processed_dataset.csv",
        mimetype="text/csv"
    )

if __name__ == '__main__':
    app.run(debug=True, port=5000)
