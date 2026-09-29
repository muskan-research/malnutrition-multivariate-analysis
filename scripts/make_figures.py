import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from src.config import FEATURES
from src.data import get_binary_labels, load_dataset, prepare_matrix
from src.structure import covariance_eigenstructure


def main():
    parser = argparse.ArgumentParser(description="Generate the two main analysis figures.")
    parser.add_argument("data")
    parser.add_argument("--label-column", default="SGA_binary")
    parser.add_argument("--output-dir", default="results/figures")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    df = load_dataset(args.data)
    y = get_binary_labels(df, args.label_column)
    X, _, _ = prepare_matrix(df, FEATURES)

    ref = X[y == 0]
    mal = X[y == 1]
    reference_center = ref.mean(axis=0)
    distances = np.linalg.norm(X - reference_center, axis=1)

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.boxplot([distances[y == 0], distances[y == 1]], showfliers=False)
    ax.set_xticks([1, 2], ["Reference", "Malnourished"])
    ax.set_ylabel("Distance from reference-group centre")
    ax.set_title("Multivariate distance from the reference state")
    fig.tight_layout()
    fig.savefig(output_dir / "multivariate_distance.png", dpi=300)
    plt.close(fig)

    _, eig_ref, _ = covariance_eigenstructure(ref)
    _, eig_mal, _ = covariance_eigenstructure(mal)
    order = np.argsort(eig_ref)
    eig_ref = eig_ref[order]
    eig_mal = eig_mal[order]
    axes = np.arange(1, len(eig_ref) + 1)

    fig, ax = plt.subplots(figsize=(7, 5))
    for i in range(len(axes)):
        ax.plot([eig_ref[i], eig_mal[i]], [axes[i], axes[i]], linewidth=1)
    ax.scatter(eig_ref, axes, s=25, label="Reference")
    ax.scatter(eig_mal, axes, s=25, label="Malnourished")
    ax.set_xscale("log")
    ax.set_xlabel("Eigenvalue (log scale)")
    ax.set_ylabel("Principal axis")
    ax.set_title("Covariance eigenvalues by principal axis")
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(output_dir / "covariance_eigenvalues.png", dpi=300)
    plt.close(fig)

    print(f"Figures written to {output_dir}")


if __name__ == "__main__":
    main()
