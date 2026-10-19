"""Deterministic synthetic lending portfolio and SQLite monitoring extracts.

Only fictional accounts are generated. All amounts use integer cents.
"""
import argparse
import csv
import random
import sqlite3
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = """
PRAGMA foreign_keys = ON;
CREATE TABLE loans (
    loan_id INTEGER PRIMARY KEY,
    origination_date TEXT NOT NULL,
    origination_month TEXT NOT NULL,
    principal_cents INTEGER NOT NULL CHECK(principal_cents > 0),
    apr_bps INTEGER NOT NULL CHECK(apr_bps BETWEEN 0 AND 5000),
    term_months INTEGER NOT NULL CHECK(term_months IN (6, 12)),
    risk_tier TEXT NOT NULL CHECK(risk_tier IN ('A','B','C'))
);
CREATE TABLE installments (
    loan_id INTEGER NOT NULL REFERENCES loans(loan_id),
    installment_number INTEGER NOT NULL,
    due_date TEXT NOT NULL,
    amount_cents INTEGER NOT NULL CHECK(amount_cents > 0),
    PRIMARY KEY (loan_id, installment_number)
);
CREATE TABLE payments (
    payment_id INTEGER PRIMARY KEY,
    loan_id INTEGER NOT NULL REFERENCES loans(loan_id),
    payment_date TEXT NOT NULL,
    amount_cents INTEGER NOT NULL CHECK(amount_cents > 0)
);
CREATE TABLE calendar_months(as_of TEXT PRIMARY KEY);
CREATE INDEX idx_inst_loan_date ON installments(loan_id, due_date);
CREATE INDEX idx_pay_loan_date ON payments(loan_id, payment_date);
"""


def month_at(start, offset):
    index = start.year * 12 + start.month - 1 + offset
    return date(index // 12, index % 12 + 1, 1)


def month_end(start):
    next_month = month_at(start, 1)
    return next_month - timedelta(days=1)


def seed_database(conn, loans_per_month=100, seed=20261018):
    """Fixed seed and scheduled installments; a payment may be late or never arrive."""
    if loans_per_month <= 0:
        raise ValueError('loans_per_month must be positive')
    rng = random.Random(seed)
    conn.executescript(SCHEMA)
    loan_id = 0
    payment_id = 0
    for offset in range(24):
        orig = month_at(date(2023, 1, 1), offset)
        for _ in range(loans_per_month):
            loan_id += 1
            tier = rng.choices(['A', 'B', 'C'], weights=[55, 30, 15])[0]
            principal = rng.randint(400, 4500) * 100
            term = rng.choice([6, 12])
            apr_bps = {'A': 950, 'B': 1650, 'C': 2600}[tier]
            conn.execute('INSERT INTO loans VALUES (?,?,?,?,?,?,?)', (
                loan_id, orig.isoformat(), orig.strftime('%Y-%m'), principal,
                apr_bps, term, tier
            ))
            # Demonstration installment schedule, NOT a production amortization engine.
            total_interest = (principal * apr_bps * term + 60000) // 120000
            total_due = principal + total_interest
            equal, remainder = divmod(total_due, term)
            for n in range(1, term + 1):
                due = month_at(orig, n).replace(day=20)
                amount = equal + (remainder if n == term else 0)
                conn.execute('INSERT INTO installments VALUES (?,?,?,?)', (
                    loan_id, n, due.isoformat(), amount
                ))
                payment_chance = {'A': 0.985, 'B': 0.94, 'C': 0.83}[tier]
                if rng.random() >= payment_chance:
                    continue
                delay = rng.choices([-3, 1, 8, 21, 44, 76],
                                    weights=[35, 30, 15, 10, 7, 3])[0]
                payment_date = due + timedelta(days=delay)
                payment_id += 1
                conn.execute('INSERT INTO payments VALUES (?,?,?,?)', (
                    payment_id, loan_id, payment_date.isoformat(), amount
                ))
    for offset in range(30):
        month = month_at(date(2023, 1, 1), offset)
        conn.execute('INSERT INTO calendar_months VALUES (?)',
                     (month_end(month).isoformat(),))
    conn.commit()


def sql_text(name):
    return (ROOT / 'sql' / name).read_text(encoding='utf-8')


def write_csv(conn, query, filepath):
    result = conn.execute(query)
    headers = [item[0] for item in result.description]
    rows = result.fetchall()
    with filepath.open('w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(rows)
    return rows


def ensure_quality(conn):
    checks = conn.execute(sql_text('00_quality.sql')).fetchall()
    failing = [(name, count) for name, count in checks if count]
    if failing:
        raise ValueError(f'Portfolio quality checks failed: {failing}')
    return checks


def build(db_path, out_dir, loans_per_month=100, seed=20261018):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    db_path = Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    if db_path.exists():
        db_path.unlink()
    with sqlite3.connect(db_path) as conn:
        seed_database(conn, loans_per_month=loans_per_month, seed=seed)
        ensure_quality(conn)
        conn.executescript(sql_text('10_snapshot.sql'))
        outputs = {
            'portfolio_kpis.csv': sql_text('20_kpis.sql'),
            'roll_rates.csv': sql_text('30_roll_rates.sql'),
            'vintage_cohorts.csv': sql_text('40_vintages.sql'),
            'snapshot_sample.csv': """SELECT as_of, loan_id, origination_month,
                risk_tier, dpd_bucket, days_past_due, past_due_cents,
                remaining_receivables_cents FROM monthly_status
                WHERE as_of = '2025-06-30' ORDER BY loan_id LIMIT 20""",
        }
        for filename, query in outputs.items():
            write_csv(conn, query, out_dir / filename)
        loans = conn.execute('SELECT COUNT(*) FROM loans').fetchone()[0]
        installments = conn.execute('SELECT COUNT(*) FROM installments').fetchone()[0]
        payments = conn.execute('SELECT COUNT(*) FROM payments').fetchone()[0]
        statuses = conn.execute('SELECT COUNT(*) FROM monthly_status').fetchone()[0]
        # Use the exact same published query for the executive summary.
        rows = conn.execute(sql_text('20_kpis.sql')).fetchall()
        final = rows[-1]
    report = f"""# Synthetic loan portfolio: reproducible SQL results

> **Simulation, not observed lending performance.** Seed `{seed}`, {loans_per_month} fictional loans originated per month. Never treat scenario figures as historical portfolio outcomes.

- Loans: **{loans:,}** (24 origination months, Jan 2023-Dec 2024)
- Contractual installments: **{installments:,}**; recorded payments: **{payments:,}**
- Month-end loan snapshots: **{statuses:,}**, Jan 2023-Jun 2025
- Latest as-of: **{final[0]}**, open accounts **{final[1]:,}**; 30+ DPD open accounts **{final[2]:,}**
- Latest 30+ DPD rate (open-account denominator): **{final[3]:.2f}%**
- Latest 30+ DPD contractual receivable exposure share: **{final[6]:.2f}%**

**Definitions:** DPD counts calendar days from the *earliest due installment not fully covered by cumulative, as-of-date payments*, allocated oldest-first. 30+ rate = open accounts with DPD >= 30 divided by all open accounts. Receivables include scheduled interest and are *not* principal outstanding, expected credit losses, or a GAAP loan balance. Roll rates require consecutive snapshots of the same account; closures are retained as an explicit destination. Vintage tables do not report unseasoned cohorts at 6/12 months.

The CSVs and SQLite DB are re-created by `python src/build.py`. No real people, customers, accounts, or bank data were used.
"""
    (out_dir / 'REPORT.md').write_text(report, encoding='utf-8')
    return {'loans': loans, 'installments': installments, 'payments': payments,
            'snapshots': statuses, 'last': final}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--db', default=str(ROOT / 'outputs' / 'portfolio.sqlite'))
    parser.add_argument('--output', default=str(ROOT / 'outputs'))
    parser.add_argument('--loans-per-month', type=int, default=100)
    parser.add_argument('--seed', type=int, default=20261018)
    args = parser.parse_args()
    print(build(args.db, args.output, args.loans_per_month, args.seed))


if __name__ == '__main__':
    main()
