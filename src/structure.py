import numpy as np


def covariance_eigenstructure(X_group):
    covariance = np.cov(X_group, rowvar=False)
    eigenvalues, eigenvectors = np.linalg.eigh(covariance)
    order = np.argsort(eigenvalues)
    return covariance, eigenvalues[order], eigenvectors[:, order]


def eigenvalue_summary(X_reference, X_malnourished, features, k=5):
    _, eig_ref, vec_ref = covariance_eigenstructure(X_reference)
    _, eig_mal, _ = covariance_eigenstructure(X_malnourished)

    low_ratio = eig_mal[:k] / eig_ref[:k]
    high_ratio = eig_mal[-k:] / eig_ref[-k:]

    rows = []
    for i in range(k):
        vector = vec_ref[:, i]
        top = np.argsort(np.abs(vector))[-5:][::-1]
        rows.append(
            {
                "axis": i + 1,
                "reference_eigenvalue": eig_ref[i],
                "malnourished_eigenvalue": eig_mal[i],
                "expansion_ratio": low_ratio[i],
                "top_features": [features[j] for j in top],
            }
        )

    return {
        "reference_eigenvalues": eig_ref,
        "malnourished_eigenvalues": eig_mal,
        "reference_eigenvectors": vec_ref,
        "low_variance_ratio": low_ratio,
        "high_variance_ratio": high_ratio,
        "low_variance_axes": rows,
    }
