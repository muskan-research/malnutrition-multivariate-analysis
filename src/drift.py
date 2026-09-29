import numpy as np
from scipy.spatial.distance import pdist


def reference_distances(X, y, reference_label=0):
    """Return each observation's Euclidean distance from the reference centroid."""
    reference = X[y == reference_label]
    if reference.size == 0:
        raise ValueError(f"No observations found for reference label {reference_label}.")
    centroid = reference.mean(axis=0)
    distances = np.linalg.norm(X - centroid, axis=1)
    return distances, centroid


def mean_pairwise_distance(X_group):
    """Return the mean pairwise Euclidean distance within a group."""
    if len(X_group) < 2:
        raise ValueError("At least two observations are required for pairwise distance.")
    return float(np.mean(pdist(X_group, metric="euclidean")))
