from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler


def load_dataset(path):
    """Load CSV or Excel input."""
    path = Path(path)
    if path.suffix.lower() in {".xlsx", ".xls"}:
        return pd.read_excel(path)
    if path.suffix.lower() == ".csv":
        return pd.read_csv(path)
    raise ValueError(f"Unsupported file format: {path.suffix}")


def prepare_matrix(df, features):
    """Coerce biomarkers to numeric, impute medians, and standardize."""
    missing = [f for f in features if f not in df.columns]
    if missing:
        raise ValueError(f"Missing biomarker columns: {missing}")

    raw = df[features].apply(pd.to_numeric, errors="coerce")
    imputer = SimpleImputer(strategy="median")
    scaler = StandardScaler()

    imputed = imputer.fit_transform(raw)
    standardized = scaler.fit_transform(imputed)
    return standardized, imputer, scaler


def get_binary_labels(df, column="SGA_binary"):
    if column not in df.columns:
        raise ValueError(
            f"Label column '{column}' is not present. "
            "Keep private labels in the local dataset rather than hard-coding them in scripts."
        )
    y = pd.to_numeric(df[column], errors="raise").to_numpy()
    if not np.isin(y, [0, 1]).all():
        raise ValueError(f"{column} must contain only 0/1 values.")
    return y.astype(int)


def get_ordinal_labels(df, column="SGA_ordinal"):
    if column not in df.columns:
        raise ValueError(f"Ordinal SGA column '{column}' is not present.")
    mapping = {"A": 0, "B": 1, "C": 2}
    values = df[column].astype(str).str.upper()
    if not values.isin(mapping).all():
        raise ValueError(f"{column} must contain only A, B, or C.")
    return values.map(mapping).to_numpy()
