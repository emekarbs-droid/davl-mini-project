import pandas as pd
import io
from services.data_utils import clean_dataset
from routers.analyze import get_summary
from app_state import state
import numpy as np

# load the file
df = pd.read_csv('cars.csv', encoding='windows-1252')
state.df = df

print("Columns:", df.columns)
numeric_df = clean_dataset(df).select_dtypes(include=[np.number])
print("Numeric columns:", numeric_df.columns)

try:
    res = get_summary()
    print("Analyze success!")
except Exception as e:
    import traceback
    traceback.print_exc()

# Let's test pca and clustering
from routers.pca import get_pca
from routers.clustering import train_kmeans, ClusteringRequest
try:
    print("Testing PCA...")
    res_pca = get_pca()
    print("PCA success!")
    
    print("Testing Clustering...")
    req_clus = ClusteringRequest(n_clusters=3)
    res_clus = train_kmeans(req_clus)
    print("Clustering success!")
except Exception as e:
    import traceback
    traceback.print_exc()
except Exception as e:
    import traceback
    traceback.print_exc()
