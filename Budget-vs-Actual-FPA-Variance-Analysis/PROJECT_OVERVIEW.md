# Budget vs. Actual FP&A Variance Analysis

## Business view

This project turns budget and actual expense data into a management reporting package. The goal is to explain whether spending is tracking to plan, identify the largest variance drivers, and support forecast updates.

## Questions answered

- Are actual expenses materially above or below budget?
- Which accounts explain the largest favorable or unfavorable variances?
- Which variances are large enough to require management commentary?
- Is the budget accurate enough to support the next forecast cycle?

## Dataset

- Source label: Synthetic Kaggle scenario dataset for budget-vs-actual analysis
- Raw file: Financial analysis_Data Set.xlsx
- Raw shape: 24 rows x 8 columns
- Analysis shape: 72 account-level budget/actual rows after reshaping

## Methods

- Reshape budget and actual rows into account-level records.
- Calculate dollar variance and percent variance.
- Flag favorable, unfavorable, and material variances.
- Summarize results by month and expense category.
- Create KPI scorecards and executive commentary.

## Key indicators

| Indicator | Business use |
|---|---|
| Net Budget Variance | Shows whether actual spend is materially different from plan. |
| Forecast Accuracy | Measures how close budget was to actuals. |
| Unfavorable Variance Exposure | Quantifies cost pressure requiring review. |
| Material Variance Rate | Shows how often account lines exceed the threshold. |
| Largest Monthly Variance | Highlights the month requiring the clearest explanation. |

## Portfolio framing

This case study demonstrates FP&A variance analysis, account-level drilldowns, forecast accuracy reporting, KPI design, dashboard automation, and executive communication.
