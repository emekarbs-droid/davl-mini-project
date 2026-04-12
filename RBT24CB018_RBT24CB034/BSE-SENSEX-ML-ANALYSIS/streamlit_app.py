import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import io
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

# Page Configuration for Premium Feel
st.set_page_config(page_title="SENSEX ML Analysis", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for aesthetics
st.markdown("""
<style>
    .main {
        background-color: #0e1117;
    }
    .stApp {
        background: linear-gradient(135deg, #09090e, #1a153a, #11111a);
    }
    h1 {
        text-align: center;
        background: linear-gradient(90deg, #00ffcc, #ff007f);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 3.5rem !important;
        margin-bottom: 2rem !important;
    }
    .stmetric {
        background: rgba(255, 255, 255, 0.05);
        padding: 10px;
        border-radius: 10px;
        border: 1px solid rgba(0, 255, 204, 0.2);
    }
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown('<h1>BSE SENSEX<br><span style="color:white; font-size: 0.6em; font-weight: 300;">Machine Learning Analysis</span></h1>', unsafe_allow_html=True)

# --- DATA PIPELINE ---
@st.cache_data
def load_data():
    df_raw = pd.read_csv("BSE SENSEX.csv")
    df_clean = df_raw.copy()
    df_clean.ffill(inplace=True)
    df_clean['Date'] = pd.to_datetime(df_clean['Date'])
    df_clean.sort_values('Date', inplace=True)
    df_clean['Daily_Return'] = df_clean['Close'].pct_change() * 100
    return df_raw, df_clean

try:
    df_original, df = load_data()
except Exception as e:
    st.error("Please ensure 'BSE SENSEX.csv' is in the same directory.")
    st.stop()

# --- SIDEBAR & NAVIGATION ---
st.sidebar.title("ML Navigation")
st.sidebar.markdown("Navigate through the 6 ML objectives of the SENSEX system.")
selection = st.sidebar.radio("Go to:", [
    "Dashboard Overview", 
    "1. Data Loading & Understanding",
    "2. Preprocessing & Cleaning",
    "3. Exploratory Data Analysis",
    "4. Feature Relationships",
    "5. Dimensionality Reduction (PCA)",
    "6. Prediction Model (Linear Regression)"
])

# --- DASHBOARD OVERVIEW ---
if selection == "Dashboard Overview":
    st.header("📈 Dataset Overview")
    
    st.markdown("### Initial Data Structures")
    tab1, tab2, tab3, tab4 = st.tabs(["Head", "Tail", "Description", "Info"])
    
    with tab1:
        st.dataframe(df_original.head(10), use_container_width=True)
    with tab2:
        st.dataframe(df_original.tail(10), use_container_width=True)
    with tab3:
        st.write(df.describe())
    with tab4:
        buffer = io.StringIO()
        df.info(buf=buffer)
        st.text(buffer.getvalue())

    st.info("Scroll down or use the sidebar to explore specific ML Objectives.")

# --- OBJECTIVE 1 ---
elif selection == "1. Data Loading & Understanding":
    st.header("Objective 1: Data Loading & Understanding")
    st.markdown("**ML Operation:** Data Loading, Data Understanding")
    st.write("The system consumes the BSE SENSEX historical data, identifying dimensions and primitive types.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Data Head")
        st.table(df_original.head(5))
    with col2:
        st.subheader("Dataset Parameters")
        st.write(f"**Total Records:** {df.shape[0]}")
        st.write(f"**Total Features:** {df.shape[1]}")

# --- OBJECTIVE 2 ---
elif selection == "2. Preprocessing & Cleaning":
    st.header("Objective 2: Preprocessing & Cleaning")
    st.markdown("**ML Operation:** Handling Missing Values, Data Transformation")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Original Missing Values")
        st.write(df_original.isnull().sum())
    with col2:
        st.subheader("Post-Cleaning (Forward Fill)")
        st.write(df.isnull().sum())
    
    st.success("Successfully converted Date column to Datetime and performed chronological sorting.")

# --- OBJECTIVE 3 ---
elif selection == "3. Exploratory Data Analysis":
    st.header("Objective 3: Exploratory Data Analysis (EDA)")
    st.markdown("**ML Operation:** EDA, Statistical Analysis, Data Visualization")
    
    st.subheader("SENSEX Closing Price Trend")
    fig1, ax1 = plt.subplots(figsize=(12, 5))
    ax1.plot(df['Date'], df['Close'], color='#00ffcc')
    ax1.set_title("Close Price History")
    st.pyplot(fig1)
    
    st.subheader("Daily Returns (%) Distribution")
    fig2, ax2 = plt.subplots(figsize=(10, 4))
    sns.histplot(df['Daily_Return'].dropna(), bins=50, kde=True, color='#ff007f', ax=ax2)
    st.pyplot(fig2)

# --- OBJECTIVE 4 ---
elif selection == "4. Feature Relationships":
    st.header("Objective 4: Identify Relationships Between Features")
    st.markdown("**ML Operation:** Correlation Analysis, Scatter plots")
    
    st.subheader("Heatmap of Correlations")
    numeric_cols = ['Open', 'High', 'Low', 'Close', 'Daily_Return']
    fig3, ax3 = plt.subplots(figsize=(8, 6))
    sns.heatmap(df[numeric_cols].corr(), annot=True, cmap='coolwarm', ax=ax3)
    st.pyplot(fig3)
    
    st.subheader("Pairplot Visualization")
    sample_df = df[['Open', 'High', 'Low', 'Close']].dropna().sample(n=min(300, len(df)), random_state=42)
    fig4 = sns.pairplot(sample_df, diag_kind="kde", corner=True)
    st.pyplot(fig4)

# --- OBJECTIVE 5 ---
elif selection == "5. Dimensionality Reduction (PCA)":
    st.header("Objective 5: Dimensionality Reduction")
    st.markdown("**ML Operation:** PCA (Principal Component Analysis)")
    
    features = ['Open', 'High', 'Low']
    X_pca_input = df[features].dropna()
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_pca_input)
    pca = PCA(n_components=2)
    principal_components = pca.fit_transform(X_scaled)
    
    st.write(f"**Explained Variance PC1:** {pca.explained_variance_ratio_[0]*100:.2f}%")
    st.write(f"**Explained Variance PC2:** {pca.explained_variance_ratio_[1]*100:.2f}%")
    
    fig5, ax5 = plt.subplots(figsize=(8, 6))
    ax5.scatter(principal_components[:, 0], principal_components[:, 1], alpha=0.5, c='#00ffcc')
    ax5.set_xlabel("PC1")
    ax5.set_ylabel("PC2")
    st.pyplot(fig5)

# --- OBJECTIVE 6 ---
elif selection == "6. Prediction Model (Linear Regression)":
    st.header("Objective 6: Prediction Model")
    st.markdown("**ML Operation:** Supervised Learning, Linear Regression")
    
    df_model = df.dropna().copy()
    X = df_model[['Open', 'High', 'Low']]
    y = df_model['Close']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, shuffle=False)
    
    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    
    m1, m2, m3 = st.columns(3)
    m1.metric("RMSE", f"{np.sqrt(mean_squared_error(y_test, y_pred)):.2f}")
    m2.metric("MAE", f"{mean_absolute_error(y_test, y_pred):.2f}")
    m3.metric("R2 Score", f"{r2_score(y_test, y_pred):.4f}")
    
    st.subheader("Actual vs Predicted Closing Price")
    fig6, ax6 = plt.subplots(figsize=(14, 6))
    test_dates = df_model.loc[X_test.index, 'Date']
    ax6.plot(test_dates, y_test, label='Actual', alpha=0.8)
    ax6.plot(test_dates, y_pred, label='Predicted', linestyle='--', alpha=0.8)
    ax6.legend()
    st.pyplot(fig6)
