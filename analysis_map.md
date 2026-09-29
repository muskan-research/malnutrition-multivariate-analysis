# Analysis map

## Primary analysis

`run_main_analysis.py` implements the covariance pattern-matching score using the reference and malnourished covariance structures and evaluates the score with ROC/AUC, Youden's J, sensitivity, specificity, precision, and the confusion matrix.

## Covariance structure

`run_structure_analysis.py` decomposes the covariance matrices into eigenvalues/eigenvectors and summarizes the lowest- and highest-variance axes.

## Reference-structure probability analysis

`run_reference_probability.py` projects observations into the reference covariance eigenbasis and computes axis-wise and global probabilities under the reference covariance model.

## Sensitivity analyses

`run_clinical_midpoint_sensitivity.py` compares distances from the reference-group centre with distances from a clinical reference-range midpoint.

`run_ordinal_analysis.py` tests the association between the continuous model score and ordinal SGA category.

`run_permutation_tests.py` tests whether the observed difference in within-group multivariate pairwise distance is unusual under permutation of group labels.

## Figures

`make_figures.py` generates the two main figures used to communicate multivariate distance and covariance-eigenvalue structure.
