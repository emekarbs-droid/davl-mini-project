"""
eda.py — Univariate, Bivariate, Multivariate, Correlation analysis.
"""
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


def show_univariate(df, name="Dataset"):
    """Univariate analysis for selected columns."""
    st.subheader(f"📊 Univariate Analysis — {name}")

    num_cols = df.select_dtypes(include="number").columns.tolist()
    cat_cols = df.select_dtypes(include="object").columns.tolist()

    col_type = st.radio("Column type", ["Numeric", "Categorical"],
                        key=f"eda_uni_type_{name}", horizontal=True)

    if col_type == "Numeric":
        if not num_cols:
            st.info("No numeric columns available.")
            return
        col = st.selectbox("Select column", num_cols, key=f"eda_uni_num_{name}")
        data = df[col].dropna()

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Mean", f"{data.mean():.2f}")
        c2.metric("Median", f"{data.median():.2f}")
        c3.metric("Std Dev", f"{data.std():.2f}")
        c4.metric("Skewness", f"{data.skew():.2f}")

        tab1, tab2 = st.tabs(["Histogram", "Box Plot"])
        with tab1:
            fig = px.histogram(df, x=col, title=f"Distribution of {col}",
                               marginal="box", nbins=40)
            st.plotly_chart(fig, use_container_width=True)
        with tab2:
            fig = px.box(df, y=col, title=f"Box Plot — {col}")
            st.plotly_chart(fig, use_container_width=True)
    else:
        if not cat_cols:
            st.info("No categorical columns available.")
            return
        col = st.selectbox("Select column", cat_cols, key=f"eda_uni_cat_{name}")
        counts = df[col].value_counts().head(20)

        st.metric("Unique Values", df[col].nunique())

        tab1, tab2 = st.tabs(["Bar Chart", "Pie Chart"])
        with tab1:
            fig = px.bar(x=counts.index, y=counts.values,
                         title=f"Value Counts — {col}",
                         labels={"x": col, "y": "Count"})
            st.plotly_chart(fig, use_container_width=True)
        with tab2:
            fig = px.pie(values=counts.values, names=counts.index,
                         title=f"Distribution — {col}")
            st.plotly_chart(fig, use_container_width=True)


def show_bivariate(df, name="Dataset"):
    """Bivariate analysis between two selected columns."""
    st.subheader(f"📈 Bivariate Analysis — {name}")

    all_cols = df.columns.tolist()
    c1, c2 = st.columns(2)
    col_x = c1.selectbox("X-axis", all_cols, key=f"eda_bi_x_{name}")
    col_y = c2.selectbox("Y-axis", all_cols,
                         index=min(1, len(all_cols) - 1),
                         key=f"eda_bi_y_{name}")

    x_is_num = pd.api.types.is_numeric_dtype(df[col_x])
    y_is_num = pd.api.types.is_numeric_dtype(df[col_y])

    if x_is_num and y_is_num:
        fig = px.scatter(df.head(3000), x=col_x, y=col_y,
                         title=f"{col_x} vs {col_y}", opacity=0.5)
        st.plotly_chart(fig, use_container_width=True)
    elif not x_is_num and y_is_num:
        top = df[col_x].value_counts().head(15).index
        filtered = df[df[col_x].isin(top)]
        fig = px.box(filtered, x=col_x, y=col_y,
                     title=f"{col_y} by {col_x}")
        st.plotly_chart(fig, use_container_width=True)
    elif x_is_num and not y_is_num:
        top = df[col_y].value_counts().head(15).index
        filtered = df[df[col_y].isin(top)]
        fig = px.box(filtered, x=col_y, y=col_x,
                     title=f"{col_x} by {col_y}")
        st.plotly_chart(fig, use_container_width=True)
    else:
        ct = pd.crosstab(df[col_x], df[col_y])
        ct = ct.loc[ct.sum(axis=1).nlargest(10).index,
                     ct.sum(axis=0).nlargest(10).index]
        fig = px.imshow(ct, title=f"Crosstab — {col_x} vs {col_y}",
                        text_auto=True, aspect="auto")
        st.plotly_chart(fig, use_container_width=True)


def show_multivariate(df, name="Dataset"):
    """Multivariate analysis — scatter matrix."""
    st.subheader(f"🔗 Multivariate Analysis — {name}")

    num_cols = df.select_dtypes(include="number").columns.tolist()
    if len(num_cols) < 2:
        st.info("Need at least 2 numeric columns.")
        return

    selected = st.multiselect("Select numeric columns (2–5)", num_cols,
                              default=num_cols[:min(3, len(num_cols))],
                              key=f"eda_multi_cols_{name}")
    if len(selected) < 2:
        st.warning("Select at least 2 columns.")
        return

    cat_cols = df.select_dtypes(include="object").columns.tolist()
    color_col = st.selectbox("Color by (optional)",
                             ["None"] + cat_cols, key=f"eda_multi_color_{name}")

    sub = df[selected + ([color_col] if color_col != "None" else [])].dropna().head(2000)
    fig = px.scatter_matrix(sub, dimensions=selected,
                            color=color_col if color_col != "None" else None,
                            title="Scatter Matrix", opacity=0.4)
    fig.update_layout(height=600)
    st.plotly_chart(fig, use_container_width=True)


def show_correlation(df, name="Dataset"):
    """Correlation heatmap for numeric columns."""
    st.subheader(f"🔥 Correlation Matrix — {name}")

    num_cols = df.select_dtypes(include="number").columns.tolist()
    if len(num_cols) < 2:
        st.info("Need at least 2 numeric columns for correlation.")
        return

    method = st.selectbox("Method", ["pearson", "spearman", "kendall"],
                          key=f"eda_corr_method_{name}")
    corr = df[num_cols].corr(method=method)

    fig = px.imshow(corr, text_auto=".2f", title=f"Correlation Heatmap ({method})",
                    color_continuous_scale="RdBu_r", aspect="auto",
                    zmin=-1, zmax=1)
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)

    # Top correlations
    with st.expander("Top Correlated Pairs"):
        pairs = []
        for i in range(len(num_cols)):
            for j in range(i + 1, len(num_cols)):
                pairs.append({
                    "Feature 1": num_cols[i],
                    "Feature 2": num_cols[j],
                    "Correlation": round(corr.iloc[i, j], 4),
                })
        pairs_df = pd.DataFrame(pairs).sort_values("Correlation",
                                                     key=abs, ascending=False)
        st.dataframe(pairs_df, use_container_width=True, hide_index=True)
