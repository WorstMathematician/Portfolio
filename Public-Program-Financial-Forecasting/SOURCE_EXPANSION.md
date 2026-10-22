# Historical source expansion register — Measure H and Measure A

Updated 2026-10-09. This is a **source register, not an assertion that all referenced records were extracted**. Sources are official County publications unless indicated. Separately track fiscal year, funding measure, amount type, spending category, and publication/effective dates. Do not claim the Measure A service tracker is expenditure data.

| Period | Measure | Evidence | Kind | Extraction status |
|---|---|---|---|---|
| FY 2017-18 | H | [County expenditure archives](https://homeless.lacounty.gov/evaluations-audits/) | Program expenditure log | Annual summary only; detailed transcription pending |
| FY 2018-19 | H | [County expenditure archives](https://homeless.lacounty.gov/evaluations-audits/) | Expenditure log and oversight packet | Annual summary only; detailed transcription pending |
| FY 2019-20 | H | [County expenditure archives](https://homeless.lacounty.gov/evaluations-audits/) | Program expenditure log | Annual summary only; detailed transcription pending |
| FY 2020-21 | H | [County expenditure archives](https://homeless.lacounty.gov/evaluations-audits/) | Program expenditure log | Annual summary only; scope unclassified |
| FY 2021-22 | H | [County expenditure archives](https://homeless.lacounty.gov/evaluations-audits/) | Program expenditure log | Annual summary only; scope unclassified |
| FY 2022-23 | H | [County expenditure archives](https://homeless.lacounty.gov/evaluations-audits/) | Program expenditure log | Annual ongoing total only; detail pending |
| FY 2023-24 | H | [FY23-24 source](https://file.lacounty.gov/SDSInter/lac/1187357_MeasureHExpenditureLog-FY23-24-COAB.pdf) | Ongoing program/agency quarterly spending | 32 lines extracted and reconciled |
| FY 2024-25 | H with A tax transition | [FY24-25 source](https://file.lacounty.gov/SDSInter/lac/1195430_MeasureHExpenditureLog-FY24-25-COAB.pdf) | Ongoing program/agency quarterly spending | 41 lines extracted and reconciled; reporting taxonomy still H |
| FY 2025-26 | A with H carryover | [Approved funding recommendations](https://homeless.lacounty.gov/budget-archive/) | Approved funding plans and revisions | Identified, **not** extracted as actual expenditures |
| FY 2026-27 | A with H carryover and HHAP | [Approved spending plan](https://homeless.lacounty.gov/fiscal-year-2026-27-measure-a-spending-plan/) | Approved funding plans and revenue mix | Identified, **not** extracted as actual expenditures |
| Measure A era | A | [LACAHSA fund tracker](https://lacahsa.gov/measure-a-funds-tracker/) | Receipts and distributions, LACAHSA jurisdiction scope | Identified; no time-stamped exports acquired |
| Measure A era | A | [County progress tracker](https://homeless.lacounty.gov/measure-a-progress-tracker/) | Outcome metrics | Identified; not an expenditure measure |

## Core financial definitions

- **Appropriation/allocation**: approved availability of funds, subject to revisions.
- **Distributions/disbursements**: funds transferred to an agency or jurisdiction; not necessarily program spending.
- **Expenditure**: reported expenses within an accounting period and stated reporting scope.
- **Carryover**: prior-year balances used in later spending plans. Must not be added to current-year revenue as though new taxes.
- **Outcome**: people housed or served, not dollars spent.
- **Fiscal year of a budget** is different from its approval date, revision date, reporting period and publication date.

## Essential quality gates for expanded data

1. Extract raw program-by-agency quarterly tables from each Measure H PDF and retain source page references.
2. Preserve original strategy labels and build an evidence-based many-to-many program crosswalk; map only with documentary support.
3. Reconcile each extracted year to published YTD and the applicable ongoing/one-time/comprehensive subtotal. Never force equality by altering raw values.
4. Require origin-time availability of budget revisions before introducing allocation features in historical forecasts.
5. Track Measure A receipts, distribution and eventual expenditure actuals in **separate tables**; do not assume a budget plan equals observed spending.
6. Distinguish the April 2025 tax transition from the FY 2024-25 reporting label (the H spending log can include legacy funds after A starts).
7. Report data sufficiency by **number of distinct comparable quarters**, not by total panel cells. Current detailed H panel has 8 quarters, not enough for confident long-horizon models.

## Target data products

- `fact_program_expenditure_quarterly.csv`: source/measure/scope/year/quarter/program/agency/actual.
- `fact_funding_allocation_versions.csv`: adopted and revised allocations, effective time, funding source.
- `fact_measure_a_distributions.csv`: receipts/distributions, source jurisdiction, transaction period.
- `dim_program_crosswalk.csv`: original category -> comparable analytic category, provenance and confidence.
- `fact_services_outcomes.csv`: outcomes with clearly documented definitions.

**Never impute missing Measure A expenditure actuals from planned allocations.** Forecast evaluation is blocked until target and source time series are comparable and historical dates can be enforced.
