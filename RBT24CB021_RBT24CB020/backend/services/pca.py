import pandas as pd
from sklearn.decomposition import PCA
import plotly.express as px
import plotly.graph_objects as go
import json

def perform_pca(df_scaled: pd.DataFrame) -> dict:
    try:
        pca = PCA()
        components = pca.fit_transform(df_scaled)
        
        explained_variance = pca.explained_variance_ratio_ * 100
        
        # Scree plot
        fig_scree = px.bar(
            x=[f"PC{i+1}" for i in range(len(explained_variance))],
            y=explained_variance,
            labels={"x": "Principal Components", "y": "Explained Variance (%)"},
            title="Scree Plot (Explained Variance)"
        )
        
        # 2D Scatter plot (if at least 2 components)
        if components.shape[1] >= 2:
            df_pca = pd.DataFrame(data=components[:, :2], columns=['PC1', 'PC2'])
            fig_scatter = px.scatter(df_pca, x="PC1", y="PC2", title="PCA - 2D Scatter Plot")
        else:
            fig_scatter = go.Figure()
            
        return {
            "explained_variance": json.loads(fig_scree.to_json()),
            "scatter_plot": json.loads(fig_scatter.to_json())
        }
    except Exception as e:
        return {"error": str(e)}
