import matplotlib.pyplot as plt
import seaborn as sns


def income_histogram(df):
    fig, ax = plt.subplots(figsize=(7, 4.2))
    ax.hist(df["income"], bins=35, color="#0ea5a4", edgecolor="#0f172a", alpha=0.85)
    ax.set_title("Income Distribution")
    ax.set_xlabel("Income")
    ax.set_ylabel("Frequency")
    ax.grid(alpha=0.2)
    return fig


def income_expense_scatter(df):
    fig, ax = plt.subplots(figsize=(7, 4.2))
    target_column = "total_expense" if "total_expense" in df.columns else "desired_savings"
    ax.scatter(df["income"], df[target_column], alpha=0.35, color="#f59e0b", s=16)
    ax.set_title(f"Income vs {target_column.replace('_', ' ').title()}")
    ax.set_xlabel("Income")
    ax.set_ylabel(target_column.replace("_", " ").title())
    ax.grid(alpha=0.2)
    return fig


def correlation_heatmap(df):
    fig, ax = plt.subplots(figsize=(9, 6))
    sns.heatmap(df.corr(numeric_only=True), cmap="YlGnBu", ax=ax, linewidths=0.4)
    ax.set_title("Correlation Matrix")
    return fig


def actual_vs_predicted(y_test, predictions):
    """
    Plots regression performance. Points closer to the diagonal red line
    indicate higher accuracy in predicting the target variable.
    """
    fig, ax = plt.subplots(figsize=(8, 4.8))
    ax.scatter(y_test, predictions, alpha=0.35, color="#14b8a6")
    bounds = [min(y_test.min(), predictions.min()), max(y_test.max(), predictions.max())]
    ax.plot(bounds, bounds, color="#b91c1c", linewidth=2)
    ax.set_title("Regression: Actual vs Predicted Savings")
    ax.set_xlabel("Actual")
    ax.set_ylabel("Predicted")
    ax.grid(alpha=0.2)
    return fig


def confusion_matrix_figure(cm, labels):
    fig, ax = plt.subplots(figsize=(6.5, 4.8))
    sns.heatmap(cm, annot=True, fmt="d", cmap="YlOrBr", xticklabels=labels, yticklabels=labels, ax=ax)
    ax.set_title("Saver Class Confusion Matrix")
    ax.set_xlabel("Predicted Persona")
    ax.set_ylabel("Actual Persona")
    return fig


def saver_scatter_figure(df, class_col):
    """
    Visualizes the users in the dataset colored by their strictly classified Saver Persona.
    Shows the relationship between Income, Expenses, and their Saver group.
    """
    fig, ax = plt.subplots(figsize=(8, 4.8))
    colors = {"Low Saver": "#ef4444", "Medium Saver": "#eab308", "High Saver": "#22c55e"}
    for label, color in colors.items():
        subset = df[df[class_col] == label]
        ax.scatter(subset["income"], subset["total_expense"], c=color, label=label, alpha=0.6, s=25)
    
    ax.set_title("Users Colored by Saver Persona")
    ax.set_xlabel("Income")
    ax.set_ylabel("Total Expense")
    ax.legend(title="Persona")
    ax.grid(alpha=0.2)
    return fig


def elbow_figure(k_values, wcss):
    fig, ax = plt.subplots(figsize=(8, 4.6))
    ax.plot(k_values, wcss, marker="o", color="#0f766e")
    ax.set_title("Elbow Method")
    ax.set_xlabel("Number of Clusters (K)")
    ax.set_ylabel("WCSS")
    ax.grid(alpha=0.25)
    return fig


def pca_cluster_figure(components, labels, pca):
    fig, ax = plt.subplots(figsize=(8, 5.2))
    scatter = ax.scatter(
        components[:, 0],
        components[:, 1],
        c=labels,
        cmap="viridis",
        alpha=0.55,
        s=22,
    )
    ax.set_title("PCA Projection with K-Means Clusters")
    ax.set_xlabel(f"PC1 ({pca.explained_variance_ratio_[0] * 100:.1f}% var)")
    ax.set_ylabel(f"PC2 ({pca.explained_variance_ratio_[1] * 100:.1f}% var)")
    ax.grid(alpha=0.2)
    legend = ax.legend(*scatter.legend_elements(), title="Cluster")
    ax.add_artist(legend)
    return fig


def monthly_spending_figure(monthly):
    fig, ax = plt.subplots(figsize=(8.5, 4.8))
    ax.plot(monthly["year_month"], monthly["amount"], marker="o", color="#0ea5a4")
    ax.set_title("Monthly Spending Trend")
    ax.set_xlabel("Month")
    ax.set_ylabel("Total Amount")
    ax.tick_params(axis="x", labelrotation=60)
    ax.grid(alpha=0.2)
    return fig


def category_spending_figure(category_frame):
    fig, ax = plt.subplots(figsize=(8.5, 4.8))
    ax.bar(category_frame["category"], category_frame["amount"], color="#f59e0b")
    ax.set_title("Top Category-wise Spending")
    ax.set_xlabel("Category")
    ax.set_ylabel("Total Amount")
    ax.tick_params(axis="x", labelrotation=45)
    ax.grid(alpha=0.2, axis="y")
    return fig
