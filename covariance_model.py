import numpy as np
from sklearn.metrics import confusion_matrix, roc_auc_score, roc_curve


def covariance_parameters(X_group, regularization=1e-5):
    mean = X_group.mean(axis=0)
    covariance = np.cov(X_group, rowvar=False)
    covariance_reg = covariance + regularization * np.eye(covariance.shape[0])
    sign, logdet = np.linalg.slogdet(covariance_reg)
    if sign <= 0:
        raise ValueError("Regularized covariance matrix is not positive definite.")
    return mean, covariance, covariance_reg, logdet


def mahalanobis_squared(X, mean, covariance_reg):
    delta = X - mean
    solved = np.linalg.solve(covariance_reg, delta.T).T
    return np.einsum("ij,ij->i", delta, solved)


def pattern_matching_score(
    X,
    y,
    regularization=1e-5,
):
    X_ref = X[y == 0]
    X_mal = X[y == 1]
    mu_ref, sigma_ref, sigma_ref_reg, logdet_ref = covariance_parameters(
        X_ref, regularization
    )
    mu_mal, sigma_mal, sigma_mal_reg, logdet_mal = covariance_parameters(
        X_mal, regularization
    )

    d_ref = mahalanobis_squared(X, mu_ref, sigma_ref_reg)
    d_mal = mahalanobis_squared(X, mu_mal, sigma_mal_reg)
    score = (d_ref + logdet_ref) - (d_mal + logdet_mal)

    auc = roc_auc_score(y, score)
    fpr, tpr, thresholds = roc_curve(y, score)
    youden = tpr - fpr
    idx = int(np.argmax(youden))
    threshold = thresholds[idx]
    prediction = (score >= threshold).astype(int)
    tn, fp, fn, tp = confusion_matrix(y, prediction, labels=[0, 1]).ravel()

    metrics = {
        "auc": float(auc),
        "youden_j": float(youden[idx]),
        "threshold": float(threshold),
        "sensitivity": float(tp / (tp + fn)),
        "specificity": float(tn / (tn + fp)),
        "precision": float(tp / (tp + fp)) if (tp + fp) else np.nan,
        "tn": int(tn),
        "fp": int(fp),
        "fn": int(fn),
        "tp": int(tp),
    }

    return {
        "score": score,
        "prediction": prediction,
        "metrics": metrics,
        "reference": {
            "mean": mu_ref,
            "covariance": sigma_ref,
            "covariance_reg": sigma_ref_reg,
            "logdet": logdet_ref,
        },
        "malnourished": {
            "mean": mu_mal,
            "covariance": sigma_mal,
            "covariance_reg": sigma_mal_reg,
            "logdet": logdet_mal,
        },
        "distance_reference": d_ref,
        "distance_malnourished": d_mal,
    }
