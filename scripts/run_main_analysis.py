import argparse
from pathlib import Path

import pandas as pd

from src.config import FEATURES, REGULARIZATION
from src.covariance_model import pattern_matching_score
from src.data import get_binary_labels, load_dataset, prepare_matrix


def main():
    parser = argparse.ArgumentParser(description="Run the covariance pattern matching analysis.")
    parser.add_argument("data", help="Path to the private analysis dataset (.csv or .xlsx).")
    parser.add_argument("--label-column", default="SGA_binary")
    parser.add_argument("--output", default="results/main_model_metrics.csv")
    args = parser.parse_args()

    df = load_dataset(args.data)
    y = get_binary_labels(df, args.label_column)
    X, _, _ = prepare_matrix(df, FEATURES)

    result = pattern_matching_score(X, y, regularization=REGULARIZATION)
    metrics = pd.DataFrame([result["metrics"]])

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    metrics.to_csv(output, index=False)

    print(metrics.T.to_string(header=False))
    print(f"\nSaved metrics to {output}")


if __name__ == "__main__":
    main()
