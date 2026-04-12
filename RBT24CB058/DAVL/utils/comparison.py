"""
comparison.py — Full Dataset A vs Dataset B comparison.
"""
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def show_comparison(df_a, df_b, name_a="Dataset A", name_b="Dataset B"):
    """Side-by-side comparison of two datasets."""
    st.subheader(f"🔀 Comparison — {name_a} vs {name_b}")

    # ── Shape comparison ──
    st.markdown("### Shape")
    c1, c2 = st.columns(2)
    c1.metric(name_a, f"{df_a.shape[0]:,} × {df_a.shape[1]}")
    c2.metric(name_b, f"{df_b.shape[0]:,} × {df_b.shape[1]}")

    # ── Column overlap ──
    st.markdown("### Column Overlap")
    cols_a = set(df_a.columns)
    cols_b = set(df_b.columns)
    common = cols_a & cols_b
    only_a = cols_a - cols_b
    only_b = cols_b - cols_a

    c1, c2, c3 = st.columns(3)
    c1.metric("Common Columns", len(common))
    c2.metric(f"Only in {name_a}", len(only_a))
    c3.metric(f"Only in {name_b}", len(only_b))

    if common:
        with st.expander("Common Columns"):
            st.write(", ".join(sorted(common)))
    if only_a:
        with st.expander(f"Only in {name_a}"):
            st.write(", ".join(sorted(only_a)))
    if only_b:
        with st.expander(f"Only in {name_b}"):
            st.write(", ".join(sorted(only_b)))

    # ── Missing values comparison ──
    st.markdown("### Missing Values Comparison")
    common_list = sorted(common)
    if common_list:
        miss_a = (df_a[common_list].isnull().sum() / len(df_a) * 100).round(2)
        miss_b = (df_b[common_list].isnull().sum() / len(df_b) * 100).round(2)
        miss_df = pd.DataFrame({
            "Column": common_list,
            f"{name_a} Missing %": miss_a.values,
            f"{name_b} Missing %": miss_b.values,
        })
        st.dataframe(miss_df, use_container_width=True, hide_index=True)

        # Bar chart
        fig = go.Figure()
        fig.add_trace(go.Bar(x=common_list, y=miss_a.values, name=name_a,
                             marker_color="#E50914"))
        fig.add_trace(go.Bar(x=common_list, y=miss_b.values, name=name_b,
                             marker_color="#00A8E1"))
        fig.update_layout(title="Missing % Comparison", barmode="group",
                          height=400, yaxis_title="Missing %")
        st.plotly_chart(fig, use_container_width=True)

    # ── Numeric stats comparison ──
    st.markdown("### Numeric Statistics Comparison")
    num_common = [c for c in common_list
                  if pd.api.types.is_numeric_dtype(df_a[c])
                  and pd.api.types.is_numeric_dtype(df_b[c])]

    if num_common:
        stats_rows = []
        for col in num_common:
            stats_rows.append({
                "Column": col,
                f"{name_a} Mean": round(df_a[col].mean(), 2),
                f"{name_b} Mean": round(df_b[col].mean(), 2),
                f"{name_a} Median": round(df_a[col].median(), 2),
                f"{name_b} Median": round(df_b[col].median(), 2),
                f"{name_a} Std": round(df_a[col].std(), 2),
                f"{name_b} Std": round(df_b[col].std(), 2),
            })
        st.dataframe(pd.DataFrame(stats_rows), use_container_width=True, hide_index=True)

    # ── Categorical comparison ──
    st.markdown("### Categorical Value Comparison")
    cat_common = [c for c in common_list
                  if df_a[c].dtype == "object" and df_b[c].dtype == "object"]

    if cat_common:
        sel_col = st.selectbox("Select column", cat_common, key="comp_cat_col")

        fig = make_subplots(rows=1, cols=2,
                            subplot_titles=(name_a, name_b))
        for i, df, color in [(1, df_a, "#E50914"), (2, df_b, "#00A8E1")]:
            counts = df[sel_col].value_counts().head(10)
            fig.add_trace(go.Bar(x=counts.index, y=counts.values,
                                 marker_color=color), row=1, col=i)
        fig.update_layout(title=f"Top values — {sel_col}", height=400,
                          showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    # ── Row count comparison by a column ──
    st.markdown("### Value Count Comparison")
    if cat_common:
        comp_col = st.selectbox("Compare distribution of", cat_common,
                                key="comp_dist_col")
        counts_a = df_a[comp_col].value_counts().head(15)
        counts_b = df_b[comp_col].value_counts().head(15)
        all_vals = sorted(set(counts_a.index) | set(counts_b.index))

        fig = go.Figure()
        fig.add_trace(go.Bar(x=all_vals,
                             y=[counts_a.get(v, 0) for v in all_vals],
                             name=name_a, marker_color="#E50914"))
        fig.add_trace(go.Bar(x=all_vals,
                             y=[counts_b.get(v, 0) for v in all_vals],
                             name=name_b, marker_color="#00A8E1"))
        fig.update_layout(title=f"Distribution — {comp_col}", barmode="group",
                          height=400)
        st.plotly_chart(fig, use_container_width=True)
