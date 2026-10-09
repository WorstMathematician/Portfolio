# Budget vs. Actual FP&A Variance Analysis

This expense-only management reporting project now includes a source-validated, directly executable analytical reporting pipeline and synthetic regression tests.

**Historical published metrics:** budget $1,762,200; actual $1,718,180; favorable net variance $44,020; aggregate net budget adherence 97.5%. The original workbook is missing, so these figures remain historical references, not reproduced pipeline results. The legacy phrase "forecast accuracy" is a misnomer.

**Live metrics (from user-supplied validated data):** net and gross variance; weighted absolute budget error; account-month materiality (10% threshold); unfavorable exposure; monthly net variance and account breakdowns. The six report artifacts are written together into `outputs/generated/`.

**Management meaning:** Aggregate adherence helps monitor total spending while gross absolute budget error highlights offsetting planning deviations. Neither measures true predictive forecast accuracy without time-stamped forecasts and defined horizons.

See [README](README.md), [data note](data/DATA_NOTE.md) and [tests](tests/test_budget_variance.py).
