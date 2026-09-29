import argparse
from pathlib import Path

import pandas as pd

from src.config import FEATURES
from src.data import get_ordinal_labels, load_dataset, prepare_matrix
from src.trajectory import trajectory_summary


def main():
    parser = argparse.ArgumentParser(
        description="Quantify magnitude and angular divergence of the SGA A -> B -> C trajectory."
    )
    parser.add_argument("data")
    parser.add_argument("--label-column", default="SGA_ordinal")
    parser.add_argument("--output", default="results/trajectory_analysis.csv")
    args = parser.parse_args()

    df = load_dataset(args.data)
    labels = get_ordinal_labels(df, args.label_column)
    X, _, _ = prepare_matrix(df, FEATURES)

    summary = trajectory_summary(X, labels)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)

    row = {
        key: value
        for key, value in summary.items()
        if not key.startswith("centroid_")
    }
    pd.DataFrame([row]).to_csv(output, index=False)

    print(f"Trajectory analysis written to {output}")
    print(f"A -> B distance: {summary['distance_A_B']:.3f}")
    print(f"B -> C distance: {summary['distance_B_C']:.3f}")
    print(f"A -> C distance: {summary['distance_A_C']:.3f}")
    print(f"Angle A -> B vs B -> C: {summary['angle_AB_BC_degrees']:.2f} degrees")


if __name__ == "__main__":
    main()
