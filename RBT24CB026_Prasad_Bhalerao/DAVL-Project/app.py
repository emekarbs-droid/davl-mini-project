import warnings

import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

from modules.clustering import compute_elbow, fit_kmeans, prepare_cluster_matrix
from modules.data_loader import load_datasets
from modules.features import build_model_frame
from modules.pca import project_to_2d
from modules.preprocess import preprocess_structured, preprocess_transactions
from modules.regression import run_regression, run_saver_classification
from modules.transactions import category_spending, monthly_spending
from utils.plots import (
    actual_vs_predicted,
    category_spending_figure,
    correlation_heatmap,
    confusion_matrix_figure,
    saver_scatter_figure,
    elbow_figure,
    income_expense_scatter,
    income_histogram,
    monthly_spending_figure,
    pca_cluster_figure,
)

warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="Financial Behavior Modeling Studio",
    page_icon="📊",
    layout="wide",
)

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

:root {
  --background: #121212;
  --surface: #1e1e1e;
  --text-primary: #e0e0e0;
  --text-secondary: #a0a0a0;
  --border: #333333;
  --accent: #3b82f6;
}

html, body, [class*="css"] {
  font-family: 'Inter', sans-serif;
  color: var(--text-primary) !important;
  background-color: var(--background) !important;
}

.stApp {
  background: var(--background);
}

h1, h2, h3, h4, h5, h6 {
  color: var(--text-primary) !important;
  font-weight: 600;
}

.hero {
  background-color: var(--surface);
  border: 1px solid var(--border);
  border-radius: 8px;
  color: var(--text-primary);
  padding: 1.5rem;
  margin-bottom: 1.5rem;
}

.block-card {
  background-color: var(--surface);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 1rem;
  color: var(--text-primary);
}

.stTabs [data-baseweb="tab-list"] {
  gap: 20px;
  background-color: transparent;
}

.stTabs [data-baseweb="tab"] {
  background-color: transparent !important;
  border: none !important;
  border-bottom: 2px solid transparent !important;
  padding: 10px 4px !important;
  color: var(--text-secondary) !important;
}

.stTabs [aria-selected="true"] {
  color: var(--accent) !important;
  border-bottom: 2px solid var(--accent) !important;
}

[data-testid="stSidebar"] {
  background-color: var(--surface) !important;
  border-right: 1px solid var(--border);
}

[data-testid="stSidebar"] * {
  color: var(--text-primary) !important;
}

div[data-testid="stMetricValue"] {
  color: var(--text-primary) !important;
  font-weight: 600;
}

div[data-testid="stMetricLabel"] {
  color: var(--text-secondary) !important;
}

/* Adjust dataframe and table styles for dark mode */
[data-testid="stDataFrame"] {
  background-color: var(--surface);
}
</style>
    """,
    unsafe_allow_html=True,
)


def filter_structured(df: pd.DataFrame) -> pd.DataFrame:
    """
    Applies sidebar filtering rules to the master DataFrame based on user selections 
    for Age, Income, Occupation, and City Tier.
    """
    filtered = df.copy()

    st.sidebar.markdown("## Control Panel")
    st.sidebar.caption("Filter the structured modeling dataset")

    if "age" in filtered.columns:
        age_min, age_max = int(filtered["age"].min()), int(filtered["age"].max())
        age_range = st.sidebar.slider("Age range", age_min, age_max, (age_min, age_max))
        filtered = filtered[(filtered["age"] >= age_range[0]) & (filtered["age"] <= age_range[1])]

    if "income" in filtered.columns:
        inc_min, inc_max = float(filtered["income"].min()), float(filtered["income"].max())
        income_range = st.sidebar.slider(
            "Income range",
            min_value=float(np.floor(inc_min)),
            max_value=float(np.ceil(inc_max)),
            value=(float(np.floor(inc_min)), float(np.ceil(inc_max))),
        )
        filtered = filtered[(filtered["income"] >= income_range[0]) & (filtered["income"] <= income_range[1])]

    if "occupation" in filtered.columns:
        occupations = ["All"] + sorted(filtered["occupation"].dropna().unique().tolist())
        selected_occupation = st.sidebar.selectbox("Occupation", occupations)
        if selected_occupation != "All":
            filtered = filtered[filtered["occupation"] == selected_occupation]

    if "city_tier" in filtered.columns:
        tier_options = sorted(filtered["city_tier"].dropna().unique().tolist())
        selected_tiers = st.sidebar.multiselect("City tier", tier_options, default=tier_options)
        if selected_tiers:
            filtered = filtered[filtered["city_tier"].isin(selected_tiers)]

    return filtered


def render_hero(filtered_structured: pd.DataFrame, cleaned_transactions: pd.DataFrame) -> None:
    st.markdown(
        """
<div class='hero'>
  <h2 style='margin:0;'>Data-Driven Financial Behavior Modeling and Prediction System</h2>
  <p style='margin-top:0.3rem;'>Interactive analysis across one structured modeling dataset and one messy transaction dataset.</p>
</div>
""",
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Structured Records", f"{len(filtered_structured):,}", help="Total number of users in the structured dataset based on current filters.")
    col2.metric("Transaction Records", f"{len(cleaned_transactions):,}", help="Total number of valid, cleaned transaction records available.")
    col3.metric("Avg Income", f"{filtered_structured['income'].mean():,.0f}" if len(filtered_structured) else "N/A", help="Average monthly income of the filtered users.")
    col4.metric(
        "Avg Savings",
        f"{filtered_structured['desired_savings'].mean():,.0f}" if len(filtered_structured) else "N/A",
        help="Average intended savings amount of the filtered users."
    )


def main() -> None:
    """
    Main entry point for the Streamlit dashboard app. 
    It orchestrates the data loading, caching, filtering, and tab rendering.
    """
    st.title("Financial Behavior Intelligence Dashboard")

    try:
        raw_transactions, raw_structured = load_datasets()
    except Exception as exc:
        st.error(f"Data loading failed: {exc}")
        st.stop()

    cleaned_transactions, cleaning_summary = preprocess_transactions(raw_transactions)
    structured, expense_cols = preprocess_structured(raw_structured)
    filtered_structured = filter_structured(structured)

    render_hero(filtered_structured, cleaned_transactions)

    tabs = st.tabs(
        [
            "Financial Overview",
            "Statistical Analysis",
            "Predictive Models",
            "Clustering + PCA",
            "Transaction Trends",
            "Data Quality",
        ]
    )

    with tabs[0]:
        st.subheader("Financial Overview")
        st.markdown("🎯 **Goal:** Grasp the high-level distribution of financial wealth inside the dataset.")
        if filtered_structured.empty:
            st.warning("No records after filtering. Adjust sidebar filters.")
        else:
            left, right = st.columns(2)
            with left:
                st.info("💡 **Income Distribution:** This histogram shows how many people fall into each income bracket, highlighting the most common salary ranges.")
                st.pyplot(income_histogram(filtered_structured))
            with right:
                st.info("💡 **Income vs Target:** This scatter plot maps out if making more money actually equates to higher expenses or savings in real life.")
                st.pyplot(income_expense_scatter(filtered_structured))

    with tabs[1]:
        st.subheader("Statistical Analysis")
        st.markdown("🎯 **Goal:** Understand numerical averages, spreads, and the correlations (how strongly two things relate) between financial variables.")
        if filtered_structured.empty:
            st.warning("No data available for this view.")
        else:
            numeric_df = filtered_structured.select_dtypes(include=[np.number])
            if numeric_df.empty:
                st.warning("No numeric columns found.")
            else:
                summary = numeric_df.describe().T[["mean", "50%", "std", "min", "max"]].rename(columns={"50%": "median"})
                st.dataframe(summary.style.format("{:.2f}"), width="stretch")
                st.pyplot(correlation_heatmap(numeric_df))

                x_option = st.selectbox("Scatter X axis", numeric_df.columns.tolist(), index=0)
                y_default = 1 if len(numeric_df.columns) > 1 else 0
                y_option = st.selectbox("Scatter Y axis", numeric_df.columns.tolist(), index=y_default)

                fig, ax = plt.subplots(figsize=(8, 4.8))
                ax.scatter(numeric_df[x_option], numeric_df[y_option], alpha=0.3, color="#0f766e")
                ax.set_title(f"{x_option} vs {y_option}")
                ax.set_xlabel(x_option)
                ax.set_ylabel(y_option)
                ax.grid(alpha=0.2)
                st.pyplot(fig)

    with tabs[2]:
        st.subheader("Predictive Models: Regression & Classification")
        st.markdown("We predict exactly **how much a user should save** based on their income and expenses, and classify them into a **Saver Profile**.", unsafe_allow_html=True)
        
        if filtered_structured.empty:
            st.warning("No rows available for modeling.")
        elif not {"income", "total_expense", "desired_savings", "savings_ratio"}.issubset(filtered_structured.columns):
            st.error("Required fields for modeling are missing.")
        else:
            model_frame = build_model_frame(filtered_structured, expense_cols)
            if st.button("Run Regression", width="stretch"):
                regression_result = run_regression(filtered_structured, model_frame, "desired_savings")
                left, right = st.columns(2)
                left.metric("R2 Score", f"{regression_result['r2']:.4f}", help="R² (0 to 1): Measures how well the model explains the variance in savings. Closer to 1.0 means highly accurate predictions.")
                right.metric("RMSE", f"{regression_result['rmse']:,.2f}", help="Root Mean Squared Error: The average error in the predicted savings amount. E.g., if RMSE is 2,000, predictions are off by ₹2,000 on average (lower is better).")
                st.pyplot(actual_vs_predicted(regression_result["y_test"], regression_result["predictions"]))

            classification_result = run_saver_classification(
                filtered_structured,
                model_frame,
                "savings_ratio",
            )
            if classification_result.get("available"):
                st.info("💡 **Classification Metrics:** The model tries to correctly identify what bucket a user theoretically fits into. A high accuracy on the confusion matrix means we can reliably label unseen users.")
                cls_left, cls_right = st.columns(2)
                with cls_left:
                    st.metric("Saver Category Accuracy", f"{classification_result['accuracy']:.4f}", help="Accuracy (0 to 1): The percentage of users correctly categorized as Low, Medium, or High savers by the model. 0.85 means 85% correct predictions.")
                    st.pyplot(
                        confusion_matrix_figure(
                            classification_result["confusion_matrix"],
                            classification_result["labels"],
                        )
                    )
                with cls_right:
                    # Let's show the dataset colored by real Saver Type
                    # Create temporary binning for visualization to answer user requirement
                    temp_df = filtered_structured.copy()
                    bins = np.unique(temp_df["savings_ratio"].quantile([0, 1/3, 2/3, 1]).values)
                    temp_df["Saver_Persona"] = pd.cut(temp_df["savings_ratio"], bins=bins, labels=classification_result["labels"], include_lowest=True)
                    st.markdown("**How do Saver Types stack up in real life?**")
                    st.pyplot(saver_scatter_figure(temp_df, "Saver_Persona"))
            
            st.markdown("---")
            st.subheader("🔮 Predict For a New User")
            st.markdown("Enter custom values below to see the prediction models in action:")
            in_col, ex_col, age_col = st.columns(3)
            test_income = in_col.number_input("Monthly Income", min_value=5000.0, value=50000.0, step=1000.0)
            test_expense = ex_col.number_input("Total Expense", min_value=1000.0, value=30000.0, step=1000.0)
            test_age = age_col.slider("User Age", 18, 80, 30)

            if st.button("Predict Target Savings", width="stretch"):
                # We need to construct an exact row format matching the model
                # The model expects x-features derived from `build_model_frame`
                # which gets dummified. To mock this properly without full dummies:
                # We can just fit a basic linear model locally strictly for Income & Expense
                try:
                    # Quick custom prediction just for this form using existing data
                    X_simple = filtered_structured[["income", "total_expense", "age"]]
                    y_simple_reg = filtered_structured["desired_savings"]
                    
                    from sklearn.linear_model import LinearRegression
                    # Train quick predictive subset regression
                    m_reg = LinearRegression().fit(X_simple, y_simple_reg)
                    mock_reg_pred = m_reg.predict(pd.DataFrame([[test_income, test_expense, test_age]], columns=X_simple.columns))[0]
                    
                    # Train quick predictive subset classification
                    if classification_result.get("available") and "savings_ratio" in filtered_structured.columns:
                        y_simple_clf = classification_result["y_test"].copy() # This includes labels
                        # Just grab from the original classification logic slightly modified:
                        from sklearn.linear_model import LogisticRegression
                        model_frame_slice = filtered_structured[["income", "total_expense", "age"]].dropna()
                        clf_labels = classification_result["labels"]
                        bins = np.unique(filtered_structured["savings_ratio"].quantile([0, 1/3, 2/3, 1]).values)
                        y_targets = pd.cut(filtered_structured.loc[model_frame_slice.index, "savings_ratio"], bins=bins, labels=clf_labels, include_lowest=True)
                        m_clf = LogisticRegression(max_iter=500).fit(model_frame_slice, y_targets)
                        mock_clf_pred = m_clf.predict(pd.DataFrame([[test_income, test_expense, test_age]], columns=model_frame_slice.columns))[0]
                    else:
                        mock_clf_pred = "N/A"

                    # Show Results
                    disp_income = test_income - test_expense
                    
                    st.info("💡 **Why this number?** The 'Predicted Ideal Savings' is NOT a simple math calculator (Income - Expense). It uses our Machine Learning model tracking thousands of users to predict what a typical person with your exact profile *usually* saves behaviorally.")
                    
                    p_col1, p_col2, p_col3 = st.columns(3)
                    p_col1.metric("Max Disposable Income", f"₹ {disp_income:,.2f}")
                    p_col2.metric("Predicted Ideal Savings Amount", f"₹ {mock_reg_pred:,.2f}", 
                        help="Calculated via Linear Regression based on behavioral trends, not pure subtraction.")
                    p_col3.metric("Predicted Saver Persona", f"{mock_clf_pred}",
                        help=f"Classified out of historical Low, Medium, and High Savers.")
                except Exception as e:
                    st.error(f"Need more data variations to predict standard behavior accurately.")
            else:
                st.info("Saver category classification is not informative for the current filtered data.")

    with tabs[3]:
        st.subheader("Behavioral Clustering and PCA")
        st.markdown("🎯 **Goal:** Uncover hidden financial segments that share common spending/saving triggers without labeling them explicitly beforehand. Then, use PCA to compress dimensions safely into a 2D scatter graph so we can actually see the shape of the cohorts.")
        
        if filtered_structured.empty:
            st.warning("No rows available for clustering.")
        else:
            base_columns = ["income", "total_expense", "desired_savings", "age", "dependents"] + expense_cols
            cluster_columns = [column for column in base_columns if column in filtered_structured.columns]
            if len(cluster_columns) < 2:
                st.warning("Not enough numeric columns for clustering.")
            else:
                _, _, x_scaled = prepare_cluster_matrix(filtered_structured, cluster_columns)
                max_k = min(10, len(filtered_structured) - 1)
                k_values, wcss = compute_elbow(x_scaled, max_k)
                st.pyplot(elbow_figure(k_values, wcss))

                k_choice = st.slider("Choose K", min_value=2, max_value=max_k, value=min(4, max_k))
                _, clusters = fit_kmeans(x_scaled, k_choice)
                pca, components = project_to_2d(x_scaled)
                st.pyplot(pca_cluster_figure(components, clusters, pca))
                
                # Show cluster profiles to explain what they mean
                st.markdown("<div class='block-card' style='margin-top:1rem;'><b>Cluster Profiles (Averages)</b></div>", unsafe_allow_html=True)
                st.caption("This shows the defining financial traits of each behavior cluster based on average values.")
                profile_df = filtered_structured.copy()
                profile_df["Cluster"] = clusters
                cols_to_agg = [col for col in ["income", "total_expense", "desired_savings", "age"] if col in profile_df.columns]
                cluster_means = profile_df.groupby("Cluster")[cols_to_agg].mean().round(2)
                st.dataframe(cluster_means.style.format("{:.2f}"), width="stretch")

    with tabs[4]:
        st.subheader("Transaction Trends")
        st.markdown("🎯 **Goal:** Look back at the isolated, granular transaction history to pinpoint real-world categorical expenditure velocity and monthly cash flow.")
        if cleaned_transactions.empty:
            st.warning("No cleaned transaction data available.")
        else:
            left, right = st.columns(2)
            with left:
                st.pyplot(monthly_spending_figure(monthly_spending(cleaned_transactions)))
            with right:
                st.pyplot(category_spending_figure(category_spending(cleaned_transactions)))

    with tabs[5]:
        st.subheader("Data Quality and Cleaning Impact")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Raw Transactions", f"{len(raw_transactions):,}", help="Total number of original uncleaned transaction rows.")
        col2.metric("Clean Transactions", f"{len(cleaned_transactions):,}", help="Total number of transaction rows successfully parsed and cleaned.")
        col3.metric("Invalid Dates", f"{cleaning_summary['invalid_dates']:,}", help="Number of rows dropped because the date format was unrecognizable.")
        col4.metric("Outliers Removed", f"{cleaning_summary['rows_removed_outliers']:,}", help="Number of extreme spending amounts removed to ensure models aren't skewed.")

        left, right = st.columns(2)
        left.markdown("<div class='block-card'><b>Cleaning Summary</b></div>", unsafe_allow_html=True)
        left.write(pd.DataFrame([cleaning_summary]).T.rename(columns={0: "count"}))

        right.markdown("<div class='block-card'><b>Structured Dataset Snapshot</b></div>", unsafe_allow_html=True)
        preview_columns = [
            column
            for column in ["income", "age", "occupation", "city_tier", "total_expense", "desired_savings", "savings_ratio"]
            if column in filtered_structured.columns
        ]
        right.dataframe(filtered_structured[preview_columns].head(10), width="stretch")


if __name__ == "__main__":
    main()
