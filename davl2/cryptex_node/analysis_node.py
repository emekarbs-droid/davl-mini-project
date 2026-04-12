#!/usr/bin/env python3
"""
Cryptex Insight Engine - Analysis Node
Advanced EDA and quantitative research on cryptocurrency/market datasets
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import json
import os
import warnings
from datetime import datetime

warnings.filterwarnings('ignore')

# Configuration
DATASET_PATH = 'dataset/realistic_food_delivery_dataset_15000.csv'
CACHE_DIR = 'backend/analytics_cache'
PLOT_DPI = 150
PLOT_FIGSIZE = (14, 8)

# Ensure cache directory exists
os.makedirs(CACHE_DIR, exist_ok=True)

# Custom JSON encoder for NumPy types
class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (np.integer, np.floating)):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, (pd.Timestamp, datetime)):
            return obj.isoformat()
        return super().default(obj)

def load_data():
    """Load and validate dataset"""
    print("📊 Loading dataset...")
    df = pd.read_csv(DATASET_PATH)
    print(f"✓ Loaded {len(df)} records with {len(df.columns)} columns")
    return df

def preprocess_data(df):
    """Data cleaning and standardization"""
    print("\n🔧 Preprocessing data...")
    
    # Convert order_hour to numeric
    df['order_hour'] = pd.to_numeric(df['order_hour'], errors='coerce')
    df['delivery_time_minutes'] = pd.to_numeric(df['delivery_time_minutes'], errors='coerce')
    df['order_amount'] = pd.to_numeric(df['order_amount'], errors='coerce')
    df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce')
    
    # Fill missing delivery times with median
    df['delivery_time_minutes'].fillna(df['delivery_time_minutes'].median(), inplace=True)
    df['order_hour'].fillna(df['order_hour'].median(), inplace=True)
    
    # Create numeric status encoding
    status_map = {'Delivered': 1, 'Delayed': 0, 'Cancelled': -1}
    df['status_numeric'] = df['order_status'].map(status_map)
    
    # Create numeric payment encoding
    payment_map = {'UPI': 1, 'Card': 2, 'Cash': 0}
    df['payment_numeric'] = df['payment_mode'].map(payment_map)
    
    print(f"✓ Data preprocessed. Missing values: {df.isnull().sum().sum()}")
    return df

def trend_analysis(df):
    """Multi-variable time-series plotting"""
    print("\n📈 Conducting trend analysis...")
    
    fig, axes = plt.subplots(2, 2, figsize=PLOT_FIGSIZE, facecolor='#0a0a0f')
    fig.suptitle('Cryptex Trend Analysis', fontsize=18, color='#39ff14', weight='bold')
    
    # Plot 1: Order Amount Trend
    ax1 = axes[0, 0]
    ax1.scatter(df['order_hour'], df['order_amount'], alpha=0.5, color='#39ff14', s=20)
    ax1.set_xlabel('Order Hour', color='#39ff14')
    ax1.set_ylabel('Order Amount (₹)', color='#39ff14')
    ax1.set_title('Order Amount by Hour', color='#39ff14')
    ax1.set_facecolor('#0a0a0f')
    ax1.tick_params(colors='#39ff14')
    ax1.grid(True, alpha=0.1, color='#39ff14')
    
    # Plot 2: Delivery Time Trend
    ax2 = axes[0, 1]
    hourly_delivery = df.groupby('order_hour')['delivery_time_minutes'].mean()
    ax2.plot(hourly_delivery.index, hourly_delivery.values, color='#ff003c', linewidth=2, marker='o')
    ax2.fill_between(hourly_delivery.index, hourly_delivery.values, alpha=0.3, color='#ff003c')
    ax2.set_xlabel('Order Hour', color='#ff003c')
    ax2.set_ylabel('Avg Delivery Time (min)', color='#ff003c')
    ax2.set_title('Delivery Time Trend', color='#ff003c')
    ax2.set_facecolor('#0a0a0f')
    ax2.tick_params(colors='#ff003c')
    ax2.grid(True, alpha=0.1, color='#ff003c')
    
    # Plot 3: Status Distribution
    ax3 = axes[1, 0]
    status_counts = df['order_status'].value_counts()
    colors_status = ['#39ff14', '#ff003c', '#ffab00']
    ax3.bar(status_counts.index, status_counts.values, color=colors_status, edgecolor='white', linewidth=1.5)
    ax3.set_ylabel('Count', color='#39ff14')
    ax3.set_title('Order Status Distribution', color='#39ff14')
    ax3.set_facecolor('#0a0a0f')
    ax3.tick_params(colors='#39ff14')
    for i, v in enumerate(status_counts.values):
        ax3.text(i, v + 10, str(v), ha='center', color='#39ff14', weight='bold')
    
    # Plot 4: Quantity vs Amount
    ax4 = axes[1, 1]
    ax4.scatter(df['quantity'], df['order_amount'], alpha=0.6, color='#00d4ff', s=25)
    ax4.set_xlabel('Quantity', color='#00d4ff')
    ax4.set_ylabel('Order Amount (₹)', color='#00d4ff')
    ax4.set_title('Quantity vs Order Amount', color='#00d4ff')
    ax4.set_facecolor('#0a0a0f')
    ax4.tick_params(colors='#00d4ff')
    ax4.grid(True, alpha=0.1, color='#00d4ff')
    
    plt.tight_layout()
    plt.savefig(f'{CACHE_DIR}/01_trend_analysis.png', dpi=PLOT_DPI, facecolor='#0a0a0f', edgecolor='#39ff14')
    plt.close()
    print("✓ Trend analysis saved: 01_trend_analysis.png")

def correlation_heatmap(df):
    """Correlation analysis of numerical columns"""
    print("🔗 Computing correlation heatmap...")
    
    numeric_cols = df[['order_amount', 'quantity', 'delivery_time_minutes', 'order_hour', 'status_numeric', 'payment_numeric']].copy()
    
    corr_matrix = numeric_cols.corr()
    
    fig, ax = plt.subplots(figsize=(10, 8), facecolor='#0a0a0f')
    sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='RdYlGn', center=0,
                cbar_kws={'label': 'Correlation'}, ax=ax, 
                linewidths=0.5, linecolor='#39ff14',
                annot_kws={'color': '#0a0a0f', 'weight': 'bold'})
    ax.set_facecolor('#0a0a0f')
    ax.set_title('Feature Correlation Matrix', fontsize=16, color='#39ff14', weight='bold', pad=20)
    plt.setp(ax.get_xticklabels(), rotation=45, ha='right', color='#39ff14')
    plt.setp(ax.get_yticklabels(), color='#39ff14')
    
    plt.tight_layout()
    plt.savefig(f'{CACHE_DIR}/02_correlation_heatmap.png', dpi=PLOT_DPI, facecolor='#0a0a0f')
    plt.close()
    print("✓ Correlation heatmap saved: 02_correlation_heatmap.png")

def distribution_outliers(df):
    """Histogram and boxplot analysis"""
    print("📊 Analyzing distributions and outliers...")
    
    fig, axes = plt.subplots(2, 2, figsize=PLOT_FIGSIZE, facecolor='#0a0a0f')
    fig.suptitle('Distribution & Outlier Analysis', fontsize=18, color='#39ff14', weight='bold')
    
    # Order Amount Distribution
    ax1 = axes[0, 0]
    ax1.hist(df['order_amount'], bins=50, color='#39ff14', edgecolor='white', alpha=0.7)
    ax1.axvline(df['order_amount'].mean(), color='#ff003c', linestyle='--', linewidth=2, label='Mean')
    ax1.set_xlabel('Order Amount (₹)', color='#39ff14')
    ax1.set_ylabel('Frequency', color='#39ff14')
    ax1.set_title('Order Amount Distribution', color='#39ff14')
    ax1.set_facecolor('#0a0a0f')
    ax1.tick_params(colors='#39ff14')
    ax1.legend(facecolor='#0a0a0f', edgecolor='#39ff14', labelcolor='#39ff14')
    ax1.grid(True, alpha=0.1, color='#39ff14', axis='y')
    
    # Order Amount Boxplot
    ax2 = axes[0, 1]
    bp = ax2.boxplot(df['order_amount'], vert=True, patch_artist=True)
    for patch in bp['boxes']:
        patch.set_facecolor('#39ff14')
        patch.set_alpha(0.7)
    for whisker in bp['whiskers']:
        whisker.set_color('#39ff14')
    for median in bp['medians']:
        median.set_color('#ff003c')
        median.set_linewidth(2)
    ax2.set_ylabel('Order Amount (₹)', color='#39ff14')
    ax2.set_title('Order Amount Outliers', color='#39ff14')
    ax2.set_facecolor('#0a0a0f')
    ax2.tick_params(colors='#39ff14')
    ax2.grid(True, alpha=0.1, color='#39ff14', axis='y')
    
    # Delivery Time Distribution
    ax3 = axes[1, 0]
    ax3.hist(df['delivery_time_minutes'], bins=50, color='#00d4ff', edgecolor='white', alpha=0.7)
    ax3.axvline(df['delivery_time_minutes'].mean(), color='#ff003c', linestyle='--', linewidth=2, label='Mean')
    ax3.set_xlabel('Delivery Time (minutes)', color='#00d4ff')
    ax3.set_ylabel('Frequency', color='#00d4ff')
    ax3.set_title('Delivery Time Distribution', color='#00d4ff')
    ax3.set_facecolor('#0a0a0f')
    ax3.tick_params(colors='#00d4ff')
    ax3.legend(facecolor='#0a0a0f', edgecolor='#00d4ff', labelcolor='#00d4ff')
    ax3.grid(True, alpha=0.1, color='#00d4ff', axis='y')
    
    # Delivery Time Boxplot
    ax4 = axes[1, 1]
    bp2 = ax4.boxplot(df['delivery_time_minutes'], vert=True, patch_artist=True)
    for patch in bp2['boxes']:
        patch.set_facecolor('#00d4ff')
        patch.set_alpha(0.7)
    for whisker in bp2['whiskers']:
        whisker.set_color('#00d4ff')
    for median in bp2['medians']:
        median.set_color('#ff003c')
        median.set_linewidth(2)
    ax4.set_ylabel('Delivery Time (minutes)', color='#00d4ff')
    ax4.set_title('Delivery Time Outliers', color='#00d4ff')
    ax4.set_facecolor('#0a0a0f')
    ax4.tick_params(colors='#00d4ff')
    ax4.grid(True, alpha=0.1, color='#00d4ff', axis='y')
    
    plt.tight_layout()
    plt.savefig(f'{CACHE_DIR}/03_distribution_outliers.png', dpi=PLOT_DPI, facecolor='#0a0a0f')
    plt.close()
    print("✓ Distribution analysis saved: 03_distribution_outliers.png")

def pca_analysis(df):
    """PCA and scree plot"""
    print("🔬 Performing PCA analysis...")
    
    # Feature selection and scaling
    features = df[['order_amount', 'quantity', 'delivery_time_minutes', 'order_hour']].copy()
    
    # Drop rows with NaN values for PCA
    features = features.dropna()
    
    if len(features) == 0:
        print("⚠ No valid data for PCA analysis")
        return
    
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features)
    
    # PCA
    pca = PCA()
    pca.fit(features_scaled)
    
    # Scree plot
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=PLOT_FIGSIZE, facecolor='#0a0a0f')
    fig.suptitle('PCA Analysis & Variance Explained', fontsize=18, color='#39ff14', weight='bold')
    
    # Scree plot
    cumvar = np.cumsum(pca.explained_variance_ratio_)
    ax1.plot(range(1, len(pca.explained_variance_ratio_) + 1), pca.explained_variance_ratio_, 
             marker='o', color='#39ff14', linewidth=2, markersize=8)
    ax1.fill_between(range(1, len(pca.explained_variance_ratio_) + 1), 
                      pca.explained_variance_ratio_, alpha=0.3, color='#39ff14')
    ax1.set_xlabel('Principal Component', color='#39ff14')
    ax1.set_ylabel('Explained Variance Ratio', color='#39ff14')
    ax1.set_title('Scree Plot', color='#39ff14')
    ax1.set_facecolor('#0a0a0f')
    ax1.tick_params(colors='#39ff14')
    ax1.grid(True, alpha=0.1, color='#39ff14')
    
    # Cumulative variance
    ax2.plot(range(1, len(cumvar) + 1), cumvar, marker='s', color='#00d4ff', linewidth=2, markersize=8)
    ax2.axhline(y=0.95, color='#ff003c', linestyle='--', linewidth=2, label='95% Variance')
    ax2.fill_between(range(1, len(cumvar) + 1), cumvar, alpha=0.3, color='#00d4ff')
    ax2.set_xlabel('Principal Component', color='#00d4ff')
    ax2.set_ylabel('Cumulative Explained Variance', color='#00d4ff')
    ax2.set_title('Cumulative Variance Explained', color='#00d4ff')
    ax2.set_facecolor('#0a0a0f')
    ax2.tick_params(colors='#00d4ff')
    ax2.legend(facecolor='#0a0a0f', edgecolor='#00d4ff', labelcolor='#00d4ff')
    ax2.grid(True, alpha=0.1, color='#00d4ff')
    
    plt.tight_layout()
    plt.savefig(f'{CACHE_DIR}/04_pca_analysis.png', dpi=PLOT_DPI, facecolor='#0a0a0f')
    plt.close()
    print("✓ PCA analysis saved: 04_pca_analysis.png")

def kmeans_clustering(df):
    """K-Means clustering and elbow plot"""
    print("🎯 Performing K-Means clustering...")
    
    features = df[['order_amount', 'quantity', 'delivery_time_minutes', 'order_hour']].copy()
    
    # Drop rows with NaN values for K-Means
    features = features.dropna()
    
    if len(features) == 0:
        print("⚠ No valid data for K-Means analysis")
        return
    
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features)
    
    # Elbow method
    inertias = []
    silhouettes = []
    K_range = range(1, 11)
    
    for k in K_range:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        kmeans.fit(features_scaled)
        inertias.append(kmeans.inertia_)
    
    # Elbow plot
    fig, ax = plt.subplots(figsize=(12, 6), facecolor='#0a0a0f')
    ax.plot(K_range, inertias, marker='o', color='#39ff14', linewidth=2.5, markersize=10)
    ax.axvline(x=3, color='#ff003c', linestyle='--', linewidth=2, alpha=0.7, label='Optimal K=3')
    ax.fill_between(K_range, inertias, alpha=0.2, color='#39ff14')
    ax.set_xlabel('Number of Clusters (k)', color='#39ff14', fontsize=12)
    ax.set_ylabel('Inertia (Within-cluster sum of squares)', color='#39ff14', fontsize=12)
    ax.set_title('K-Means Elbow Plot', fontsize=16, color='#39ff14', weight='bold')
    ax.set_facecolor('#0a0a0f')
    ax.tick_params(colors='#39ff14')
    ax.grid(True, alpha=0.1, color='#39ff14')
    ax.legend(facecolor='#0a0a0f', edgecolor='#39ff14', labelcolor='#39ff14', fontsize=11)
    
    plt.tight_layout()
    plt.savefig(f'{CACHE_DIR}/05_kmeans_elbow.png', dpi=PLOT_DPI, facecolor='#0a0a0f')
    plt.close()
    print("✓ K-Means analysis saved: 05_kmeans_elbow.png")

def json_export(df):
    """Export full report as JSON"""
    print("💾 Exporting JSON report...")
    
    numeric_cols = df.select_dtypes(include=[np.number])
    
    report = {
        'metadata': {
            'total_records': len(df),
            'total_columns': len(df.columns),
            'generated_at': datetime.now().isoformat(),
            'columns': list(df.columns)
        },
        'market_metrics': {
            'total_orders': int(len(df)),
            'successful_deliveries': int((df['order_status'] == 'Delivered').sum()),
            'delayed_orders': int((df['order_status'] == 'Delayed').sum()),
            'cancelled_orders': int((df['order_status'] == 'Cancelled').sum()),
            'success_rate': float(((df['order_status'] == 'Delivered').sum() / len(df)) * 100),
            'total_liquidity': float(df['order_amount'].sum()),
            'avg_transaction_size': float(df['order_amount'].mean()),
            'stats': {
                'order_amount': {
                    'mean': float(df['order_amount'].mean()),
                    'median': float(df['order_amount'].median()),
                    'std': float(df['order_amount'].std()),
                    'min': float(df['order_amount'].min()),
                    'max': float(df['order_amount'].max()),
                    'q25': float(df['order_amount'].quantile(0.25)),
                    'q75': float(df['order_amount'].quantile(0.75))
                },
                'delivery_time': {
                    'mean': float(df['delivery_time_minutes'].mean()),
                    'median': float(df['delivery_time_minutes'].median()),
                    'std': float(df['delivery_time_minutes'].std()),
                    'min': float(df['delivery_time_minutes'].min()),
                    'max': float(df['delivery_time_minutes'].max())
                },
                'order_hour': {
                    'mean': float(df['order_hour'].mean()),
                    'median': float(df['order_hour'].median()),
                    'std': float(df['order_hour'].std())
                },
                'quantity': {
                    'mean': float(df['quantity'].mean()),
                    'median': float(df['quantity'].median()),
                    'std': float(df['quantity'].std())
                },
                'order_status': df['order_status'].value_counts().to_dict()
            }
        },
        'insights': {
            'peak_ordering_hour': int(df.groupby('order_hour')['order_amount'].sum().idxmax()),
            'fastest_delivery_zone': df.groupby('delivery_zone')['delivery_time_minutes'].mean().idxmin(),
            'most_popular_payment': df['payment_mode'].value_counts().index[0],
            'avg_items_per_order': float(df['quantity'].mean()),
            'top_restaurant': df['restaurant_name'].value_counts().index[0],
            'volatility_index': float(df['order_amount'].std() / df['order_amount'].mean())
        }
    }
    
    with open(f'{CACHE_DIR}/full_report.json', 'w') as f:
        json.dump(report, f, indent=2, cls=NumpyEncoder)
    
    print("✓ JSON report saved: full_report.json")
    return report

def main():
    """Execute complete analysis pipeline"""
    print("\n" + "="*60)
    print("🚀 CRYPTEX INSIGHT ENGINE - ANALYSIS NODE")
    print("="*60)
    
    try:
        # Load and preprocess
        df = load_data()
        df = preprocess_data(df)
        
        # Perform analyses
        trend_analysis(df)
        correlation_heatmap(df)
        distribution_outliers(df)
        pca_analysis(df)
        kmeans_clustering(df)
        report = json_export(df)
        
        print("\n" + "="*60)
        print("✅ ANALYSIS COMPLETE")
        print("="*60)
        print(f"📊 Generated 5 visualization assets")
        print(f"📈 Total Records Analyzed: {report['metadata']['total_records']:,}")
        print(f"💰 Total Liquidity: ₹{report['market_metrics']['total_liquidity']:,.2f}")
        print(f"✓ Success Rate: {report['market_metrics']['success_rate']:.2f}%")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
