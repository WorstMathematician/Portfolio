# Phased implementation and acceptance gates

## M1 — Historical public finance audit (implemented)

- Source-linked annual rows, exact Decimal reconciliation, and published-total tolerance of USD 1.
- Reporting-scope classifications and continuity-aware 24-quarter model eligibility gate.
- Exploratory annual changes, Q4 shares, same-quarter robust outlier candidates (never automatically removed).
- CSV/JSON diagnostic exports, local tests, Streamlit data/diagnostic/scenario preview.
- Result: 8 years / 32 quarters; all reconcilable; only 12 explicitly ongoing quarters; **confirmatory model gate blocked**.

## M2 — Detailed program and agency panel (next)

- Collect original PDFs with metadata and hashes. Verify extracted tables against page images.
- Separate ongoing, one-time, and historical comprehensive figures. Preserve negative adjustments.
- Reconcile program totals to source subtotals and fiscal-year totals; document every exception.
- Produce a reviewed mapping of old strategy codes to newer programs. Refuse speculative links.
- Archive allocations with effective dates, guarding historical forecast-origin availability.
- Evaluate Measure H to Measure A funding transition before using cross-regime predictions.

## M3 — Statistical diagnostics and adjustments

- Examine missing values, zero spend, seasonality, distributions, trends, outliers, heteroskedasticity and structural breaks.
- Assign anomaly reason and resolution status; preserve originals.
- Compare robust modeling and transformation experiments without target leakage.
- Document sample size, pooled-vs-individual model feasibility, and sensitivity to non-comparable periods.

## M4 — Forecasting once M2/M3 pass

- Predict next-quarter net expenditure, secondarily fiscal year-end actual at a defined forecast origin.
- Baseline lag-1, seasonal naïve, historical spending run rate; ETS, constrained SARIMAX, regularized regression, gradient boosting *only if eligible*.
- Constrain parameter search to sample size; nested chronological tuning and rolling-origin evaluation.
- Compare 1-, 2-, 4-quarter horizons; MAE, bias, MASE, WAPE when valid, predictive-interval coverage.
- Publish actual holdout metrics, model artifact/data version, and an unambiguous model card; if baseline wins, prefer baseline.

## M5 — Dashboard and financial decision layer

- Current explorer is a working research interface; extend it with validated model selection, historical forecast replay, uncertainty, funding-risk alerts and well-defined agency/program filters.
- Forecast UI must remain blocked when training/evaluation gate fails.
- Distinguish extrapolations and what-if scenario assumptions from validated predictions.

## M6 — Presentation and operations

- CI for source integrity and tests, visual/accessibility QA, reproducibility, source provenance, executive report and reviewer demo.
- Integrate project into portfolio root homepage only when finance-model results can be honestly presented.

**Constraints:** No private patient data; no causal claims; no fabricated forecast scores; no assumption that one fiscal-year spending plan was known from quarter one. The audited source data are *aggregate report totals*, not a reconciled provider or program panel.
