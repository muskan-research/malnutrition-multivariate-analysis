import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from src.config import FEATURES, REGULARIZATION, N_LOW_VARIANCE_AXES
from src.data import get_binary_labels, load_dataset, prepare_matrix
from src.reference_probability import healthy_reference_probability


def main():
    parser = argparse.ArgumentParser(description="Quantify deviations from the reference covariance structure.")
    parser.add_argument("data")
    parser.add_argument("--label-column", default="SGA_binary")
    parser.add_argument("--output", default="results/reference_probability.csv")
    args = parser.parse_args()

    df = load_dataset(args.data)
    y = get_binary_labels(df, args.label_column)
    X, _, _ = prepare_matrix(df, FEATURES)
    ref = X[y == 0]

    result = healthy_reference_probability(
        X,
        X_reference=ref,
        regularization=REGULARIZATION,
        k=N_LOW_VARIANCE_AXES,
    )

    output_df = pd.DataFrame(
        {
            "global_p": result["global_p"],
            "low_variance_axis_violations": result["violations_low_variance"],
            "mahalanobis_squared": result["mahalanobis_squared"],
            "group": y,
        }
    )
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output_df.to_csv(output, index=False)
    print(output_df.groupby("group").agg({"global_p": "mean", "low_variance_axis_violations": "mean"}))
    print(f"\nSaved to {output}")


if __name__ == "__main__":
    main()
