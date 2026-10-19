# Dataset Notes

[← Back to portfolio](../README.md)

## Program Finance Control Tower

- Folder: `Program-Finance-Control-Tower`
- Source label: Synthetic Kaggle scenario dataset for program-cost analysis
- Raw file: `Dynamic_Cost_Accounting_Dataset.csv`
- Raw shape: 2,643 rows × 21 columns
- Analysis treatment: departments are treated as workstreams; period budget and actual spend are accumulated to create control metrics.

## Budget vs. Actual FP&A Variance Analysis

- Folder: `Budget-vs-Actual-FPA-Variance-Analysis`
- Source label: Synthetic Kaggle scenario dataset for budget-vs-actual analysis
- Raw file: `Financial analysis_Data Set.xlsx`
- Raw shape: 24 rows × 8 columns
- Analysis shape: 72 account-level rows after reshaping

## Defense Contractor Peer Benchmarking

- Folder: `Defense-Contractor-Peer-Benchmarking`
- Source label: Synthetic or community Kaggle scenario dataset for manufacturer benchmarking
- Raw file: `Defense_manufacture_companies_2005_to_2024.csv`
- Raw shape: 2,004 rows × 9 columns
- Cleaned panel shape: 1,986 company-year records

## Data-use note

Scenario datasets are used to demonstrate workflow, KPI design, reporting, and financial communication. They are not represented as audited financials, official procurement records, or proprietary internal program data.

Project-specific provenance notes take precedence when they provide more detail.

## Market Returns & Volatility Forecasting

- Folder: Market-Returns-Volatility-Forecasting
- Proposed source: Yahoo Finance daily SPY prices, including provider adjusted close and actions, via yfinance.
- Raw data committed: **none**. The pipeline saves source snapshots and SHA-256 checksums locally when acquisition succeeds.
- Research status: no verified market observations or empirical performance report is bundled. Synthetic software tests are explicitly separate.
- Documentation: [Source and limitations](../Market-Returns-Volatility-Forecasting/docs/DATA_PROVENANCE.md)
