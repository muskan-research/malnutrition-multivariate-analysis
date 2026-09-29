import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import mannwhitneyu

from src.config import FEATURES, clinical_midpoints
from src.data import get_binary_labels, load_dataset, prepare_matrix


def main():
    parser = argparse.ArgumentParser(description="Compare a reference-group centre with clinical reference-range midpoint.")
    parser.add_argument("data")
    parser.add_argument("--label-column", default="SGA_binary")
    parser.add_argument("--output", default="results/clinical_midpoint_sensitivity.csv")
    args = parser.parse_args()

    df = load_dataset(args.data)
    y = get_binary_labels(df, args.label_column)
    X, _, scaler = prepare_matrix(df, FEATURES)

    reference_center = X[y == 0].mean(axis=0)
    distance_reference = np.linalg.norm(X - reference_center, axis=1)

    midpoint_raw = np.asarray(clinical_midpoints(FEATURES), dtype=float)
    midpoint_std = scaler.transform(midpoint_raw.reshape(1, -1))[0]
    distance_midpoint = np.linalg.norm(X - midpoint_std, axis=1)

    reference_a = distance_midpoint[y == 0]
    mal_b_c = distance_midpoint[y == 1]
    U, p = mannwhitneyu(mal_b_c, reference_a, alternative="two-sided")

    result = pd.DataFrame([{
        "reference_mean_distance": distance_reference[y == 0].mean(),
        "malnourished_mean_distance": distance_reference[y == 1].mean(),
        "clinical_midpoint_reference_mean": reference_a.mean(),
        "clinical_midpoint_malnourished_mean": mal_b_c.mean(),
        "clinical_midpoint_reference_median": np.median(reference_a),
        "clinical_midpoint_malnourished_median": np.median(mal_b_c),
        "mean_increase_percent": ((mal_b_c.mean() - reference_a.mean()) / reference_a.mean()) * 100,
        "mann_whitney_U": U,
        "mann_whitney_p": p,
    }])

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(output, index=False)
    print(result.T.to_string(header=False))
    print(f"\nSaved to {output}")


if __name__ == "__main__":
    main()
