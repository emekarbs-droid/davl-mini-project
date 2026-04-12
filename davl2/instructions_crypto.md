# Cryptex Insight Engine: Project Instructions

## Project Overview
Your objective is to build a high-fidelity **Cryptocurrency Analytics Node** that provides deep quantitative research into global crypto markets. This project requires a Python-driven analysis backend and a glassmorphism-based "Cyberpunk" frontend.

## 1. Technical Stack (Non-Negotiable)
- **Backend:** Flask (Python)
- **Frontend:** Vanilla HTML5, CSS3 (Custom Variables), and Javascript (Fetch API)
- **Data Science:** Pandas, NumPy, Scikit-learn, Matplotlib/Seaborn
- **Styling:** Neo-Cyberpunk aesthetics (Neon accents, deep blacks, high-contrast monitors)

## 2. Dataset Requirements
- **Source:** `dataset/{YOUR_DATASET_NAME}.csv`
- **Required Columns:** Standardize your CSV to include: `Label`, `Main_Value`, `Secondary_Value`, `Timestamp`, and at least 4 categorical or numerical indicators.

## 3. Analysis Core (`analysis_node.py`)
The script must perform advanced EDA and output assets to `backend/analytics_cache/`:
1. **Trend Analysis:** Multi-variable time-series plotting.
2. **Correlation Heatmap:** Mapping inter-dependencies between provided indicators.
3. **Distribution & Outliers:** Histogram and boxplot analysis of primary values.
4. **Machine Learning Pre-processing:** PCA (Scree Plot) and K-Means Clustering (Elbow Plot) to identify data regimes.
5. **JSON Export:** A `full_report.json` containing `stats` (describe), `info` (metadata), and `insights` (narrative summary).

## 4. Interleaved Dashboard Layout
The frontend must interleave visual assets with quantitative tables:
- **Insight Clusters:** Every graph must be paired with its corresponding statistical metadata (e.g., Plot 1 next to the `Describe` table).
- **Executive Summary:** A top-level HUD showing 4-6 key metrics extracted from the latest data record.

## 5. Backend API (`backend/server.py`)
The API must feature:
- `GET /api/market-pulse`: Service-level stats and JSON summary.
- `GET /api/visuals/<filename>`: Serve generated analysis PNGs.
- `GET /`: Serve the Cryptex UI.

## 6. Website Aesthetics & UI
The design must follow a **Cyberpunk Terminal** style:
- **Fonts:** 'Inter' for UI, 'Space Mono' or 'Fira Code' for data fields.
- **Color Palette:**
  - Background: `#0a0a0f`
  - Neon Accent: `#39ff14` (Classic Terminal Green)
  - Alert Accent: `#ff003c` (Cyber Red)
- **Layout:**
  - **Node Monitor:** A top bar showing "Connected" status and total market liquidity.
  - **Interleaved Grid:** Alternate between visual maps (plots) and raw JSON-formatted table nodes.
  - **Asset Switcher:** Ability to toggle between major themes.

## 7. Project Structure
```text
cryptex_node/
├── dataset/
│   └── {YOUR_DATASET_NAME}.csv
├── backend/
│   ├── server.py
│   ├── requirements.txt
│   └── analytics_cache/ # Generated PNGs and JSON
├── frontend/ (Served by backend)
│   ├── index.html
│   ├── terminal.css
│   └── logic.js
└── analysis_node.py # The training/EDA script
```

## 8. Submission Rules
- All code must be clean and modular.
- The `analysis_node.py` script must handle NumPy serialization errors (use custom encoders).
- The frontend must be responsive and "Wow" the user with glow effects and pulse animations.
