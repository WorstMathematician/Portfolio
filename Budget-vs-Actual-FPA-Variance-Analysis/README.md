# Budget vs. Actual FP&A Variance Analysis

[← Back to portfolio](../README.md)

> **Purpose:** Turn budget and actual expense data into a management reporting package that explains performance, identifies material drivers, and supports forecast updates.

## Portfolio Snapshot

| Metric | Result |
|---|---:|
| Total budget | 1,762,200 |
| Total actuals | 1,718,180 |
| Net variance | -44,020 (-2.5%) |
| Forecast accuracy | 97.5% |
| Material variance rate | 55.6% of account lines |

## Business Problem

A useful FP&A package should do more than report a total variance. It should identify where the variance comes from, whether the movement is material, and which assumptions should be revisited before the next forecast cycle.

## Questions Answered

- Are actual expenses materially above or below budget?
- Which accounts explain the largest favorable or unfavorable variances?
- Which variances require management commentary?
- Is the budget accurate enough to support the next forecast cycle?

## Analytical Approach

- Reshape budget and actual rows into account-level records.
- Calculate dollar and percentage variance.
- Flag favorable, unfavorable, and material variances.
- Summarize performance by month and expense category.
- Produce KPI scorecards and management commentary.

## Largest Variance Drivers

| Driver | Variance | Interpretation |
|---|---:|---|
| Development Costs | -25,565 (-1.9%) | Favorable |
| Training Cost | -18,000 (-20.9%) | Favorable |
| Operational Costs | +9,082 (+5.5%) | Unfavorable |
| Travelling Cost | -6,700 (-14.0%) | Favorable |
| Marketing Costs | -5,324 (-7.1%) | Favorable |

## Key Outputs

- [Executive summary](outputs/executive_summary.md)
- [KPI scorecard](outputs/kpi_scorecard.md)
- [KPI scorecard CSV](outputs/kpi_scorecard.csv)
- [Source code](src/budget_variance.py)
- [Dataset note](data/DATA_NOTE.md)
- [Detailed project overview](PROJECT_OVERVIEW.md)

## Data Context

This project uses a synthetic Kaggle scenario dataset for budget-vs-actual analysis. The project demonstrates FP&A workflow and communication; the figures are not presented as audited or proprietary company financials.

## Skills Demonstrated

FP&A · Variance analysis · Forecast accuracy · Materiality · Management commentary · KPI design · Python · pandas

## Next Development Steps

Future iterations can add rolling-forecast logic, visualization previews, and automated tests for variance and materiality calculations.
