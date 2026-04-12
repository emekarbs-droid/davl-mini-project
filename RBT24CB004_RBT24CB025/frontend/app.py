import streamlit as st
import pandas as pd
import requests
import json
import plotly.io as pio

st.set_page_config(page_title="Sales Data Analyzer", layout="wide")

API_URL = "http://localhost:8000/api/analyze"

st.title("Sales Data Analyzer")

st.sidebar.header("Configuration")
uploaded_file = st.sidebar.file_uploader("Upload Dataset (CSV/Excel)", type=["csv", "xls", "xlsx"])

target_column = None
if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.csv'):
            df_preview = pd.read_csv(uploaded_file)
        else:
            df_preview = pd.read_excel(uploaded_file)
            
        num_columns = df_preview.select_dtypes(include=['number']).columns.tolist()
        
        target_column = st.sidebar.selectbox("Select Target Variable for Regression (Optional)", ["None"] + num_columns)
        if target_column == "None":
            target_column = None
            
        analyze_btn = st.sidebar.button("Run Analysis")
        
        if analyze_btn:
            with st.spinner("Analyzing data..."):
                uploaded_file.seek(0)
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "text/csv")}
                data = {"target_column": target_column} if target_column else {}
                
                try:
                    response = requests.post(API_URL, files=files, data=data)
                    
                    if response.status_code == 200:
                        result = response.json()
                        
                        if "error" in result:
                            st.error(f"Error from API: {result['error']}")
                        else:
                            st.success("Analysis Complete!")
                            
                            st.header("1. Overview")
                            st.dataframe(df_preview.head())
                            st.write("**Missing Values Summary:**")
                            st.write(df_preview.isnull().sum())
                            
                            st.header("2. Data Insights (EDA)")
                            if "correlation_fig" in result["eda"]:
                                st.plotly_chart(pio.from_json(json.dumps(result["eda"]["correlation_fig"])), use_container_width=True)
                                
                            st.subheader("Distributions")
                            cols = st.columns(2)
                            idx = 0
                            for k, v in result["distribution_plots"].items():
                                with cols[idx % 2]:
                                    st.plotly_chart(pio.from_json(json.dumps(v)), use_container_width=True)
                                idx += 1
                                
                            st.header("3. Dimensionality Reduction (PCA)")
                            if result.get("pca") and "error" in result["pca"]:
                                st.error(result["pca"]["error"])
                            elif result.get("pca"):
                                pca_cols = st.columns(2)
                                with pca_cols[0]:
                                    if "explained_variance" in result["pca"]:
                                        st.plotly_chart(pio.from_json(json.dumps(result["pca"]["explained_variance"])), use_container_width=True)
                                with pca_cols[1]:
                                    if "scatter_plot" in result["pca"]:
                                        st.plotly_chart(pio.from_json(json.dumps(result["pca"]["scatter_plot"])), use_container_width=True)
                                        
                            st.header("4. Clustering (K-Means)")
                            if result.get("clustering") and "error" in result["clustering"]:
                                st.error(result["clustering"]["error"])
                            elif result.get("clustering"):
                                st.write(f"**Optimal K determined:** {result['clustering'].get('optimal_k')}")
                                clus_cols = st.columns(2)
                                with clus_cols[0]:
                                    if "elbow_plot" in result["clustering"]:
                                        st.plotly_chart(pio.from_json(json.dumps(result["clustering"]["elbow_plot"])), use_container_width=True)
                                with clus_cols[1]:
                                    if "cluster_plot" in result["clustering"]:
                                        st.plotly_chart(pio.from_json(json.dumps(result["clustering"]["cluster_plot"])), use_container_width=True)
                                        
                            st.header("5. Predictions & Model Diagnostics")
                            if not target_column:
                                st.info("No target variable selected. Regression skipped.")
                            elif result.get("regression"):
                                if "error" in result["regression"]:
                                    st.error(result["regression"]["error"])
                                else:
                                    reg_data = result["regression"]
                                    metrics = reg_data["metrics"]
                                    
                                    metric_cols = st.columns(4)
                                    metric_cols[0].metric("Train RMSE", f"{metrics['train_rmse']:.2f}")
                                    metric_cols[1].metric("Test RMSE", f"{metrics['test_rmse']:.2f}")
                                    metric_cols[2].metric("Train R²", f"{metrics['train_r2']:.2f}")
                                    metric_cols[3].metric("Test R²", f"{metrics['test_r2']:.2f}")
                                    
                                    if metrics["overfitting_warning"]:
                                        st.warning("⚠️ Warning: Model shows signs of overfitting.")
                                    else:
                                        st.success("✅ Model does not show significant overfitting.")
                                        
                                    plot_cols = st.columns(2)
                                    with plot_cols[0]:
                                        if "actual_vs_predicted" in reg_data:
                                            st.plotly_chart(pio.from_json(json.dumps(reg_data["actual_vs_predicted"])), use_container_width=True)
                                    with plot_cols[1]:
                                        if "residual_plot" in reg_data:
                                            st.plotly_chart(pio.from_json(json.dumps(reg_data["residual_plot"])), use_container_width=True)
                except requests.exceptions.ConnectionError:
                    st.error("Failed to connect to API. Please ensure the FastAPI backend is running on http://localhost:8000")
                    
    except Exception as e:
        st.error(f"Error processing file locally: {e}")
else:
    st.info("Please upload a dataset to begin.")
