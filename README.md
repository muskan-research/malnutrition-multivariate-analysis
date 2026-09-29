# Multivariate Biomarker Analysis of Malnutrition

[![Reproducibility check](https://github.com/muskan-research/malnutrition-multivariate-analysis/actions/workflows/reproducibility.yml/badge.svg)](https://github.com/muskan-research/malnutrition-multivariate-analysis/actions/workflows/reproducibility.yml)

Python implementation of the multivariate analyses developed for a study of disease-related malnutrition using routine clinical biomarkers.

The public repository contains the analysis code, documentation, and a synthetic example dataset. The patient-level clinical data are not included.

## What the analysis asks

The project treats nutritional status as a multivariate physiological configuration rather than a collection of isolated biomarker abnormalities.

The analysis separates four related questions:

1. **Magnitude** — how far is an individual or group from the SGA-A reference state?
2. **Direction** — do the multivariate changes between SGA A, B, and C point in the same direction?
3. **Structure** — how do covariance and variance patterns differ between reference and malnourished groups?
4. **Classification** — how well does the covariance-based score distinguish the two binary SGA groups, and how does it behave in held-out data?

## Repository structure

```text
.
├── README.md
├── requirements.txt
├── .github/
│   └── workflows/
│       └── reproducibility.yml
├── src/
│   ├── config.py
│   ├── covariance_model.py
│   ├── data.py
│   ├── drift.py
│   ├── reference_probability.py
│   ├── statistics.py
│   ├── structure.py
│   └── trajectory.py
├── scripts/
│   ├── run_drift_analysis.py
│   ├── run_main_analysis.py
│   ├── run_validation_analysis.py
│   ├── run_trajectory_analysis.py
│   ├── run_structure_analysis.py
│   ├── run_reference_probability.py
│   ├── run_ordinal_analysis.py
│   ├── run_clinical_midpoint_sensitivity.py
│   ├── run_permutation_tests.py
│   └── make_figures.py
├── data/
│   ├── README.md
│   └── example_synthetic.csv
├── docs/
│   ├── analysis_map.md
│   ├── publication_notes.md
│   └── validation.md
└── results/
    └── README.md
```

## Data and preprocessing

The analysis uses a fixed panel of 37 biomarkers defined in `src/config.py`.

For a supplied dataset, the workflow:

1. checks that all required biomarker columns are present;
2. converts biomarker values to numeric form;
3. imputes missing biomarker values with the cohort-specific median;
4. standardises the biomarker matrix with z-scores.

For independent validation, the imputer and scaler are fitted **only in the development cohort** and then applied unchanged to the validation cohort. See [Validation](docs/validation.md).

The public `data/example_synthetic.csv` file is simulated data for software testing and demonstration. It is not clinical data and should not be used for scientific inference.

## Main analyses

### Multivariate drift

The SGA-A centroid is used as the reference state. Euclidean distance quantifies the magnitude of displacement from that reference, while within-group pairwise Euclidean distance describes dispersion.

Run:

```bash
python -m scripts.run_drift_analysis /path/to/dataset.xlsx
```

### Geometric trajectory analysis

Centroid profiles are calculated for SGA A, B, and C. Euclidean transition lengths quantify the size of A→B, B→C, and A→C changes. Cosine similarity is used to calculate the angle between successive trajectory vectors.

This is a **cross-sectional centroid analysis**, not longitudinal tracking of individual patients.

Run:

```bash
python -m scripts.run_trajectory_analysis /path/to/dataset.xlsx
```

### Covariance-based model

The binary covariance model estimates separate covariance structures for the reference and malnourished groups and produces a continuous pattern-matching score. The exploratory threshold is selected with Youden's J.

Run:

```bash
python -m scripts.run_main_analysis /path/to/dataset.xlsx
```

### Held-out validation

The validation script keeps preprocessing, covariance estimation, and threshold selection in the development cohort. The resulting model and threshold are then applied unchanged to the held-out cohort.

Run:

```bash
python -m scripts.run_validation_analysis \
    /path/to/development_dataset.xlsx \
    /path/to/validation_dataset.xlsx
```

### Covariance structure and reference probability

The remaining modules examine covariance eigenstructure, deviation from the reference covariance model, and the relationship between the continuous score and ordinal SGA categories.

Permutation testing and a clinical-reference-midpoint sensitivity analysis are included as supporting analyses.

See [the analysis map](docs/analysis_map.md) for the full workflow.

## Reproducibility

The repository keeps reusable calculations in `src/` and command-line entry points in `scripts/`.

GitHub Actions runs the analysis scripts on the synthetic dataset after each push and pull request. The workflow checks that the code installs cleanly, the modules import correctly, and the principal analyses complete without error.

Results generated from private clinical data are written locally to `results/`; generated result files are ignored by Git by default.

## Interpretation

Exploratory performance estimates are obtained within the supplied cohort unless the held-out validation workflow is used. Same-cohort performance can be optimistic and should not be interpreted as independent validation.

The code is intended for research use. It is not a clinical diagnostic system.

## Research status

This repository contains the reproducible analysis code developed as part of an MSc research project in Clinical Nutrition at the University of Tartu. The associated manuscript is currently in preparation.

## Author

**Muskan**  
MSc Health Sciences (Clinical Nutrition)  
University of Tartu
