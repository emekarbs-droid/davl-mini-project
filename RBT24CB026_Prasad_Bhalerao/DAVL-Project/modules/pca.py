from sklearn.decomposition import PCA


def project_to_2d(x_scaled):
    """
    Reduces the high-dimensional scaled features down to 2 Principal Components.
    This captures the most variance, enabling easy 2D visualization of our clusters.
    """
    pca = PCA(n_components=2, random_state=42)
    components = pca.fit_transform(x_scaled)
    return pca, components
