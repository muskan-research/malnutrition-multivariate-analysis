import argparse
from pathlib import Path

import pandas as pd

from src.config import FEATURES, N_LOW_VARIANCE_AXES
from src.data import get_binary_labels, load_dataset, prepare_matrix
from src.structure import eigenvalue_summary


def main():
    parser = argparse.ArgumentParser(description="Summarize covariance eigenstructure by group.")
    parser.add_argument("data")
    parser.add_argument("--label-column", default="SGA_binary")
    parser.add_argument("--output", default="results/eigenstructure.csv")
    args = parser.parse_args()

    df = load_dataset(args.data)
    y = get_binary_labels(df, args.label_column)
    X, _, _ = prepare_matrix(df, FEATURES)

    summary = eigenvalue_summary(
        X[y == 0], X[y == 1], FEATURES, k=N_LOW_VARIANCE_AXES
    )

    rows = []
    for row in summary["low_variance_axes"]:
        rows.append(
            {
                "axis": row["axis"],
                "reference_eigenvalue": row["reference_eigenvalue"],
                "malnourished_eigenvalue": row["malnourished_eigenvalue"],
                "expansion_ratio": row["expansion_ratio"],
                "top_features": "; ".join(row["top_features"]),
            }
        )

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(output, index=False)
    print(pd.DataFrame(rows).to_string(index=False))
    print(f"\nLow-variance expansion range: {summary['low_variance_ratio'].min():.3f}–{summary['low_variance_ratio'].max():.3f}")
    print(f"High-variance expansion range: {summary['high_variance_ratio'].min():.3f}–{summary['high_variance_ratio'].max():.3f}")


if __name__ == "__main__":
    main()
