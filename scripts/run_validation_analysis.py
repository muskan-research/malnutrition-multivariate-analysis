import argparse
from pathlib import Path

import pandas as pd

from src.config import FEATURES, REGULARIZATION
from src.covariance_model import (
    evaluate_binary_score,
    fit_covariance_models,
    covariance_score,
)
from src.data import (
    fit_preprocessor,
    get_binary_labels,
    load_dataset,
    transform_matrix,
)


def main():
    parser = argparse.ArgumentParser(
        description="Evaluate the covariance model on a held-out cohort."
    )
    parser.add_argument("development_data")
    parser.add_argument("validation_data")
    parser.add_argument("--label-column", default="SGA_binary")
    parser.add_argument("--output", default="results/validation_performance.csv")
    args = parser.parse_args()

    development = load_dataset(args.development_data)
    validation = load_dataset(args.validation_data)

    y_development = get_binary_labels(development, args.label_column)
    y_validation = get_binary_labels(validation, args.label_column)

    imputer, scaler = fit_preprocessor(development, FEATURES)
    X_development = transform_matrix(
        development, FEATURES, imputer, scaler
    )
    X_validation = transform_matrix(
        validation, FEATURES, imputer, scaler
    )

    models = fit_covariance_models(
        X_development, y_development, regularization=REGULARIZATION
    )

    development_scored = covariance_score(X_development, models)
    validation_scored = covariance_score(X_validation, models)

    development_metrics = evaluate_binary_score(
        y_development, development_scored["score"]
    )
    validation_metrics = evaluate_binary_score(
        y_validation,
        validation_scored["score"],
        threshold=development_metrics["threshold"],
    )

    rows = []
    for cohort, metrics in (
        ("development", development_metrics),
        ("validation", validation_metrics),
    ):
        rows.append({"cohort": cohort, **metrics})

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(output, index=False)
    print(pd.DataFrame(rows).to_string(index=False))
    print(
        "\nValidation uses the preprocessing, covariance models, "
        "and classification threshold fitted in the development cohort."
    )
    print(f"Saved to {output}")


if __name__ == "__main__":
    main()
