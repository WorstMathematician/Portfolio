# Data acquisition and financial reconciliation

## Dataset added to PR #9

`data/ongoing_program_agency_2023_2025.csv` contains **73 published program-agency-year lines**, represented by **292 quarterly expenditure observations** in the generated long format.

- FY 2023–24: **32 program-agency rows** — the published ongoing-spending report; source [PDF](https://file.lacounty.gov/SDSInter/lac/1187357_MeasureHExpenditureLog-FY23-24-COAB.pdf), printed PDF pages 1–2.
- FY 2024–25: **41 program-agency rows** — the published ongoing-spending report; source [PDF](https://file.lacounty.gov/SDSInter/lac/1195430_MeasureHExpenditureLog-FY24-25-COAB.pdf), printed PDF pages 1–2.

These are **original public financial numbers, manually transcribed and checked against the reports' rendered pages and extracted text**. The reports themselves are authoritative; this transcription is an independently maintained research copy and should be reviewed against original source PDFs before operational reuse.

No actual patient or client records are included. Agency names and program labels follow the published reports, with minor consistent punctuation/spacing normalization. The symbol `-` in quarterly financial cells is represented as **numeric zero** solely where the published report uses a dash, not for missing source pages. Each CSV row contains an original source URL and 1-indexed PDF page.

## Reconciliation gates

The automated `src.program_panel` procedure validates:

1. Required columns; expected fiscal years, unique program-agency-year keys, valid source URL/page, and nonnegative allocations.
2. Program-row quarterly sums match reported YTD (within a one-dollar tolerance for financial rounding); no suspicious row is silently dropped.
3. Program rows by fiscal year sum to the full official published **ongoing** report's allocation, each quarter, and published year-to-date expenditures (within one dollar).
4. Any discrepancy exceeding one dollar fails the pipeline.

**Verified totals**:

| Year | Rows | Allocation | Reported YTD |
| --- | ---: | ---: | ---: |
| FY 2023–24 | 32 | $527,932,000.00 | $400,492,675.72 |
| FY 2024–25 | 41 | $651,312,000.00 | $538,421,310.00 |

The FY 2024–25 report's quarterly expenditures sum to **$538,421,311**, while its published YTD is **$538,421,310**: one dollar of printed rounding difference, preserved instead of corrected away. Some individual program lines also have one-dollar differences. The FY 2023–24 report reconciles exactly to the cent.

## Statistical limitations and honest use

- Only **8 independent quarterly time periods** across the 2 ongoing fiscal-year reports. Cross-program row count (292) is not equivalent to 292 independent forecast origins. The project's 24-comparable-quarter promotion gate remains **blocked**.
- The data are retrospective fiscal-year-end totals and cannot substantiate what was available to forecasters at each earlier quarter-end. A real-time backtest requires publication timing or a clearly labeled hindsight limitation.
- Agency and program classifications may have shifted; comparable labels are only provisional until the underlying program and funding definitions are audited.
- Year-end allocation amounts should not be used as inputs at earlier historical quarter-end origins unless their effective dates can be established.
- One-time commitments are **excluded**. Historical comprehensive totals must not be mixed with this ongoing-only panel.
- No service utilization, client outcomes, program effectiveness, or causal impact can be inferred from expenditure amounts alone.

## Reproduce

From the project root:

```
python -m src.program_panel --input data/ongoing_program_agency_2023_2025.csv --totals data/annual_quarterly_totals.csv --output outputs
python -m pytest -q
streamlit run dashboard/app.py
```

The separate Streamlit `Program Explorer` page provides genuine program-by-agency financial drilldown without presenting misleading model forecasts.