import numpy as np
from scipy.stats import chi2, norm


def healthy_reference_probability(X, X_reference, regularization=1e-5, k=5):
    """Quantify deviations from the reference group's covariance structure."""
    mean = X_reference.mean(axis=0)
    covariance = np.cov(X_reference, rowvar=False)
    covariance_reg = covariance + regularization * np.eye(covariance.shape[0])

    eigenvalues, eigenvectors = np.linalg.eigh(covariance_reg)
    order = np.argsort(eigenvalues)
    eigenvalues = eigenvalues[order]
    eigenvectors = eigenvectors[:, order]

    centered = X - mean
    projections = centered @ eigenvectors
    z = projections / np.sqrt(eigenvalues)
    axis_p = 2 * norm.sf(np.abs(z))
    violations = (np.abs(z[:, :k]) > 2).sum(axis=1)

    inv = np.linalg.inv(covariance_reg)
    mahalanobis = np.einsum("ij,ij->i", centered, centered @ inv.T)
    global_p = chi2.sf(mahalanobis, df=X.shape[1])

    return {
        "eigenvalues": eigenvalues,
        "eigenvectors": eigenvectors,
        "z": z,
        "axis_p": axis_p,
        "violations_low_variance": violations,
        "mahalanobis_squared": mahalanobis,
        "global_p": global_p,
    }
