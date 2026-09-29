# Analysis map

The repository is organised into reusable functions in `src/` and executable analyses in `scripts/`.

## 1. Multivariate preprocessing

`src/data.py` loads CSV/Excel data, validates the required biomarker columns, coerces biomarker values to numeric form, performs median imputation, and standardises the biomarker matrix.

The final biomarker panel is defined in `src/config.py`.

## 2. Multivariate drift

The reference state is the centroid of the SGA-A group.

`run_main_analysis.py` and `make_figures.py` calculate Euclidean distance from this reference centre. Pairwise Euclidean distances are also used to quantify within-group dispersion.

These measures describe **magnitude** of multivariate displacement.

## 3. Geometric trajectory analysis

`scripts/run_trajectory_analysis.py` uses `src/trajectory.py` to calculate centroid profiles for SGA A, B, and C.

For successive centroid vectors:

- A → B
- B → C
- A → C

the analysis calculates Euclidean transition lengths and cosine-derived angular relationships.

The key A → B versus B → C angle addresses whether the multivariate configuration changes in a directionally consistent way across SGA stages.

This is a cross-sectional centroid analysis, not longitudinal tracking of individual patients.

## 4. Covariance pattern matching

`scripts/run_main_analysis.py` estimates reference and malnourished covariance structures and evaluates a continuous covariance-based score using ROC/AUC, Youden's J, sensitivity, specificity, precision, and a confusion matrix.

Core calculations are implemented in `src/covariance_model.py`.

## 5. Covariance structure

`scripts/run_structure_analysis.py` uses `src/structure.py` to decompose group covariance matrices into eigenvalues and eigenvectors and summarise low- and high-variance axes.

## 6. Reference-structure probability

`scripts/run_reference_probability.py` uses `src/reference_probability.py` to project observations into the reference covariance eigenbasis and calculate axis-wise and global probabilities under the reference covariance model.

## 7. Ordinal SGA analysis

`scripts/run_ordinal_analysis.py` relates the continuous covariance-based model score to ordinal SGA categories using Spearman correlation and the Kruskal–Wallis test.

## 8. Sensitivity analysis

`scripts/run_clinical_midpoint_sensitivity.py` compares distances from the reference-group centre with distances from clinical reference-range midpoints. Sex-specific ranges are handled by the midpoint function in `src/config.py`.

## 9. Permutation analysis

`scripts/run_permutation_tests.py` tests whether the observed difference in mean within-group multivariate pairwise distance is unusual under permutation of group labels.

## 10. Figures

`scripts/make_figures.py` generates figures for multivariate distance from the reference-group centre and covariance eigenvalue structure.

## Overall data flow

```text
Clinical dataset
      |
      v
src/data.py
  numeric coercion
  median imputation
  standardisation
      |
      +-------------------------+
      |                         |
      v                         v
Euclidean drift           Covariance analysis
and dispersion                  |
      |                   +-----+------+
      |                   |            |
      v                   v            v
Trajectory             covariance   eigenstructure
analysis               score        / probability
      |                   |
      |                   v
      |                ROC / SGA
      |                   |
      +---------+---------+
                |
                v
      sensitivity + permutation
                |
                v
           figures/results
```
