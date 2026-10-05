# Program Finance Control Tower

[← Back to portfolio](../README.md)

> **Purpose:** Convert period-level cost data into a finance control view that helps leadership identify workstreams requiring forecast or management review.

## Portfolio Snapshot

| Metric | Result |
|---|---:|
| Workstreams reviewed | 10 |
| Watchlist workstreams | 3 |
| Portfolio EAC variance vs. BAC | 22.3% |
| Projected portfolio margin at completion | 36.3% |

## Business Problem

Program finance teams need a fast way to distinguish normal cost movement from workstreams that require intervention. This project converts cost-accounting records into a management view centered on completion cost, efficiency, margin, and risk.

## Questions Answered

- Which workstreams need leadership attention?
- Is expected completion cost above or below the budget baseline?
- Which workstreams show cost, margin, or execution risk?
- What spend rate should be reviewed during forecast updates?

## Analytical Approach

- Clean and normalize period-level cost records.
- Group observations into portfolio workstreams.
- Accumulate budget and actual spend.
- Calculate EAC, ETC, CPI, cost variance, projected margin, and status.
- Produce KPI scorecards and executive commentary for review.

## Management Watchlist

The generated scenario output identifies three workstreams for review:

| Workstream | Status | EAC variance | Projected margin | CPI | Risk score |
|---|---|---:|---:|---:|---:|
| Program 6 | Yellow | 24.2% | 37.8% | 1.32 | 0.84 |
| Program 1 | Yellow | 22.7% | 36.6% | 1.29 | 0.80 |
| Program 7 | Red | 19.4% | 33.9% | 1.24 | 0.92 |

## Key Outputs

- [Executive summary](outputs/executive_summary.md)
- [KPI scorecard](outputs/kpi_scorecard.md)
- [KPI scorecard CSV](outputs/kpi_scorecard.csv)
- [Source code](src/program_finance.py)
- [Dataset note](data/DATA_NOTE.md)
- [Detailed project overview](PROJECT_OVERVIEW.md)

## Data Context

This project uses a synthetic Kaggle scenario dataset for program-cost analysis. Departments are treated as portfolio workstreams for analytical purposes. The scenario is designed to demonstrate program-control workflow and should not be interpreted as audited or proprietary program financials.

## Skills Demonstrated

Program finance · Forecast review · EAC/ETC modeling · CPI · Margin analysis · KPI design · Management reporting · Python · pandas

## Next Development Steps

Future iterations can add interactive visualization, explicit forecast-version comparisons, and automated tests for the core calculation functions.
