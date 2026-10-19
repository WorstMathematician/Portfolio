# Synthetic loan portfolio: reproducible SQL results

> **Simulation, not observed lending performance.** Seed `20261018`, 100 fictional loans originated per month. Never treat scenario figures as historical portfolio outcomes.

- Loans: **2,400** (24 origination months, Jan 2023-Dec 2024)
- Contractual installments: **21,636**; recorded payments: **20,540**
- Month-end loan snapshots: **44,400**, Jan 2023-Jun 2025
- Latest as-of: **2025-06-30**, open accounts **976**; 30+ DPD open accounts **688**
- Latest 30+ DPD rate (open-account denominator): **70.49%**
- Latest 30+ DPD contractual receivable exposure share: **60.33%**

**Definitions:** DPD counts calendar days from the *earliest due installment not fully covered by cumulative, as-of-date payments*, allocated oldest-first. 30+ rate = open accounts with DPD >= 30 divided by all open accounts. Receivables include scheduled interest and are *not* principal outstanding, expected credit losses, or a GAAP loan balance. Roll rates require consecutive snapshots of the same account; closures are retained as an explicit destination. Vintage tables do not report unseasoned cohorts at 6/12 months.

The CSVs and SQLite DB are re-created by `python src/build.py`. No real people, customers, accounts, or bank data were used.
