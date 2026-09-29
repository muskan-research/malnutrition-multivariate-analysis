import argparse
from pathlib import Path

import pandas as pd

from src.config import FEATURES, N_PERMUTATIONS, RANDOM_SEED
from src.data import get_binary_labels, load_dataset, prepare_matrix
from src.statistics import permutation_pairwise_distance


def main():
    parser = argparse.ArgumentParser(description="Permutation test for within-group multivariate heterogeneity.")
    parser.add_argument("data")
    parser.add_argument("--label-column", default="SGA_binary")
    parser.add_argument("--output", default="results/pairwise_distance_permutation.csv")
    parser.add_argument("--n-permutations", type=int, default=N_PERMUTATIONS)
    parser.add_argument("--seed", type=int, default=RANDOM_SEED)
    args = parser.parse_args()

    df = load_dataset(args.data)
    y = get_binary_labels(df, args.label_column)
    X, _, _ = prepare_matrix(df, FEATURES)

    result = permutation_pairwise_distance(
        X, y, n_permutations=args.n_permutations, seed=args.seed
    )

    summary = pd.DataFrame(
        [{
            "observed_reference": result["observed_reference"],
            "observed_malnourished": result["observed_malnourished"],
            "observed_difference": result["observed_difference"],
            "null_mean": result["null_distribution"].mean(),
            "null_sd": result["null_distribution"].std(ddof=1),
            "null_q025": pd.Series(result["null_distribution"]).quantile(0.025),
            "null_q975": pd.Series(result["null_distribution"]).quantile(0.975),
            "p_permutation": result["p_permutation"],
        }]
    )

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    summary.to_csv(output, index=False)
    print(summary.T.to_string(header=False))
    print(f"\nSaved to {output}")


if __name__ == "__main__":
    main()
