import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# -------------------------------
# TITLE
# -------------------------------
st.title("📊Weather Predicter")

# -------------------------------
# FILE UPLOAD
# -------------------------------
file = st.file_uploader("Upload CSV File", type=["csv"])

if file:
    df = pd.read_csv(file)
    
    st.subheader("Dataset Preview")
    st.write(df.head())

    # -------------------------------
    # DATA OVERVIEW
    # -------------------------------
    st.subheader("Data Overview")
    st.write(df.info())

    st.subheader("Statistical Summary")
    st.write(df.describe())

    # -------------------------------
    # PREPROCESSING
    # -------------------------------
    df = df.copy()

    # Handle missing values
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col].fillna(df[col].mode()[0], inplace=True)
        else:
            df[col].fillna(df[col].mean(), inplace=True)

    # Encode categorical
    le = LabelEncoder()
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = le.fit_transform(df[col])

    # -------------------------------
    # CORRELATION HEATMAP
    # -------------------------------
    fig, ax = plt.subplots(figsize=(16, 16))

    sns.heatmap(
        df.corr(),
        cmap="coolwarm"
    )

    st.pyplot(fig)

    # -------------------------------
    # HISTOGRAM
    # -------------------------------
    st.subheader("Distribution Plot (Histogram)")
    col = st.selectbox("Select column", df.columns)
    fig, ax = plt.subplots()
    sns.histplot(df[col], kde=True, ax=ax)
    st.pyplot(fig)

    # -------------------------------
    # BOX PLOT
    # -------------------------------
    selected_cols = st.multiselect(
    "Select columns for Box Plot",
    df.select_dtypes(include=np.number).columns,
    default=df.select_dtypes(include=np.number).columns[:5]
)

    if selected_cols:
        fig, ax = plt.subplots(figsize=(12,6)) 
        sns.boxplot(data=df[selected_cols], ax=ax)
        plt.xticks(rotation=45)
        st.pyplot(fig)

    # -------------------------------
    # SCATTER PLOT
    # -------------------------------
    st.subheader("Scatter Plot")
    x = st.selectbox("X-axis", df.columns)
    y = st.selectbox("Y-axis", df.columns)

    fig, ax = plt.subplots()
    sns.scatterplot(x=df[x], y=df[y], ax=ax)
    st.pyplot(fig)

    # -------------------------------
    # PAIR PLOT
    # -------------------------------
    st.subheader("Pair Plot")
    if st.button("Generate Pair Plot"):
        fig = sns.pairplot(df)
        st.pyplot(fig)

    # -------------------------------
    # PCA
    # -------------------------------
    st.subheader("PCA")
    if st.button("Run PCA"):
        scaler = StandardScaler()
        scaled = scaler.fit_transform(df)

        pca = PCA(n_components=2)
        pca_result = pca.fit_transform(scaled)

        pca_df = pd.DataFrame(pca_result, columns=['PC1', 'PC2'])
        st.write(pca_df)

        fig, ax = plt.subplots()
        ax.scatter(pca_df['PC1'], pca_df['PC2'])
        ax.set_title("PCA Scatter")
        st.pyplot(fig)

    # -------------------------------
    # TARGET COLUMN
    # -------------------------------
    target = st.selectbox("Select Target Column", df.columns)

    X = df.drop(columns=[target])
    y = df[target]

    scaler = StandardScaler()
    X = scaler.fit_transform(X)

    # -------------------------------
    # LDA
    # -------------------------------
    st.subheader("LDA")
    if st.button("Run LDA"):
        lda = LDA(n_components=1)
        lda_result = lda.fit_transform(X, y)

        lda_df = pd.DataFrame(lda_result, columns=['LD1'])
        st.write(lda_df)

    # -------------------------------
    # MODEL TRAINING
    # -------------------------------
    st.subheader("Model Training")

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    # Choose model type
    task = st.radio("Choose Task", ["Regression", "Classification"])

    if task == "Regression":
        model = LinearRegression()
        model.fit(X_train, y_train)
        preds = model.predict(X_test)

        st.write("Predictions:", preds[:5])

    else:
        models = {
            "Logistic Regression": LogisticRegression(),
            "Decision Tree": DecisionTreeClassifier(),
            "Random Forest": RandomForestClassifier()
        }

        results = {}

        for name, model in models.items():
            model.fit(X_train, y_train)
            preds = model.predict(X_test)

            acc = accuracy_score(y_test, preds)
            results[name] = acc

            st.subheader(name)
            st.write("Accuracy:", acc)
            st.write("Confusion Matrix:")
            st.write(confusion_matrix(y_test, preds))

        # -------------------------------
        # MODEL COMPARISON
        # -------------------------------
        st.subheader("Model Comparison")
        st.write(results)