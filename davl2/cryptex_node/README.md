# Cryptex Insight Engine - Project README

## 🚀 Quick Start Guide

Cryptex Insight Engine is a high-fidelity Cryptocurrency/Market Analytics Node featuring a Python analysis backend and a cyberpunk-themed frontend dashboard.

### Project Structure

```
cryptex_node/
├── dataset/
│   └── realistic_food_delivery_dataset_15000.csv
├── backend/
│   ├── server.py              # Flask API server
│   ├── requirements.txt        # Python dependencies
│   └── analytics_cache/        # Generated analysis assets (PNGs + JSON)
├── frontend/
│   ├── index.html             # Main dashboard HTML
│   ├── terminal.css           # Cyberpunk styling
│   └── logic.js               # Interactive frontend logic
├── analysis_node.py           # EDA & analysis engine
└── README.md                  # This file
```

## 📋 Setup Instructions

### 1. **Install Python Dependencies**

Navigate to the backend directory and install requirements:

```bash
cd cryptex_node/backend
pip install -r requirements.txt
```

**Required packages:**
- Flask 2.3.3 - Web framework
- Flask-CORS 4.0.0 - Enable cross-origin requests
- pandas 2.0.3 - Data manipulation
- numpy 1.24.3 - Numerical computing
- scikit-learn 1.3.0 - ML preprocessing
- matplotlib 3.7.2 - Visualization
- seaborn 0.12.2 - Statistical visualization

### 2. **Run the Analysis Engine**

Generate all analytical assets and JSON report:

```bash
cd cryptex_node
python analysis_node.py
```

**Expected Output:**
- 5 PNG visualizations in `backend/analytics_cache/`
- 1 JSON report: `full_report.json`

**Generated Assets:**
1. `01_trend_analysis.png` - Time-series trends and distributions
2. `02_correlation_heatmap.png` - Feature correlations
3. `03_distribution_outliers.png` - Histograms and boxplots
4. `04_pca_analysis.png` - Principal Component Analysis & scree plot
5. `05_kmeans_elbow.png` - K-Means clustering optimization

### 3. **Start the Backend Server**

```bash
cd cryptex_node/backend
python server.py
```

Server will start at: `http://localhost:5000`

### 4. **Access the Dashboard**

Open your browser and navigate to:
```
http://localhost:5000
```

## 📊 API Endpoints

### `GET /api/market-pulse`
Returns real-time market metrics and visualization inventory.

**Response:**
```json
{
  "status": "connected",
  "node_id": "CRYPTEX-NODE-001",
  "market_metrics": {
    "total_orders": 15000,
    "success_rate": 85.2,
    "total_liquidity": 8500000
  },
  "insights": {
    "peak_ordering_hour": 14,
    "fastest_delivery_zone": "Powai",
    "volatility_index": 0.547
  }
}
```

### `GET /api/visuals/<filename>`
Retrieve generated PNG analysis visualizations.

**Valid filenames:**
- `01_trend_analysis.png`
- `02_correlation_heatmap.png`
- `03_distribution_outliers.png`
- `04_pca_analysis.png`
- `05_kmeans_elbow.png`

### `GET /api/full-report`
Retrieve complete analysis report with detailed statistics.

### `GET /api/health`
Health check endpoint.

## 🎨 Frontend Features

### Node Monitor (Header)
- **Real-time metrics:** Total liquidity, order volume, success rate
- **Connection status:** Live indicator with pulse animation
- **Node identification:** Unique node ID and timestamp

### Executive Summary
- **Peak Hour:** Most active ordering time
- **Fastest Zone:** Best delivery zone performance
- **Popular Payment:** Most used payment method
- **Average Items:** Typical items per order
- **Top Vendor:** Most popular restaurant
- **Volatility Index:** Market price volatility metric

### Interleaved Dashboard
Alternates visual analytics with statistical tables:
- **Trend Analysis** + Order Metrics Table
- **Correlation Matrix** + Delivery Metrics Table
- **Distribution Analysis** + Order Status Table
- **PCA Analysis** + Feature Statistics Table
- **K-Means Clustering** + Market Intelligence Table

### Design
- **Theme:** Cyberpunk terminal aesthetic
- **Colors:** Neon green (#39ff14) primary, Cyan (#00d4ff) secondary, Red (#ff003c) alerts
- **Typography:** Space Mono (monospace), Inter (sans-serif)
- **Effects:** Glow, pulse animations, glass-morphism panels

## 🔧 Technical Stack

**Backend:**
- Python 3.x
- Flask (micro web framework)
- Pandas & NumPy (data processing)
- Scikit-learn (ML preprocessing, PCA, K-Means)
- Matplotlib & Seaborn (visualization)

**Frontend:**
- HTML5
- CSS3 (custom properties, animations)
- Vanilla JavaScript (Fetch API)

**Data:**
- CSV dataset with 15,000 food delivery records
- Features: order details, delivery metrics, payment methods, status

## 📈 Analysis Workflow

### 1. Data Preprocessing
- Load CSV and standardize columns
- Handle missing values
- Create numeric encodings for categorical features

### 2. Exploratory Data Analysis (EDA)
- **Trend Analysis:** Multi-variable time-series trends
- **Correlation:** Inter-feature dependencies
- **Distribution:** Statistical distributions and outlier detection
- **PCA:** Dimensionality reduction and variance analysis
- **Clustering:** K-Means with elbow method optimization

### 3. Metrics Generation
- Descriptive statistics (mean, median, std, quartiles)
- Order status distribution
- Delivery performance metrics
- Market volatility indices

### 4. Asset Export
- PNG visualizations (150 DPI, neon color scheme)
- JSON report with full statistics
- Serialization of NumPy types handled

## 🔍 Data Schema

### Input CSV Columns
- `order_id` - Unique order identifier
- `customer_name` - Customer name
- `restaurant_name` - Restaurant name
- `food_item` - Item ordered
- `quantity` - Item quantity
- `order_amount` - Total amount (₹)
- `delivery_zone` - Delivery zone
- `order_hour` - Order time (0-23)
- `delivery_time_minutes` - Delivery duration
- `payment_mode` - Payment method (UPI, Card, Cash)
- `order_status` - Status (Delivered, Delayed, Cancelled)

## 🚨 Troubleshooting

### "Analysis not yet generated" error
**Solution:** Run `python analysis_node.py` first to generate assets.

### Images not loading in dashboard
**Solution:** Check that `analytics_cache/` contains PNG files and Flask server is running.

### Port 5000 already in use
**Solution:** Change Flask port in `server.py` or kill process using port 5000.

### Missing Python packages
**Solution:** Run `pip install -r requirements.txt` again, ensure pip is updated.

## 📝 Analysis Configuration

Edit `analysis_node.py` to customize:

```python
DATASET_PATH = 'dataset/realistic_food_delivery_dataset_15000.csv'
CACHE_DIR = 'backend/analytics_cache'
PLOT_DPI = 150  # Resolution
PLOT_FIGSIZE = (14, 8)  # Visualization size
```

## 🎯 Performance Notes

- Analysis completes in ~10-30 seconds depending on CPU
- Dashboard loads visualizations asynchronously
- JSON report is lightweight (<100KB)
- Auto-refresh can be enabled in `logic.js` (UPDATE_INTERVAL)

## 📄 License & Attribution

Cryptex Insight Engine v1.0
Created for advanced quantitative market analytics and research.

---

**For questions or extensions, refer to the inline code documentation.**
