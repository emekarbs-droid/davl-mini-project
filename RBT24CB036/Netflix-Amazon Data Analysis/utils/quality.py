"""
quality.py — Missing values, duplicates, outliers, class imbalance.
"""
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


def show_missing_values(df, name="Dataset"):
    """Display missing value analysis."""
    st.subheader(f"🔍 Missing Values — {name}")

    missing = df.isnull().sum()
    missing_pct = (df.isnull().sum() / len(df) * 100).round(2)
    missing_df = pd.DataFrame({
        "Column": missing.index,
        "Missing Count": missing.values,
        "Missing %": missing_pct.values,
        "Present Count": (len(df) - missing).values,
    }).sort_values("Missing Count", ascending=False)

    st.dataframe(missing_df, use_container_width=True, hide_index=True)

    # bar chart
    cols_with_missing = missing_df[missing_df["Missing Count"] > 0]
    if len(cols_with_missing) > 0:
        fig = px.bar(cols_with_missing, x="Column", y="Missing %",
                     title=f"{name} — Missing Values %",
                     text="Missing %", color="Missing %",
                     color_continuous_scale="Reds")
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.success("No missing values found!")

    # Null heatmap
    if df.isnull().sum().sum() > 0:
        with st.expander("Null Pattern Heatmap"):
            sample = df.head(100)
            fig = go.Figure(data=go.Heatmap(
                z=sample.isnull().astype(int).values,
                x=df.columns.tolist(),
                y=[str(i) for i in range(len(sample))],
                colorscale=[[0, "#e8f5e9"], [1, "#e53935"]],
                showscale=True,
            ))
            fig.update_layout(title="Null Pattern (first 100 rows)", height=400,
                              xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)


def show_duplicates(df, name="Dataset"):
    """Display duplicate row analysis."""
    st.subheader(f"📑 Duplicate Rows — {name}")

    dup_count = df.duplicated().sum()
    st.metric("Duplicate Rows", dup_count)

    if dup_count > 0:
        st.warning(f"Found {dup_count} duplicate rows.")
        with st.expander("Show Duplicate Rows"):
            st.dataframe(df[df.duplicated(keep=False)].head(20),
                         use_container_width=True)
    else:
        st.success("No duplicate rows found.")


def show_outliers(df, name="Dataset"):
    """Detect outliers using IQR method for numeric columns."""
    st.subheader(f"📦 Outlier Detection (IQR) — {name}")

    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    if not numeric_cols:
        st.info("No numeric columns for outlier detection.")
        return

    outlier_info = []
    for col in numeric_cols:
        data = df[col].dropna()
        if len(data) == 0:
            continue
        Q1 = data.quantile(0.25)
        Q3 = data.quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        outliers = ((data < lower) | (data > upper)).sum()
        outlier_info.append({
            "Column": col,
            "Q1": round(Q1, 2),
            "Q3": round(Q3, 2),
            "IQR": round(IQR, 2),
            "Lower Bound": round(lower, 2),
            "Upper Bound": round(upper, 2),
            "Outlier Count": int(outliers),
            "Outlier %": round(outliers / len(data) * 100, 2),
        })

    if outlier_info:
        outlier_df = pd.DataFrame(outlier_info)
        st.dataframe(outlier_df, use_container_width=True, hide_index=True)

        # Box plots
        with st.expander("Box Plots"):
            selected = st.multiselect("Select columns", numeric_cols,
                                      default=numeric_cols[:min(3, len(numeric_cols))],
                                      key=f"quality_outlier_box_{name}")
            if selected:
                fig = px.box(df, y=selected, title="Box Plots")
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)


def show_class_imbalance(df, target_col, name="Dataset"):
    """Show class distribution for a target column."""
    st.subheader(f"⚖️ Class Imbalance — {name}")

    if target_col is None or target_col not in df.columns:
        st.info("No target column detected.")
        return

    counts = df[target_col].value_counts()
    st.dataframe(
        pd.DataFrame({"Class": counts.index, "Count": counts.values,
                       "%": (counts.values / len(df) * 100).round(2)}),
        use_container_width=True, hide_index=True
    )

    fig = px.pie(values=counts.values, names=counts.index,
                 title=f"Class Distribution — {target_col}")
    st.plotly_chart(fig, use_container_width=True)
