import argparse
from pathlib import Path

import pandas as pd

from src.config import FEATURES
from src.data import get_binary_labels, load_dataset, prepare_matrix
from src.drift import mean_pairwise_distance, reference_distances


def main():
    parser = argparse.ArgumentParser(
        description="Quantify multivariate drift and within-group dispersion."
    )
    parser.add_argument("data")
    parser.add_argument("--label-column", default="SGA_binary")
    parser.add_argument("--output", default="results/drift_analysis.csv")
    args = parser.parse_args()

    df = load_dataset(args.data)
    y = get_binary_labels(df, args.label_column)
    X, _, _ = prepare_matrix(df, FEATURES)

    distances, _ = reference_distances(X, y, reference_label=0)

    rows = []
    for label, name in ((0, "reference"), (1, "malnourished")):
        group = distances[y == label]
        rows.append(
            {
                "group": name,
                "n": int(group.size),
                "mean_reference_distance": float(group.mean()),
                "median_reference_distance": float(pd.Series(group).median()),
                "mean_pairwise_distance": mean_pairwise_distance(X[y == label]),
            }
        )

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(output, index=False)
    print(pd.DataFrame(rows).to_string(index=False))
    print(f"\nSaved to {output}")


if __name__ == "__main__":
    main()
