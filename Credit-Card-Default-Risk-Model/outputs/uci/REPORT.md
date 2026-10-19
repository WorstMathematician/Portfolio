# Next-month credit-card default model (uci)

> **Real historical UCI data: Taiwan, 2005**. This is a learning case, **not an approved underwriting model**.

- Rows: 30,000 (train 18,000; validation 6,000; held-out test 6,000).
- Validation-chosen classifier: **hist gradient boosting** (minimum validation Brier score).
- Held-out test ROC-AUC: **0.7773**; PR-AUC: **0.5560**; Brier: **0.1353**.
- Held-out test F1 at default-probability 0.50: **0.4640**.
- Fictional payoff threshold selected using **validation only**: **0.200** (approve if estimated default probability <= threshold).
- Held-out scenario approval rate: **65.88%**; fictional payoff/application **32.25 units**.

Model selection and threshold selection never use the final test partition. See `metrics.json`, `validation_models.csv`, `test_calibration_bins.csv`, and `test_subgroup_diagnostics.csv` for diagnostics.

**Interpretation restrictions:** No application decision date permits genuine out-of-time testing. Our fictional payoff assumption does not estimate real profits, causal intervention effects, or legally permissible lending decisions. Excluding demographic features does not establish non-discrimination. Real use would require validation, documented monitoring, governance, legal review, data access controls, and independent fair-lending testing.
