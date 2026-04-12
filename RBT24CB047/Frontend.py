import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

st.set_page_config(page_title="IPL Match Winner ML Dashboard", layout="wide")
st.title("🏏 IPL Match Winner ML Dashboard")

@st.cache_data
def load_data():
    matches_df = None
    deliveries_df = None
    
    if os.path.exists("matches.csv"):
        matches_df = pd.read_csv("matches.csv")
    if os.path.exists("deliveries.csv"):
        deliveries_df = pd.read_csv("deliveries.csv")
    
    return matches_df, deliveries_df

matches_df, deliveries_df = load_data()

if matches_df is None:
    st.error("No matches.csv dataset found. Place `matches.csv` in the project folder.")
    st.stop()

st.write("✅ Matches dataset loaded successfully!")
if deliveries_df is not None:
    st.write("✅ Deliveries dataset loaded successfully!")

df = matches_df

if True:
    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    st.markdown("---")
    st.header("📊 Exploratory Data Analysis")

    st.subheader("Winner Distribution")
    fig1, ax1 = plt.subplots(figsize=(10, 4))
    df["winner"].value_counts().plot(kind="bar", ax=ax1)
    ax1.set_ylabel("Match Count")
    ax1.set_xlabel("Winner")
    ax1.set_title("Winner Distribution")
    plt.xticks(rotation=45, ha="right")
    st.pyplot(fig1)

    st.subheader("Toss Decision Distribution")
    fig2, ax2 = plt.subplots(figsize=(8, 4))
    df["toss_decision"].value_counts().plot(kind="bar", ax=ax2, color="tab:orange")
    ax2.set_ylabel("Count")
    ax2.set_title("Toss Decision")
    st.pyplot(fig2)

    st.subheader("Matches by Season")
    fig3, ax3 = plt.subplots(figsize=(10, 4))
    df["season"].value_counts().sort_index().plot(kind="bar", ax=ax3, color="tab:green")
    ax3.set_ylabel("Matches")
    ax3.set_title("Matches per Season")
    st.pyplot(fig3)

    st.subheader("Numeric Correlation - Matches Dataset")
    numeric_df = df.select_dtypes(include=[np.number])
    fig4, ax4 = plt.subplots(figsize=(10, 8))
    sns.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm", ax=ax4, fmt='.2f', cbar_kws={'label': 'Correlation'})
    ax4.set_title("Correlation Heatmap - Matches Data")
    st.pyplot(fig4)

    if deliveries_df is not None:
        st.subheader("Numeric Correlation - Deliveries Dataset")
        deliveries_numeric = deliveries_df.select_dtypes(include=[np.number])
        
        if len(deliveries_numeric.columns) > 1:
            fig_deliv, ax_deliv = plt.subplots(figsize=(10, 8))
            sns.heatmap(deliveries_numeric.corr(), annot=True, cmap="viridis", ax=ax_deliv, fmt='.2f', cbar_kws={'label': 'Correlation'})
            ax_deliv.set_title("Correlation Heatmap - Deliveries Data")
            st.pyplot(fig_deliv)
        else:
            st.info("Deliveries dataset has fewer than 2 numeric columns for correlation analysis.")

    st.subheader("Pair Plot (Sample)")
    sample = numeric_df.sample(min(300, len(numeric_df)), random_state=42)
    pair = sns.pairplot(sample)
    st.pyplot(pair.fig)

    if deliveries_df is not None:
        st.markdown("---")
        st.header("📈 Deliveries Dataset Analysis")
        
        st.subheader("Deliveries Dataset Preview")
        st.dataframe(deliveries_df.head())
        
        # Runs by batsmen (top 15) - Heatmap style visualization
        st.subheader("Runs Distribution Analysis")
        if 'batsman' in deliveries_df.columns and 'runs' in deliveries_df.columns:
            top_batsmen = deliveries_df.groupby('batsman')['runs'].sum().nlargest(15)
            
            fig_bat, ax_bat = plt.subplots(figsize=(12, 6))
            top_batsmen.plot(kind='barh', ax=ax_bat, color='steelblue')
            ax_bat.set_xlabel('Total Runs')
            ax_bat.set_title('Top 15 Batsmen by Total Runs')
            st.pyplot(fig_bat)
        
        # Wickets by bowlers - Heatmap style
        st.subheader("Wickets by Bowlers")
        if 'bowler' in deliveries_df.columns and 'is_wicket' in deliveries_df.columns:
            top_bowlers = deliveries_df[deliveries_df['is_wicket'] == 1].groupby('bowler').size().nlargest(15)
            
            fig_bowl, ax_bowl = plt.subplots(figsize=(12, 6))
            top_bowlers.plot(kind='barh', ax=ax_bowl, color='coral')
            ax_bowl.set_xlabel('Wickets')
            ax_bowl.set_title('Top 15 Bowlers by Wickets')
            st.pyplot(fig_bowl)
        
        # Runs per over heatmap
        st.subheader("Runs Distribution by Ball Type")
        if 'ball' in deliveries_df.columns and 'runs' in deliveries_df.columns:
            fig_ball, ax_ball = plt.subplots(figsize=(10, 5))
            ball_runs = deliveries_df.groupby('ball')['runs'].value_counts().unstack(fill_value=0)
            sns.heatmap(ball_runs, annot=True, cmap='YlOrRd', ax=ax_ball, fmt='d', cbar_kws={'label': 'Frequency'})
            ax_ball.set_title('Heatmap: Runs by Ball Position')
            st.pyplot(fig_ball)

    st.markdown("---")
    st.header("🤖 Model Training & Comparison")

    df_ml = df.copy()
    df_ml["team1_wins"] = (df_ml["winner"] == df_ml["team1"]).astype(int)

    features = df_ml[["season", "city", "team1", "team2", "toss_winner", "toss_decision", "dl_applied", "venue"]].copy()
    features["city"] = features["city"].fillna("Unknown")
    features["venue"] = features["venue"].fillna("Unknown")

    X = pd.get_dummies(features, drop_first=True)
    y = df_ml["team1_wins"]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000, solver="liblinear"),
        "Decision Tree": DecisionTreeClassifier(random_state=42),
        "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
    }

    results = {}
    for name, model in models.items():
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        results[name] = accuracy_score(y_test, preds)

    st.subheader("Model Accuracy")
    for name, score in results.items():
        st.write(f"**{name}**: {score:.4f}")

    st.subheader("Model Comparison")
    fig5, ax5 = plt.subplots(figsize=(8, 4))
    ax5.bar(results.keys(), results.values(), color=["tab:blue", "tab:green", "tab:red"])
    ax5.set_ylim(0, 1)
    ax5.set_ylabel("Accuracy")
    ax5.set_title("Comparison of Classifier Accuracy")
    plt.xticks(rotation=20)
    st.pyplot(fig5)

    best_model = max(results, key=results.get)
    st.success(f"🏆 Best Model: {best_model} with accuracy {results[best_model]:.4f}")
