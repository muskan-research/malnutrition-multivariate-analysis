import numpy as np
from scipy.spatial.distance import pdist
from scipy.stats import chi2, kruskal, mannwhitneyu, spearmanr



def mean_pairwise_distance(X_group):
    return float(np.mean(pdist(X_group, metric="euclidean")))


def permutation_pairwise_distance(
    X,
    y,
    n_permutations=1000,
    seed=12345,
):
    observed_ref = mean_pairwise_distance(X[y == 0])
    observed_mal = mean_pairwise_distance(X[y == 1])
    observed_difference = observed_mal - observed_ref

    rng = np.random.default_rng(seed)
    null = np.empty(n_permutations)
    for i in range(n_permutations):
        shuffled = rng.permutation(y)
        null[i] = (
            mean_pairwise_distance(X[shuffled == 1])
            - mean_pairwise_distance(X[shuffled == 0])
        )

    p = (np.sum(null >= observed_difference) + 1) / (n_permutations + 1)
    return {
        "observed_reference": observed_ref,
        "observed_malnourished": observed_mal,
        "observed_difference": observed_difference,
        "null_distribution": null,
        "p_permutation": float(p),
    }


def ordinal_score_test(score, ordinal_labels):
    rho, p = spearmanr(score, ordinal_labels)
    groups = [score[ordinal_labels == value] for value in np.unique(ordinal_labels)]
    H, p_kw = kruskal(*groups)
    medians = {int(v): float(np.median(score[ordinal_labels == v])) for v in np.unique(ordinal_labels)}
    return {
        "spearman_rho": float(rho),
        "spearman_p": float(p),
        "kruskal_H": float(H),
        "kruskal_p": float(p_kw),
        "group_medians": medians,
    }


def clinical_reference_distance_test(X, scaler, features, midpoint):
    midpoint_std = scaler.transform(np.asarray(midpoint).reshape(1, -1))[0]
    distances = np.linalg.norm(X - midpoint_std, axis=1)
    return distances
