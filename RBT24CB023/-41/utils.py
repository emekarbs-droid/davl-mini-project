import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st


def plot_histogram(df, col):
    fig, ax = plt.subplots()
    df[col].hist(ax=ax)
    st.pyplot(fig)


def plot_boxplot(df):
    fig, ax = plt.subplots()
    df.plot(kind='box', ax=ax)
    st.pyplot(fig)


def plot_scatter(df, x, y):
    fig, ax = plt.subplots()
    ax.scatter(df[x], df[y])
    ax.set_xlabel(x)
    ax.set_ylabel(y)
    st.pyplot(fig)


def plot_heatmap(df):
    import numpy as np
    
    numeric_df = df.select_dtypes(include=[np.number])

    if numeric_df.shape[1] < 2:
        st.warning("Not enough numeric columns for heatmap")
        return

    fig, ax = plt.subplots()
    sns.heatmap(numeric_df.corr(), ax=ax, annot=True)
    st.pyplot(fig)