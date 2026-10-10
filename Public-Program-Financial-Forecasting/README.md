# Public Program Financial Forecasting

**Status: Program-level data expanded; still an exploratory research dashboard, not a validated predictive model.**

This independent portfolio case study investigates whether official LA County homelessness spending data support responsible financial prediction. It emphasizes source provenance, accounting reconciliation, statistical analysis, and honest model eligibility.

## Program-by-agency dataset (added in second milestone)

- [Download official-source ongoing program/agency data](data/ongoing_program_agency_2023_2025.csv): **73 financial records / 292 quarterly values**, representing **19 distinct programs**, **13 agencies**, and **31 program-agency pairs observed in both fiscal years**.
- FY 2023–24: **32 program/agency rows**, exactly reconciled to $400,492,675.72 reported ongoing YTD expenditure.
- FY 2024–25: **41 program/agency rows**, reconciled to $538,421,310 published ongoing YTD expenditure (the published quarterly sums are $1 higher).
- New [Program Explorer](dashboard/pages/1_Program_Explorer.py) offers filters, real historical program charts, allocations vs actuals, source links and CSV export.
- New [Data acquisition and reconciliation note](DATA_NOTE.md) documents transcription decisions, source pages and known limits.
- Run **python -m src.program_panel** to create audited quarterly panel CSV and JSON reconciliation/readiness reports in **outputs/**.
- **Important:** eight independent quarterly periods remain insufficient for the model promotion gate; no forecast accuracy is claimed.

## What has been validated

- **8 fiscal-year reports** (FY 2017–18 through FY 2024–25) and **32 quarterly actuals** manually transcribed from official published year-end total rows.
- All 8 reports reconcile to their published YTD figure **within USD 1**; 2017–18, 2019–20, and 2024–25 differ by USD 1.
- 2017–18 through 2019–20 are labeled **comprehensive**; 2020–21 through 2021–22 **unclassified**; 2022–23 through 2024–25 explicitly **ongoing**.
- **Only 12 consecutive quarters** have the most recent explicitly ongoing definition. Data cannot be pooled indiscriminately.
- The project's initial **24 comparable quarters** promotion threshold is **not met**. No scored model or forecast is claimed.

Official sources: [County expenditure-report archive](https://homeless.lacounty.gov/evaluations-audits/). Per-record PDF links appear in [the source data](data/annual_quarterly_totals.csv). The FY2018–19 published *actuals* were recovered from [the August 2019 County oversight meeting packet](https://homeless.lacounty.gov/wp-content/uploads/2019/08/09.05.19-COAB-MTG-PACKET-FINAL.pdf); the initial FY2018–19 PDF link was not accessible.

## Run locally (Python 3.10+)

From this project folder:

1. Install: **python -m pip install -r requirements.txt**
2. Generate diagnostics: **python -m src.pipeline**
3. Test: **python -m pytest -q**
4. Open dashboard: **streamlit run dashboard/app.py**

Generated CSV reports and readiness JSON are written to ignored **outputs/**.

## Interactive dashboard

- Historical actuals, scope selection, annual and fiscal-quarter trends
- Reconciliation, coverage, and data-sufficiency tables
- Statistical outlier review, with insufficient-reference safeguards
- Candidate model registry (not trained); visible blocked readiness state
- Hypothetical spending/funding assumption controls and scenario export
- Original report links and source CSV download

These are **expenditure measures**, not service utilization or housing outcomes. Unspent funds are not automatically cost savings. Source PDFs are retrospective and should not be treated as contemporaneous quarter-end data availability.

See [the implementation and modeling gates](PROJECT_PLAN.md).

*Independent educational work; not affiliated with LA County or LAHSA.*
