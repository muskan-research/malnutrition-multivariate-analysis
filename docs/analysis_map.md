# Analysis map

The repository separates reusable calculations in `src/` from executable analyses in `scripts/`.

## 1. Preprocessing

`src/data.py` loads the data, checks the 37 biomarker columns, fits median imputation and standardisation, and applies those transformations.

For validation, preprocessing is fitted once in the development cohort and reused unchanged in the held-out cohort.

## 2. Multivariate drift

`src/drift.py` calculates:

- Euclidean distance from the SGA-A centroid;
- mean within-group pairwise Euclidean distance.

Entry point: `scripts/run_drift_analysis.py`.

These measures describe the magnitude of multivariate displacement and the dispersion of individual profiles.

## 3. Geometric trajectories

`src/trajectory.py` calculates SGA-A, SGA-B, and SGA-C centroids and the vectors connecting them.

It returns:

- A→B, B→C, and A→C Euclidean transition lengths;
- cosine similarity for the relevant vector pairs;
- corresponding angular divergence in degrees.

Entry point: `scripts/run_trajectory_analysis.py`.

The analysis is cross-sectional and centroid-based; it is not a longitudinal patient trajectory.

## 4. Covariance model

`src/covariance_model.py` contains separate functions for:

- fitting the reference and malnourished covariance models;
- scoring new observations against fitted models;
- selecting a Youden threshold;
- evaluating binary classification performance.

Entry points:

- `scripts/run_main_analysis.py` for exploratory same-cohort analysis;
- `scripts/run_validation_analysis.py` for development/validation separation.

The validation script applies the development preprocessing, fitted covariance models, and fixed decision threshold to the held-out cohort without refitting.

## 5. Covariance eigenstructure

`src/structure.py` decomposes group covariance matrices into eigenvalues and eigenvectors and summarises low- and high-variance axes.

Entry point: `scripts/run_structure_analysis.py`.

## 6. Reference-structure probability

`src/reference_probability.py` projects observations into the reference covariance eigenbasis and calculates axis-wise and global probabilities.

Entry point: `scripts/run_reference_probability.py`.

## 7. Ordinal SGA analysis

`scripts/run_ordinal_analysis.py` relates the continuous covariance-based score to SGA A/B/C using Spearman correlation and the Kruskal–Wallis test.

## 8. Clinical-reference sensitivity analysis

`scripts/run_clinical_midpoint_sensitivity.py` compares the reference-centroid distance with distance from clinical reference-range midpoints.

## 9. Permutation analysis

`scripts/run_permutation_tests.py` evaluates the observed difference in within-group mean pairwise distance against a permutation-based null distribution.

## 10. Figures

`scripts/make_figures.py` generates figures for multivariate distance and covariance eigenvalue structure.

## Overall flow

```text
Dataset
  |
  v
Preprocessing
  |
  +----------------------+----------------------+
  |                      |                      |
  v                      v                      v
Drift / dispersion   Trajectory geometry   Covariance model
  |                      |                      |
  |                      |                 +----+----+
  |                      |                 |         |
  |                      |                 v         v
  |                      |              ROC/SGA   Validation
  |                      |
  +----------+-----------+
             |
             v
  Structure / probability /
  sensitivity / permutation
             |
             v
          Outputs
```
