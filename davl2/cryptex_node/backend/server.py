#!/usr/bin/env python3
"""
Cryptex Insight Engine - Backend Flask Server
Serves the Cyberpunk analytics dashboard and API endpoints
"""

from flask import Flask, jsonify, send_file, send_from_directory
from flask_cors import CORS
import json
import os
from pathlib import Path
import pandas as pd

# Configuration
CACHE_DIR = 'analytics_cache'
DATASET_PATH = 'dataset/realistic_food_delivery_dataset_15000.csv'

# Initialize Flask
app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)

# Load report on startup
REPORT = {}
try:
    with open(f'{CACHE_DIR}/full_report.json', 'r') as f:
        REPORT = json.load(f)
except FileNotFoundError:
    REPORT = {'error': 'Analysis not yet generated. Run analysis_node.py first.'}

def load_live_data():
    """Load live data for real-time metrics"""
    try:
        df = pd.read_csv(DATASET_PATH)
        return df
    except Exception as e:
        return None

@app.route('/')
def index():
    """Serve the main dashboard"""
    return send_from_directory('../frontend', 'index.html')

@app.route('/api/market-pulse')
def market_pulse():
    """
    GET /api/market-pulse
    Service-level stats and JSON summary
    """
    if 'error' in REPORT:
        return jsonify({'status': 'offline', 'message': REPORT['error']}), 503
    
    return jsonify({
        'status': 'connected',
        'node_id': 'CRYPTEX-NODE-001',
        'timestamp': REPORT.get('metadata', {}).get('generated_at'),
        'market_metrics': REPORT.get('market_metrics', {}),
        'insights': REPORT.get('insights', {}),
        'visualizations': [
            '01_trend_analysis.png',
            '02_correlation_heatmap.png',
            '03_distribution_outliers.png',
            '04_pca_analysis.png',
            '05_kmeans_elbow.png'
        ]
    })

@app.route('/api/visuals/<filename>')
def serve_visual(filename):
    """
    GET /api/visuals/<filename>
    Serve generated analysis PNG files
    """
    # Security: Validate filename to prevent path traversal
    allowed_files = [
        '01_trend_analysis.png',
        '02_correlation_heatmap.png',
        '03_distribution_outliers.png',
        '04_pca_analysis.png',
        '05_kmeans_elbow.png'
    ]
    
    if filename not in allowed_files:
        return jsonify({'error': 'File not found'}), 404
    
    try:
        return send_file(
            f'{CACHE_DIR}/{filename}',
            mimetype='image/png',
            as_attachment=False
        )
    except FileNotFoundError:
        return jsonify({'error': 'Visualization not generated yet'}), 404

@app.route('/api/full-report')
def full_report():
    """Get the complete analysis report"""
    if 'error' in REPORT:
        return jsonify(REPORT), 503
    return jsonify(REPORT)

@app.route('/api/health')
def health():
    """Health check endpoint"""
    report_exists = os.path.exists(f'{CACHE_DIR}/full_report.json')
    return jsonify({
        'status': 'healthy' if report_exists else 'degraded',
        'cache_available': report_exists,
        'timestamp': os.path.getmtime(f'{CACHE_DIR}/full_report.json') if report_exists else None
    })

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 CRYPTEX INSIGHT ENGINE - BACKEND SERVER")
    print("="*60)
    print("📡 Starting Flask server...")
    print("🌐 Navigate to: http://localhost:5000")
    print("📊 API Health: http://localhost:5000/api/health")
    print("=" * 60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
