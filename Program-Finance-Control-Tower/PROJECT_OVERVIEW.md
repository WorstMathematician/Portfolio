# Program Finance Control Tower

## Business view

This project converts period-level cost data into a finance control view. The goal is to show which workstreams are tracking to plan and which workstreams need forecast review.

## Questions answered

- Which workstreams need leadership attention?
- Is expected completion cost above or below the budget baseline?
- Which workstreams show cost, margin, or risk issues?
- What spend rate should be reviewed during forecast updates?

## Dataset

- Source label: Synthetic Kaggle scenario dataset for program-cost analysis
- Raw file: Dynamic_Cost_Accounting_Dataset.csv
- Raw shape: 2,643 rows x 21 columns
- Analysis treatment: departments are treated as portfolio workstreams.

## Methods

- Clean and normalize fields.
- Group records by workstream.
- Accumulate budget and actual spend.
- Calculate EAC, ETC, CPI, cost variance, projected margin, and status.
- Export dashboard-ready tables, visuals, and commentary.

## Key indicators

| Indicator | Business use |
|---|---|
| Portfolio EAC Variance | Shows whether expected completion cost is above or below baseline. |
| Weighted CPI | Measures cost efficiency across the portfolio. |
| Projected Margin at Completion | Connects execution performance to margin protection. |
| Watchlist Workstream Rate | Shows how much of the portfolio needs review. |
| Median Period Burn Rate | Supports forecast discussions. |

## Portfolio framing

This case study demonstrates finance monitoring, forecast review, EAC and ETC modeling, margin analysis, KPI design, and executive reporting.
