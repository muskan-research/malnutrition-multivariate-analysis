# Validation analysis

The manuscript analysis used an exploratory cohort for model development and a separate held-out cohort for validation.

`scripts/run_validation_analysis.py` reproduces that separation:

1. Median imputation and standardisation are fitted on the development cohort only.
2. The same preprocessing is applied to the validation cohort without refitting.
3. The covariance models are estimated from the development cohort only.
4. The classification threshold is selected in the development cohort using Youden's J.
5. The fixed threshold is then applied unchanged to the validation cohort.

This distinction matters because refitting preprocessing, covariance structures, or the decision threshold on validation data would no longer constitute independent validation.

Run:

```bash
python -m scripts.run_validation_analysis \
    /path/to/development_dataset.xlsx \
    /path/to/validation_dataset.xlsx
```

The public repository does not contain either clinical cohort.
