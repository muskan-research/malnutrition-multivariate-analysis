# Analysis map

The repository is organised into reusable functions in `src/` and executable analyses in `scripts/`.

## Primary analysis

`scripts/run_main_analysis.py` runs the covariance pattern-matching analysis. It estimates reference and malnourished covariance structures and evaluates the resulting continuous score using ROC/AUC, Youden's J, sensitivity, specificity, precision, and a confusion matrix.

Core calculations are implemented in `src/covariance_model.py`.

## Covariance structure

`scripts/run_structure_analysis.py` uses `src/structure.py` to decompose group covariance matrices into eigenvalues and eigenvectors and summarise low- and high-variance axes.

## Reference-structure probability

`scripts/run_reference_probability.py` uses `src/reference_probability.py` to project observations into the reference covariance eigenbasis and calculate axis-wise and global probabilities under the reference covariance model.

## Ordinal SGA analysis

`scripts/run_ordinal_analysis.py` relates the continuous model score to ordinal SGA categories using Spearman correlation and the Kruskal–Wallis test.

## Sensitivity analysis

`scripts/run_clinical_midpoint_sensitivity.py` compares distances from the reference-group centre with distances from clinical reference-range midpoints. Sex-specific ranges are handled by the midpoint function in `src/config.py`.

## Permutation analysis

`scripts/run_permutation_tests.py` tests whether the observed difference in mean within-group multivariate pairwise distance is unusual under permutation of group labels.

## Figures

`scripts/make_figures.py` generates figures for multivariate distance from the reference-group centre and covariance eigenvalue structure.

## Data flow

```text
Private clinical dataset
        |
        v
src/data.py
  numeric coercion
  median imputation
  standardisation
        |
        +----------------------+
        |                      |
        v                      v
src/covariance_model.py   src/structure.py
        |                      |
        v                      v
model score / ROC        eigenstructure
        |
        +----------------------+
        |
        v
additional sensitivity,
ordinal, probability,
and permutation analyses
```
