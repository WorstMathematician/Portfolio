# Budget vs. Actual FP&A Variance Analysis

[← Back to portfolio](../README.md)

> **Reproducible pipeline, with historical evidence clearly separated.** This project models expense budget-vs-actual analysis, not independently evaluated forecast predictions.

## Historical portfolio snapshot — not currently reproducible

The originally published synthetic Kaggle scenario reported a **$1,762,200 budget**, **$1,718,180 actual expenses** and **$44,020 favorable net variance** (-2.5%, actual minus budget). Its **97.5%** headline was calculated as `1 - abs(net variance) / budget` and should be called **aggregate budget adherence**, *not forecast accuracy*. Opposing line variances may cancel.

Other *historical, unverified-from-repository* results were **55.6% material account-month lines** (40/72 at a 10% threshold) and **3.7% mean monthly absolute net variance**. The underlying `Financial analysis_Data Set.xlsx` is not committed, so the published outputs cannot be independently regenerated at present. Existing files in `outputs/` are preserved as historical examples; the pipeline writes into `outputs/generated/` by default.

## Reproduce with your own explicitly supplied data

Requires Python 3.10+. CSV works with the standard library; Excel (`.xlsx`/`.xlsm`) additionally requires `openpyxl`.

```bash
python Budget-vs-Actual-FPA-Variance-Analysis/src/budget_variance.py --input /path/to/Financial\ analysis_Data\ Set.xlsx
python -m pytest -q Budget-vs-Actual-FPA-Variance-Analysis/tests
```

Input has columns `Expenses`, `Month`, and one or more account columns. Each month has exactly one `Budget` row and one `Actual` row. Positive finite, **nonnegative** expenses are assumed; missing cells, duplicate month/scenario rows, negative/nonfinite amounts, and unexpected scenarios fail fast. Month labels should be consistent (e.g. `2023-01`), as the script does not infer calendar chronology. Do not combine revenues, credits, or mixed-sign measures with this expense-only model.

Six outputs are generated from the same validated data: detail CSV, monthly CSV, account CSV, KPI CSV, KPI Markdown and executive summary Markdown. The CLI requires explicit input and never substitutes example/historical data.

## KPI semantics

| Indicator | Formula / interpretation |
|---|---|
| Net expense variance | Actual − Budget; positive = unfavorable |
| Net budget variance % | Net variance / total budget |
| Aggregate budget adherence | 1 − abs(net variance) / total budget; **not** forecast accuracy |
| Weighted absolute budget error | Sum(abs(account-month variances)) / total budget; prevents favorable/unfavorable cancellation |
| Unfavorable exposure | Sum(positive account-month variances) / total budget |
| Material variance rate | Account-month pairs with abs(line variance / budget) >= 10%, divided by all pairs; if budget = 0, a nonzero actual is always material |
| Average monthly absolute net variance | Mean over months with positive budget of abs(monthly net variance / monthly budget); still subject to within-month offsets |
| Forecast accuracy | **Unavailable** until point-in-time forecasts, prediction horizons and actual outcomes are supplied |

Zero-budget, zero-actual records are nonmaterial; zero-budget, positive-actual records are material with undefined percentage. Zero-total-budget input is rejected because budget-normalized KPIs would be undefined. This report supports variance monitoring and forecast-review prioritization; it does not establish forecast predictive quality.

## Historical references

- [Original executive summary](outputs/executive_summary.md) — illustrative, not reproduced
- [Original KPI CSV](outputs/kpi_scorecard.csv) — preserved legacy nomenclature; read with the interpretation above
- [Original KPI Markdown](outputs/kpi_scorecard.md) — preserved legacy nomenclature
- [Data provenance](data/DATA_NOTE.md)
- [Source pipeline](src/budget_variance.py)
- [Synthetic regression tests](tests/test_budget_variance.py)
