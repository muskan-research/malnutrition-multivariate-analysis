# Multivariate Biomarker Analysis of Malnutrition

Python analysis code accompanying a research project investigating multivariate biomarker structure in relation to disease-related malnutrition.

The repository is organised around the analysis rather than the chronology of experimentation. Patient-level clinical data are not included.

## Research question

The analysis asks whether malnutrition is associated with a shift in the joint multivariate structure of routine clinical biomarkers, rather than only isolated abnormalities in individual biomarkers.

## Repository structure

```text
.
├── README.md
├── requirements.txt
├── src/
│   ├── config.py
│   ├── data.py
│   ├── covariance_model.py
│   ├── structure.py
│   ├── reference_probability.py
│   └── statistics.py
├── scripts/
│   ├── run_main_analysis.py
│   ├── run_structure_analysis.py
│   ├── run_reference_probability.py
│   ├── run_clinical_midpoint_sensitivity.py
│   ├── run_permutation_tests.py
│   └── make_figures.py
├── data/
│   └── README.md
├── results/
│   └── figures/
├── docs/
│   └── analysis_map.md
└── notebooks/
    └── README.md
```

## Data

The original patient dataset is private and is therefore excluded. See `data/README.md` for the expected input columns.

## Setup

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

## Running the analysis

Example:

```bash
python -m scripts.run_main_analysis /path/to/private_dataset.xlsx
python -m scripts.run_structure_analysis /path/to/private_dataset.xlsx
python -m scripts.run_reference_probability /path/to/private_dataset.xlsx
python -m scripts.run_clinical_midpoint_sensitivity /path/to/private_dataset.xlsx
python -m scripts.run_permutation_tests /path/to/private_dataset.xlsx
python -m scripts.make_figures /path/to/private_dataset.xlsx
```

## Reproducibility notes

The scripts preserve the main analytical logic of the original research code while separating reusable calculations from file handling and plotting. Randomized sensitivity analyses expose their seed and number of permutations as arguments.

The current exploratory implementation should not be interpreted as a clinical diagnostic tool. Performance estimates from analyses that fit and evaluate on the same cohort are subject to optimism and should be distinguished from performance in an independent validation cohort.

## Outputs

Generated tables and figures are written to `results/`. Patient-level output should remain local unless it has been de-identified and is explicitly approved for release.

## Citation

A citation file can be added once the manuscript and repository DOI are finalised.
