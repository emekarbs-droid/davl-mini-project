"""
visualization.py — Histogram, Boxplot, Scatter, Heatmap, Violin wrappers.
"""
import pandas as pd
import streamlit as st
import plotly.express as px


def show_visualization(df, name="Dataset"):
    """General-purpose visualization page."""
    st.subheader(f"🎨 Visualizations — {name}")

    chart_type = st.selectbox(
        "Chart Type",
        ["Histogram", "Box Plot", "Violin Plot", "Scatter Plot",
         "Bar Chart", "Count Plot", "Pair Plot (sample)"],
        key=f"viz_chart_type_{name}",
    )

    num_cols = df.select_dtypes(include="number").columns.tolist()
    cat_cols = df.select_dtypes(include="object").columns.tolist()
    all_cols = df.columns.tolist()

    if chart_type == "Histogram":
        col = st.selectbox("Column", num_cols or all_cols, key=f"viz_hist_col_{name}")
        bins = st.slider("Bins", 10, 100, 30, key=f"viz_hist_bins_{name}")
        color = st.selectbox("Color by", ["None"] + cat_cols, key=f"viz_hist_color_{name}")
        fig = px.histogram(df, x=col, nbins=bins,
                           color=None if color == "None" else color,
                           title=f"Histogram — {col}", marginal="rug")
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Box Plot":
        if not num_cols:
            st.info("No numeric columns available.")
            return
        col = st.selectbox("Value column", num_cols, key=f"viz_box_col_{name}")
        group = st.selectbox("Group by", ["None"] + cat_cols, key=f"viz_box_group_{name}")
        if group != "None":
            top = df[group].value_counts().head(15).index
            filtered = df[df[group].isin(top)]
            fig = px.box(filtered, x=group, y=col, title=f"Box Plot — {col} by {group}")
        else:
            fig = px.box(df, y=col, title=f"Box Plot — {col}")
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Violin Plot":
        if not num_cols:
            st.info("No numeric columns available.")
            return
        col = st.selectbox("Value column", num_cols, key=f"viz_vio_col_{name}")
        group = st.selectbox("Group by", ["None"] + cat_cols, key=f"viz_vio_group_{name}")
        if group != "None":
            top = df[group].value_counts().head(10).index
            filtered = df[df[group].isin(top)]
            fig = px.violin(filtered, x=group, y=col, box=True,
                            title=f"Violin — {col} by {group}")
        else:
            fig = px.violin(df, y=col, box=True, title=f"Violin — {col}")
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Scatter Plot":
        if len(num_cols) < 2:
            st.info("Need at least 2 numeric columns.")
            return
        c1, c2 = st.columns(2)
        x = c1.selectbox("X", num_cols, key=f"viz_sc_x_{name}")
        y = c2.selectbox("Y", num_cols, index=min(1, len(num_cols)-1), key=f"viz_sc_y_{name}")
        color = st.selectbox("Color by", ["None"] + cat_cols, key=f"viz_sc_color_{name}")
        fig = px.scatter(df.head(3000), x=x, y=y,
                         color=None if color == "None" else color,
                         title=f"Scatter — {x} vs {y}", opacity=0.6)
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Bar Chart":
        col = st.selectbox("Column", cat_cols or all_cols, key=f"viz_bar_col_{name}")
        top_n = st.slider("Top N", 5, 30, 10, key=f"viz_bar_n_{name}")
        counts = df[col].value_counts().head(top_n)
        fig = px.bar(x=counts.index, y=counts.values,
                     title=f"Bar Chart — {col}", labels={"x": col, "y": "Count"})
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Count Plot":
        col = st.selectbox("Column", cat_cols or all_cols, key=f"viz_cnt_col_{name}")
        hue = st.selectbox("Hue", ["None"] + cat_cols, key=f"viz_cnt_hue_{name}")
        if hue != "None":
            ct = df.groupby([col, hue]).size().reset_index(name="count")
            top = df[col].value_counts().head(15).index
            ct = ct[ct[col].isin(top)]
            fig = px.bar(ct, x=col, y="count", color=hue, barmode="group",
                         title=f"Count Plot — {col} by {hue}")
        else:
            counts = df[col].value_counts().head(15)
            fig = px.bar(x=counts.index, y=counts.values,
                         title=f"Count — {col}", labels={"x": col, "y": "Count"})
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Pair Plot (sample)":
        if len(num_cols) < 2:
            st.info("Need at least 2 numeric columns.")
            return
        selected = st.multiselect("Columns", num_cols,
                                  default=num_cols[:min(4, len(num_cols))],
                                  key=f"viz_pair_cols_{name}")
        if len(selected) >= 2:
            color = st.selectbox("Color by", ["None"] + cat_cols, key=f"viz_pair_color_{name}")
            sub = df[selected + ([color] if color != "None" else [])].dropna().head(1000)
            fig = px.scatter_matrix(sub, dimensions=selected,
                                    color=color if color != "None" else None,
                                    title="Pair Plot", opacity=0.5)
            fig.update_layout(height=600)
            st.plotly_chart(fig, use_container_width=True)
