# Defense Contractor Peer Benchmarking

## Business view

This project benchmarks manufacturers using revenue and category-share data. The goal is to size the benchmark market, identify concentration, compare peer growth, and build simple long-range planning scenarios.

## Questions answered

- Which companies lead the benchmark set by estimated category revenue?
- How concentrated is revenue among the largest companies?
- Which countries represent the largest share of the benchmark market?
- What growth assumptions should be used in downside, base, and upside planning scenarios?

## Dataset

- Source label: Synthetic or community Kaggle scenario dataset for manufacturer benchmarking
- Raw file: Defense_manufacture_companies_2005_to_2024.csv
- Raw shape: 2,004 rows x 9 columns
- Cleaned panel shape: 1,986 company-year records after removing incomplete or invalid revenue records

## Methods

- Clean revenue and category-share fields.
- Estimate category revenue from total revenue and category percentage.
- Build latest-year company and country benchmark summaries.
- Calculate eligible multi-year CAGR only for companies with sufficient history.
- Build downside, base, and upside long-range planning scenarios.

## Key indicators

| Indicator | Business use |
|---|---|
| Latest-Year Benchmark Revenue | Sizes the market represented by the benchmark set. |
| Top 5 Revenue Concentration | Shows market concentration risk. |
| USA Revenue Share | Shows geographic exposure. |
| Eligible Median Peer CAGR | Provides a planning growth reference. |
| Top-Quartile Peer CAGR | Provides an upside growth reference. |
| 3-Year Base LRP Growth | Converts peer growth into a planning scenario. |

## Portfolio framing

This case study demonstrates industry benchmarking, peer growth analysis, market concentration analysis, long-range planning, KPI design, and executive reporting.
