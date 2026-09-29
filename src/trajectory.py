import numpy as np


def group_centroids(X, labels):
    """Return mean standardized biomarker profiles for ordered groups A, B, C."""
    labels = np.asarray(labels)
    centroids = {}
    for label in (0, 1, 2):
        mask = labels == label
        if not np.any(mask):
            raise ValueError(f"SGA group {label} is absent from the supplied dataset.")
        centroids[label] = X[mask].mean(axis=0)
    return centroids


def euclidean_distance(a, b):
    """Straight-line distance between two multivariate states."""
    return float(np.linalg.norm(np.asarray(a) - np.asarray(b)))


def cosine_angle_degrees(a, b):
    """Angle in degrees between two non-zero vectors."""
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0:
        raise ValueError("Cosine angle is undefined for a zero-length vector.")
    cosine = np.dot(a, b) / (norm_a * norm_b)
    cosine = np.clip(cosine, -1.0, 1.0)
    return float(np.degrees(np.arccos(cosine)))


def trajectory_summary(X, labels):
    """Summarise magnitude and direction of the A -> B -> C centroid trajectory."""
    centroids = group_centroids(X, labels)

    a = centroids[0]
    b = centroids[1]
    c = centroids[2]

    v_ab = b - a
    v_bc = c - b
    v_ac = c - a

    return {
        "centroid_A": a,
        "centroid_B": b,
        "centroid_C": c,
        "distance_A_B": euclidean_distance(a, b),
        "distance_B_C": euclidean_distance(b, c),
        "distance_A_C": euclidean_distance(a, c),
        "angle_AB_BC_degrees": cosine_angle_degrees(v_ab, v_bc),
        "angle_AB_AC_degrees": cosine_angle_degrees(v_ab, v_ac),
        "cosine_AB_BC": float(np.cos(np.radians(cosine_angle_degrees(v_ab, v_bc)))),
        "cosine_AB_AC": float(np.cos(np.radians(cosine_angle_degrees(v_ab, v_ac)))),
    }
