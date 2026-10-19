# Credit Portfolio Monitoring | SQL + Vintage + Roll Rates

**A reproducible loan-monitoring case study: SQLite queries, fictional installment-level data, cohort analytics, repayment behavior, and exposure-based delinquency.**

> **Data classification: 100% synthetic.** Generated accounts, payment dates, interest assumptions, and delinquency outcomes are a teaching scenario; no actual lender metrics, defaults, proprietary data, borrower identities, or underwriting decisions are represented.

## Analyst's question

How do we distinguish an increasing share of past-due *loans* from an increasing share of outstanding contractual *dollars*, locate exposure by vintage, and track whether borrowers cure, worsen, or pay off from one month to the next?

## Reproduce in one command (Python standard library + SQLite)

```powershell
python Credit-Portfolio-SQL-Monitoring/src/build.py
python -m pytest -q Credit-Portfolio-SQL-Monitoring/tests
```

Creates `outputs/portfolio.sqlite` and CSV reporting artifacts using **2,400 synthetic loans** originated across 24 monthly cohorts (100/month, Jan 2023-Dec 2024) and 30 month-end reporting dates through Jun 2025. Use `--loans-per-month 3` for a fast smoke test or `--seed 123` for an alternate controlled scenario. CSV and summary artifacts committed under `outputs/` are produced from the default seed; the .sqlite database itself is regenerated locally and not committed.

## Data model / grain

| Entity | Key and grain | Analytical role |
| --- | --- | --- |
| `loans` | one row per `loan_id` | originations, origination cohorts, contractual receivables, risk tiers |
| `installments` | `(loan_id, installment_number)` | contractual due date/amount, oldest-unpaid FIFO rule |
| `payments` | one row per `payment_id` | **actual event date** and payment amount; no future cash in an as-of view |
| `calendar_months` | one row per as-of date | fixed month-end calendar |
| `monthly_status` | `(as_of, loan_id)` | one observation per originated loan / month-end, including closed accounts |

Amounts are stored in integer **cents** to avoid floating-point reconciliation errors. Repayments in this illustrative generator are all-or-nothing installments and simple scheduled finance charges; actual servicing may include partial payments, prepayments, fees, charge-offs, reversals, and restructured terms not covered here.

## Definitions that matter

- **Days past due (DPD):** as-of date minus the earliest due installment whose *cumulative due* exceeds *cumulative payments as-of*, allocated oldest-first. A payment after month-end does not cure a prior month's delinquency.
- **Open loan:** remaining scheduled contractual receivables **>0**. Contractual receivables contain principal plus *scheduled finance charges* and are **not GAAP book value, net principal balance, losses, or ECL**.
- **30+ DPD loan rate:** open loans with `DPD>=30 / all open loans` at same as-of month. **30+ exposure share:** outstanding contractual receivables of 30+ accounts / all open contractual receivables.
- **Roll rates:** account's bucket at month `t` to precisely the next calendar month `t+1`. `Closed` remains visible rather than excluding payoffs. Each source-bucket month's destination percentages sum to 100% (rounding permitted).
- **Vintage:** 30+ outcome of the original origination cohort at month-on-book 6 or 12. The denominator is the original cohort size (closed loans retained), *not* the active loan count. A cohort must actually have reached its reported month-on-book.
- **90+ DPD:** delinquency proxy, *not* confirmed default, charge-off, expected loss, or regulatory delinquency determination.

## Queries and outputs

1. [`sql/00_quality.sql`](sql/00_quality.sql) validates referential integrity, term coverage, amounts, premature payments, and overpayment.
2. [`sql/10_snapshot.sql`](sql/10_snapshot.sql) builds leak-free FIFO as-of statuses.
3. [`sql/20_kpis.sql`](sql/20_kpis.sql) computes account and receivable exposure measures, with explicit denominators.
4. [`sql/30_roll_rates.sql`](sql/30_roll_rates.sql) produces consecutive-month transition rates and remaining contractual exposure.
5. [`sql/40_vintages.sql`](sql/40_vintages.sql) compares seasoned origination cohorts.

**Results:** [`outputs/REPORT.md`](outputs/REPORT.md) · [`portfolio_kpis.csv`](outputs/portfolio_kpis.csv) · [`roll_rates.csv`](outputs/roll_rates.csv) · [`vintage_cohorts.csv`](outputs/vintage_cohorts.csv) · [`snapshot_sample.csv`](outputs/snapshot_sample.csv).

## Validation

Pytest checks seeded reproducibility, delinquency invariants, 100% transition completeness, immature vintage guards, malformed sources, and a hand-calculated late-payment example. This project is intentionally dependency-light: only SQLite via Python standard library, and pytest for tests. No actual consumer credit account records are committed.

## Use in an analytics interview

> "I defined the population and denominator before calculating delinquency, retained closures in transition analysis, prevented look-ahead by joining only payments received as of the report date, and used an independent test case to verify FIFO days-past-due logic. I would not mistake an amount-due metric for principal, a 90+ DPD flag for default, or a simulation for bank results."

## Scope limitations and next-step production requirements

Real servicing requires regulated source-of-truth ledgers, adjustments and reversals, audited as-of snapshots, more precise payment-allocation waterfalls, risk-attribute history, accounting reconciliation, segmentation, access controls, and formal data contracts. These synthetic findings **cannot** justify a lending policy or claim Affirm-specific behavior.
