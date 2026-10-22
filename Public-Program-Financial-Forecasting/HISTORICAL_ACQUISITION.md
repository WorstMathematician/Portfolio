# Expand historical spending — acquisition protocol

The historical source acquisition script collects the original County PDF files for FY 2017–18 to FY 2022–23. It validates that the response is a PDF, records SHA-256, and logs failures; it does **not** mistake downloads for usable machine-learning observations.

## Execute

From the project directory, run:

`python scripts/collect_historical_sources.py`

PDF originals go under ignored `data/source_pdfs/`. Verify each page and table using an appropriate PDF renderer before transcribing lines. Record original strategy identifiers and quarters, keeping annual, YTD and multi-year cumulative totals separate. Reconcile fiscal-year-only line totals and aggregate totals exactly or document source rounding. Leave rows unresolved when a PDF is inaccessible.

The FY 2020–21 report [contains visible program/strategy-agency rows](https://homeless.lacounty.gov/wp-content/uploads/2022/04/CEO-8-12-21-Measure-H-EXP-Log-FY20-21-COAB4.pdf), including negative expenditure adjustments and a column labeled **ONLY FY 20-21 YTD Expenditures**. Never substitute the adjacent FY 19–20 + FY 20–21 cumulative column.

**Measure A:** Keep adopted spending plans, receipts, distributions, and actual program expenditures in different datasets. [LACAHSA's tracker](https://lacahsa.gov/measure-a-funds-tracker/) describes receipts and distributions, not necessarily expenses incurred. Do not extend a Measure H expense history with Measure A funding allocations.

Collection depends on live public-source access. This system has not downloaded and validated the six PDF originals; additional detailed observation files remain pending extraction.
