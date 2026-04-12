import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix

st.set_page_config(page_title="ML App", layout="wide")

st.title("🧠 Mental Health / ML Analyzer")

# ---------------- Sidebar ----------------
st.sidebar.header("Upload Dataset")
file = st.sidebar.file_uploader("Upload CSV", type=["csv"])

if file:
    df = pd.read_csv(file)

    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    # ---------------- Model Setup ----------------
    st.subheader("⚙️ Model Setup")

    target = st.selectbox("Select Target Column", df.columns)

    features = st.multiselect(
        "Select Features",
        [col for col in df.columns if col != target],
        default=[col for col in df.columns if col != target][:4]
    )

    model_name = st.selectbox(
        "Choose Model",
        ["Logistic Regression", "Random Forest"]
    )

    if len(features) > 0:

        data = df[features + [target]].copy()

        # ---------------- FIX MISSING VALUES ----------------
        for col in data.columns:
            if pd.api.types.is_numeric_dtype(data[col]):
                data[col] = data[col].fillna(data[col].median())
            else:
                data[col] = data[col].fillna(data[col].mode()[0])

        # ---------------- 🔥 FORCE ENCODING (IMPORTANT FIX) ----------------
        encoders = {}

        for col in data.columns:
            if not pd.api.types.is_numeric_dtype(data[col]):
                le = LabelEncoder()
                data[col] = le.fit_transform(data[col].astype(str))
                encoders[col] = le

        # ---------------- FINAL SAFETY CHECK ----------------
        if data.select_dtypes(include=['object']).shape[1] > 0:
            st.error("❌ Encoding issue still present")
            st.write(data.dtypes)
            st.stop()

        X = data[features]
        y = data[target]

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # ---------------- TRAIN MODEL ----------------
        if st.button("🚀 Train Model"):

            if model_name == "Logistic Regression":
                model = LogisticRegression(max_iter=1000)
            else:
                model = RandomForestClassifier()

            model.fit(X_train, y_train)
            pred = model.predict(X_test)

            acc = accuracy_score(y_test, pred)
            st.success(f"✅ Accuracy: {acc:.2f}")

            # Save model
            st.session_state["model"] = model
            st.session_state["encoders"] = encoders
            st.session_state["features"] = features

            # ---------------- CONFUSION MATRIX ----------------
            st.subheader("Confusion Matrix")

            cm = confusion_matrix(y_test, pred)

            fig, ax = plt.subplots()
            sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=ax)
            st.pyplot(fig)

            # ---------------- FEATURE IMPORTANCE ----------------
            if model_name == "Random Forest":
                st.subheader("Feature Importance")

                importance = model.feature_importances_
                imp_df = pd.DataFrame({
                    "Feature": features,
                    "Importance": importance
                }).sort_values(by="Importance", ascending=False)

                fig, ax = plt.subplots()
                sns.barplot(x="Importance", y="Feature", data=imp_df, ax=ax)
                st.pyplot(fig)

        # ---------------- EDA ----------------
        st.subheader("📊 Data Visualization")

        col1, col2 = st.columns(2)

        with col1:
            hist_col = st.selectbox("Histogram Column", df.columns)
            fig, ax = plt.subplots()
            sns.histplot(df[hist_col], kde=True, ax=ax)
            st.pyplot(fig)

        with col2:
            box_col = st.selectbox("Box Plot Column", df.columns)
            fig, ax = plt.subplots()
            sns.boxplot(x=df[box_col], ax=ax)
            st.pyplot(fig)

        st.subheader("Correlation Heatmap")
        fig, ax = plt.subplots(figsize=(10,6))
        sns.heatmap(df.corr(numeric_only=True), annot=True, cmap="coolwarm", ax=ax)
        st.pyplot(fig)

        # ---------------- USER INPUT PREDICTION ----------------
        st.subheader("🔮 Predict from User Input")

        if "model" in st.session_state:

            input_data = {}

            for col in st.session_state["features"]:

                # ✅ FIXED (no mean error)
                if pd.api.types.is_numeric_dtype(df[col]):
                    val = st.number_input(
                        f"{col}",
                        value=float(df[col].mean())
                    )
                else:
                    val = st.selectbox(
                        f"{col}",
                        df[col].astype(str).unique().tolist()
                    )

                input_data[col] = val

            if st.button("Predict"):

                input_df = pd.DataFrame([input_data])

                # Apply encoding
                for col in input_df.columns:
                    if col in st.session_state["encoders"]:
                        input_df[col] = st.session_state["encoders"][col].transform(
                            input_df[col].astype(str)
                        )

                prediction = st.session_state["model"].predict(input_df)

                st.success(f"🎯 Prediction: {prediction[0]}")

                # Bonus score
                score = 0
                for val in input_data.values():
                    if isinstance(val, (int, float)):
                        score += val

                st.info(f"🧠 Simple Mental Score: {score:.2f}")

        else:
            st.warning("⚠️ Train model first")

    else:
        st.warning("Select at least one feature")

else:
    st.info("👈 Upload dataset to start")