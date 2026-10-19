# Credit Card Default Risk | Classification, Calibration & Decision Tradeoffs

**A reproducible Python model-development case study comparing prevalence baseline, logistic regression, and histogram gradient boosting for next-month credit-card default risk.**

> **Do not use for real credit decisions.** The UCI observations are Taiwan credit-card **existing account holders from 2005**, not U.S. loan applications, Affirm customers, underwriting labels, or a deployable fair-lending model. Synthetic-mode results are wholly invented.

## Business question

When ranking customers by risk of next-month default, how should an analyst separate **ranking quality (ROC-AUC / PR-AUC)** from **probability quality (Brier score / calibration)**, and distinguish **classification thresholds** from *hypothetical* policy tradeoffs?

## Data and licensing

Official dataset: **I-Cheng Yeh, “Default of Credit Card Clients,” UCI Machine Learning Repository (2009), dataset 350**, DOI [10.24432/C55S3H](https://doi.org/10.24432/C55S3H), license **CC BY 4.0**. The original XLS has **30,000 unique customers**, 2005 Taiwan credit card account features and the *next-month* default target. Source: https://archive.ics.uci.edu/dataset/350/default+of+credit+card+clients . We do not redistribute the raw dataset. Source data have no per-applicant observation/origination dates allowing a meaningful chronological cross-section split.

## Run real UCI model (download once, requires internet)

From the Portfolio repository root:

```powershell
python -m pip install -r Credit-Card-Default-Risk-Model/requirements.txt
python Credit-Card-Default-Risk-Model/src/download_uci.py
python Credit-Card-Default-Risk-Model/src/risk_model.py --mode uci --file 'Credit-Card-Default-Risk-Model/data/default of credit card clients.xls'
python -m pytest -q Credit-Card-Default-Risk-Model/tests
```

If download access is restricted, obtain the original XLS directly from the [official UCI dataset page](https://archive.ics.uci.edu/dataset/350/default+of+credit+card+clients) and save it under the same `data/` path. It is gitignored. You can run without network using the *clearly separated* synthetic demonstration below.

## Run executable synthetic demo (no UCI network needed)

```powershell
python Credit-Card-Default-Risk-Model/src/risk_model.py --mode synthetic-demo
```

The synthetic generator makes 6,000 **fictional observations** with intentionally programmed outcome associations. Example performance is **not** validated empirical predictive performance. Its only purpose is testing that the pipeline, outputs, metrics, and guardrails execute end to end.

See [`outputs/synthetic_demo/REPORT.md`](outputs/synthetic_demo/REPORT.md) for locally reproduced simulation results. UCI-mode metrics are generated as `outputs/uci/` when the real data run completes; **none are claimed before that run**.

## Methodology and leakage controls

| Decision | Implementation | Reason |
| --- | --- | --- |
| Target | Next-month default (0/1) | Explicit prediction task; not future balance/revenue |
| Feature cutoff | Prior-month repayment status, bills, payments, credit limit | No future outcome fields enter model |
| Sensitive columns | SEX, EDUCATION, MARRIAGE, AGE excluded from predictors | Limits obvious direct use, but cannot establish fairness by omission |
| Holdout | 60% train / 20% validation / 20% locked test, stratified random state 42 | Data is a single 2005 cross-section; true out-of-time splitting impossible |
| Benchmark | Empirical prior prevalence, `DummyClassifier` | Checks that performance exceeds a non-informative prediction |
| Candidates | Standardized logistic regression and histogram gradient boosting | Interpretable linear baseline vs non-linear model |
| Champion selection | Minimum validation Brier score | Probability estimates matter for credit loss; keep final test untouched |
| Threshold | Predefined 0.05-0.95 grid, select hypothetical payoff on validation | Do not optimize to the test set |
| Final assessment | One test evaluation only, plus calibration bins and subgroup diagnostics | Avoid test-set tuning; inspect probability and disparate error patterns |

Output files: [`metrics.json`](outputs/synthetic_demo/metrics.json), `validation_models.csv`, `validation_policy_grid.csv`, `test_calibration_bins.csv`, and `test_subgroup_diagnostics.csv`. Only **aggregate** evaluation statistics are committed, never individual customer records.

## Hypothetical decision economics — a teaching simulation, NOT an approval policy

For an approved observation, assume **+120 fictional units if the next-month default label is 0** and **-500 units if 1**. Rejected applications earn 0. Select an upper default-probability acceptance threshold on validation, apply it once to test, and compare rejection rates, observed default labels, and aggregate fictional payoff. Real profit depends on APR, loan amount, repayment timing, losses given default, funding, servicing, legal constraints, capital, fairness, and selection effects. **This dataset contains outcomes on customers who already hold cards, so rejected-applicant counterfactuals cannot be inferred.** No real approval policy can be justified by this exercise.

## Fair lending, limitations & model governance

Model performance != legal compliance. Excluding directly sensitive fields does not address proxies, representativeness, disparate impact, incomplete observations, shifting populations, or valid adverse-action explanations. Held-out subgroup diagnostics are **descriptive diagnostic tools** (historical source coding), not an ECOA/Reg B/FCRA compliance test. A compliant use case would require professional legal review, formal model validation, monitoring, explainability, data lineage, drift testing, appropriate permissible-purpose and adverse-action processes, and fit-for-use evaluation of current U.S. lending populations. Historical geographic generalization is not supported here.

## Recommended interview talking points

1. Distinguish next-month cardholder *default label* from a lender's final charge-off / lifetime loss and reject-inference problem.
2. Present ROC-AUC alongside PR-AUC and Brier: ranking alone cannot validate probability calibration.
3. Explain why this single 2005 customer cohort cannot support chronological evaluation; describe what dated multi-cohort data would enable instead.
4. Describe why the classification threshold 0.50 is not economically optimal by default, and why scenario payoff units are hypothetical rather than business results.
5. Explain precisely which populations, data availability, governance checks, and policy questions remain unanswered.
