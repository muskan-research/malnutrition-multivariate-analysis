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


def fit_covariance_models(X, y, regularization=1e-5):
    """Fit the two covariance models used by the pattern-matching score."""
    X_reference = X[y == 0]
    X_malnourished = X[y == 1]

    reference = covariance_parameters(X_reference, regularization)
    malnourished = covariance_parameters(X_malnourished, regularization)

    return {
        "reference": {
            "mean": reference[0],
            "covariance": reference[1],
            "covariance_reg": reference[2],
            "logdet": reference[3],
        },
        "malnourished": {
            "mean": malnourished[0],
            "covariance": malnourished[1],
            "covariance_reg": malnourished[2],
            "logdet": malnourished[3],
        },
    }


def mahalanobis_squared(X, mean, covariance_reg):
    delta = X - mean
    solved = np.linalg.solve(covariance_reg, delta.T).T
    return np.einsum("ij,ij->i", delta, solved)


def covariance_score(X, models):
    """Score observations against already-fitted covariance models."""
    reference = models["reference"]
    malnourished = models["malnourished"]

    d_reference = mahalanobis_squared(
        X, reference["mean"], reference["covariance_reg"]
    )
    d_malnourished = mahalanobis_squared(
        X, malnourished["mean"], malnourished["covariance_reg"]
    )

    score = (
        d_reference
        + reference["logdet"]
        - d_malnourished
        - malnourished["logdet"]
    )

    return {
        "score": score,
        "distance_reference": d_reference,
        "distance_malnourished": d_malnourished,
        "models": models,
    }


def evaluate_binary_score(y, score, threshold=None):
    """Evaluate a score, fitting a Youden threshold only when requested."""
    y = np.asarray(y, dtype=int)
    score = np.asarray(score, dtype=float)

    auc = roc_auc_score(y, score)
    fpr, tpr, thresholds = roc_curve(y, score)

    if threshold is None:
        youden = tpr - fpr
        idx = int(np.argmax(youden))
        threshold = float(thresholds[idx])
        youden_j = float(youden[idx])
    else:
        youden_j = float("nan")

    prediction = (score >= threshold).astype(int)
    tn, fp, fn, tp = confusion_matrix(y, prediction, labels=[0, 1]).ravel()

    metrics = {
        "auc": float(auc),
        "youden_j": youden_j,
        "threshold": float(threshold),
        "sensitivity": float(tp / (tp + fn)) if (tp + fn) else np.nan,
        "specificity": float(tn / (tn + fp)) if (tn + fp) else np.nan,
        "precision": float(tp / (tp + fp)) if (tp + fp) else np.nan,
        "tn": int(tn),
        "fp": int(fp),
        "fn": int(fn),
        "tp": int(tp),
    }
    return metrics


def pattern_matching_score(X, y, regularization=1e-5):
    """Fit the covariance score and evaluate it on the same supplied cohort."""
    models = fit_covariance_models(X, y, regularization=regularization)
    scored = covariance_score(X, models)
    metrics = evaluate_binary_score(y, scored["score"])

    return {
        **scored,
        "prediction": (
            scored["score"] >= metrics["threshold"]
        ).astype(int),
        "metrics": metrics,
    }
