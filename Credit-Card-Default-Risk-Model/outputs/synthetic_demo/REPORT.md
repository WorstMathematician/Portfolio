# Next-month credit-card default model (synthetic_demo)

> **SIMULATED demonstration only**. This is a learning case, **not an approved underwriting model**.

- Rows: 6,000 (train 3,600; validation 1,200; held-out test 1,200).
- Validation-chosen classifier: **logistic regression** (minimum validation Brier score).
- Held-out test ROC-AUC: **0.8174**; PR-AUC: **0.5911**; Brier: **0.1248**.
- Held-out test F1 at default-probability 0.50: **0.4988**.
- Fictional payoff threshold selected using **validation only**: **0.225** (approve if estimated default probability <= threshold).
- Held-out scenario approval rate: **62.00%**; fictional payoff/application **44.95 units**.

Model selection and threshold selection never use the final test partition. See `metrics.json`, `validation_models.csv`, `test_calibration_bins.csv`, and `test_subgroup_diagnostics.csv` for diagnostics.

**Interpretation restrictions:** No application decision date permits genuine out-of-time testing. Our fictional payoff assumption does not estimate real profits, causal intervention effects, or legally permissible lending decisions. Excluding demographic features does not establish non-discrimination. Real use would require validation, documented monitoring, governance, legal review, data access controls, and independent fair-lending testing.
