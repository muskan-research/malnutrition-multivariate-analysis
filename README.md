# Multivariate Biomarker Analysis of Malnutrition

Python code accompanying a research project investigating whether disease-related malnutrition is associated with changes in the joint structure of routine clinical biomarkers.

The repository contains the cleaned analytical code and documentation. The original patient-level clinical dataset is private and is not included.

## Research question

The project examines malnutrition as a multivariate physiological state. The analysis focuses on:

- distance from a reference physiological state;
- differences in covariance structure between reference and malnourished groups;
- changes in low- and high-variance directions of the biomarker space;
- deviation from the reference covariance structure; and
- sensitivity and permutation analyses.

The approach is exploratory and research-oriented. It is **not a clinical diagnostic tool**.

## Repository structure

```text
.
├── README.md
├── requirements.txt
├── src/
│   ├── config.py
│   ├── data.py
│   ├── covariance_model.py
│   ├── reference_probability.py
│   ├── statistics.py
│   └── structure.py
├── scripts/
│   ├── run_main_analysis.py
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
│   └── publication_notes.md
└── results/
    └── README.md
```

## Data

No patient-level clinical data are included.

The file `data/example_synthetic.csv` is simulated data provided only for demonstration and testing. It should not be interpreted as observations from the clinical cohort.

For an analysis using the study dataset, provide the private CSV or Excel file locally when running the scripts. The expected biomarker and SGA columns are checked by the data-loading functions.

## Setup

Python 3.10+ is recommended.

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the analyses

From the repository root:

```bash
python -m scripts.run_main_analysis /path/to/private_dataset.xlsx
python -m scripts.run_structure_analysis /path/to/private_dataset.xlsx
python -m scripts.run_reference_probability /path/to/private_dataset.xlsx
python -m scripts.run_ordinal_analysis /path/to/private_dataset.xlsx
python -m scripts.run_clinical_midpoint_sensitivity /path/to/private_dataset.xlsx
python -m scripts.run_permutation_tests /path/to/private_dataset.xlsx
python -m scripts.make_figures /path/to/private_dataset.xlsx
```

Each script accepts command-line arguments for label columns and output locations where applicable.

## Analytical components

**Covariance pattern matching**  
Compares observations with the covariance structures estimated for the reference and malnourished groups and evaluates the resulting continuous score using ROC-based measures.

**Covariance eigenstructure**  
Examines eigenvalues and eigenvectors to describe differences in the organisation and variability of the multivariate biomarker space.

**Reference-structure probability**  
Projects observations into the reference covariance eigenbasis and quantifies deviations along low-variance directions and globally.

**Ordinal analysis**  
Examines the relationship between the continuous model score and ordinal SGA categories.

**Sensitivity analysis**  
Compares distances from the reference-group centre with distances from clinical reference-range midpoints.

**Permutation analysis**  
Tests whether the observed difference in within-group multivariate pairwise distance is unusual under permutation of group labels.

Further details are provided in [the analysis map](docs/analysis_map.md).

## Reproducibility and interpretation

The repository separates reusable analytical functions in `src/` from executable analysis scripts in `scripts/`.

The current implementation includes exploratory analyses in which preprocessing and model parameters can be estimated from the supplied cohort. Performance estimates from fitting and evaluating on the same cohort can therefore be optimistic. Results from an independent validation cohort should be treated separately from exploratory performance estimates.

Randomized permutation analyses expose their seed and number of permutations as command-line arguments.

Generated tables and figures are written to `results/`. Patient-level outputs should remain local unless they have been appropriately de-identified and are approved for release.

## Research status

This repository is a public code release accompanying ongoing research. Manuscript details and a formal citation will be added when finalised.

## Author

**Muskan**  
MSc Health Sciences (Clinical Nutrition), University of Tartu
