# Defense Contractor Peer Benchmarking

[← Back to portfolio](../README.md)

> **Purpose:** Benchmark manufacturers by estimated category revenue, concentration, geography, and growth to create external planning references.

## Portfolio Snapshot

| Metric | Result |
|---|---:|
| Latest benchmark year | 2024 |
| Companies benchmarked | 100 |
| Latest-year benchmark revenue | 606.2B |
| Top-five revenue concentration | 36.1% |
| USA revenue share | 54.5% |
| Eligible median peer CAGR | 4.4% |

## Business Problem

Strategic planning often needs an external reference point. This project builds a peer benchmark that can help frame market size, concentration, relative growth, and reasonable downside/base/upside planning assumptions.

## Questions Answered

- Which companies lead the benchmark set by estimated category revenue?
- How concentrated is revenue among the largest companies?
- Which geographies represent the largest share of the benchmark market?
- What growth assumptions can serve as external planning references?

## Analytical Approach

- Clean revenue and category-share fields.
- Estimate category revenue from total revenue and category percentage.
- Build company and country benchmark summaries.
- Calculate multi-year CAGR only for companies with sufficient history.
- Build downside, base, and upside long-range planning scenarios.

## Market Leaders in the Scenario Output

| Company | Country | Estimated category revenue | Benchmark share |
|---|---|---:|---:|
| Lockheed Martin | USA | 64,650.0M | 10.7% |
| Aviation Industry Corporation of China | China | 44,911.2M | 7.4% |
| RTX | USA | 40,600.0M | 6.7% |
| Northrop Grumman | USA | 35,197.0M | 5.8% |
| General Dynamics | USA | 33,651.0M | 5.6% |

## Planning Takeaway

The scenario's base case uses an eligible-peer median CAGR of 4.4%, reaching 2,447.9M by 2027. The peer median is used as a planning anchor rather than as a forecast guarantee.

## Key Outputs

- [Executive summary](outputs/executive_summary.md)
- [KPI scorecard](outputs/kpi_scorecard.md)
- [KPI scorecard CSV](outputs/kpi_scorecard.csv)
- [Source code](src/defense_benchmark.py)
- [Dataset note](data/DATA_NOTE.md)
- [Detailed project overview](PROJECT_OVERVIEW.md)

## Data Context

This project uses a synthetic or community Kaggle scenario dataset for manufacturer benchmarking. The analysis is a portfolio exercise and is not presented as official procurement data, audited company reporting, or investment research.

## Skills Demonstrated

Peer benchmarking · Market concentration · CAGR analysis · Scenario planning · Strategic finance · KPI design · Python · pandas

## Next Development Steps

Future iterations can add visualization previews, sensitivity analysis, and tests for growth and concentration calculations.
