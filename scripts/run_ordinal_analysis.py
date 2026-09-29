import argparse
from pathlib import Path

import pandas as pd
from scipy.stats import kruskal, spearmanr

from src.config import FEATURES, REGULARIZATION
from src.covariance_model import pattern_matching_score
from src.data import get_ordinal_labels, load_dataset, prepare_matrix


def main():
    parser = argparse.ArgumentParser(description="Relate the continuous model score to ordinal SGA category.")
    parser.add_argument("data")
    parser.add_argument("--ordinal-column", default="SGA_ordinal")
    parser.add_argument("--binary-column", default="SGA_binary")
    parser.add_argument("--output", default="results/ordinal_analysis.csv")
    args = parser.parse_args()

    df = load_dataset(args.data)
    y_binary = pd.to_numeric(df[args.binary_column], errors="raise").to_numpy().astype(int)
    y_ordinal = get_ordinal_labels(df, args.ordinal_column)
    X, _, _ = prepare_matrix(df, FEATURES)

    result = pattern_matching_score(X, y_binary, regularization=REGULARIZATION)
    rho, rho_p = spearmanr(result["score"], y_ordinal)
    groups = [result["score"][y_ordinal == group] for group in [0, 1, 2]]
    H, kw_p = kruskal(*groups)

    output = pd.DataFrame([{
        "spearman_rho": rho,
        "spearman_p": rho_p,
        "kruskal_H": H,
        "kruskal_p": kw_p,
        "median_SGA_A": pd.Series(groups[0]).median(),
        "median_SGA_B": pd.Series(groups[1]).median(),
        "median_SGA_C": pd.Series(groups[2]).median(),
    }])
    path = Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    output.to_csv(path, index=False)
    print(output.T.to_string(header=False))
    print(f"\nSaved to {path}")


if __name__ == "__main__":
    main()
