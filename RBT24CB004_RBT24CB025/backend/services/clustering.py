import pandas as pd
from sklearn.cluster import KMeans
import plotly.express as px
import json

def perform_clustering(df_scaled: pd.DataFrame) -> dict:
    try:
        # Elbow method
        inertias = []
        max_k = min(10, len(df_scaled) - 1)
        if max_k < 2:
            return {"error": "Not enough data points for clustering."}
            
        K_range = range(1, max_k + 1)
        
        for k in K_range:
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            kmeans.fit(df_scaled)
            inertias.append(kmeans.inertia_)
            
        fig_elbow = px.line(x=list(K_range), y=inertias, markers=True, 
                            labels={"x": "Number of Clusters (K)", "y": "Inertia"},
                            title="Elbow Method for Optimal K")
                            
        # Automatic K
        diffs = [inertias[i] - inertias[i+1] for i in range(len(inertias)-1)]
        optimal_k = 3
        if len(diffs) > 1:
            for i in range(1, len(diffs)):
                if diffs[i] < diffs[i-1] * 0.5: # 50% drop
                    optimal_k = i + 1
                    break
                    
        optimal_k = max(2, min(optimal_k, max_k))
        
        kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
        clusters = kmeans.fit_predict(df_scaled)
        
        if df_scaled.shape[1] > 2:
            from sklearn.decomposition import PCA
            pca = PCA(n_components=2)
            vis_data = pca.fit_transform(df_scaled)
            vis_df = pd.DataFrame(vis_data, columns=['Component 1', 'Component 2'])
            vis_df['Cluster'] = clusters.astype(str)
            fig_clusters = px.scatter(vis_df, x='Component 1', y='Component 2', color='Cluster', title=f"K-Means Clusters (K={optimal_k})")
        elif df_scaled.shape[1] == 2:
            vis_df = df_scaled.copy()
            vis_df.columns = ['Feature 1', 'Feature 2']
            vis_df['Cluster'] = clusters.astype(str)
            fig_clusters = px.scatter(vis_df, x='Feature 1', y='Feature 2', color='Cluster', title=f"K-Means Clusters (K={optimal_k})")
        else:
            vis_df = df_scaled.copy()
            vis_df.columns = ['Feature 1']
            vis_df['Cluster'] = clusters.astype(str)
            fig_clusters = px.scatter(vis_df, x='Feature 1', y=[0]*len(vis_df), color='Cluster', title=f"K-Means Clusters (K={optimal_k})")
            
        return {
            "optimal_k": optimal_k,
            "elbow_plot": json.loads(fig_elbow.to_json()),
            "cluster_plot": json.loads(fig_clusters.to_json())
        }
    except Exception as e:
        return {"error": str(e)}
