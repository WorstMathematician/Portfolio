# Data provenance and reproduction limits

The original scenario is described as a synthetic Kaggle workbook named `Financial analysis_Data Set.xlsx`; it is **not included** in the repository. Provenance, workbook version and the published financial aggregates cannot currently be independently checked. Do **not** claim that running the new pipeline reproduces the original historical scorecard.

For independent runs, supply an explicit CSV or XLSX input with `Expenses`, `Month` and expense-account headers. Use exactly one Budget row and one Actual row per month. Expense amounts are finite, nonnegative numbers. Zero budget is supported at line level; missing or invalid observations are rejected. No imputations are performed. The default generated output location is `outputs/generated/`, separate from the preserved historical files.

The published 97.5% label was aggregate net budget adherence, not evidence of time-indexed forecast accuracy. A genuine forecasting study must archive forecast issuance dates, horizons and held-out realized outcomes.
