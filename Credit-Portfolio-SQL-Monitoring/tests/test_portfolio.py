import csv
import importlib.util
import sqlite3
from pathlib import Path

import pytest

MODULE = Path(__file__).resolve().parents[1] / 'src' / 'build.py'
spec = importlib.util.spec_from_file_location('portfolio_build', MODULE)
build = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build)


def test_deterministic_and_status_invariants(tmp_path):
    out = tmp_path / 'outputs'
    first = build.build(tmp_path / 'portfolio.sqlite', out, loans_per_month=3, seed=42)
    assert first['loans'] == 72
    with sqlite3.connect(tmp_path / 'portfolio.sqlite') as conn:
        assert conn.execute('SELECT COUNT(*) FROM monthly_status').fetchone()[0] > 0
        assert conn.execute('SELECT COUNT(*) FROM monthly_status WHERE past_due_cents < 0 OR remaining_receivables_cents < 0').fetchone()[0] == 0
        assert conn.execute('SELECT COUNT(*) FROM monthly_status WHERE days_past_due >= 30 AND dpd_bucket NOT IN ("30-59", "60-89", "90+")').fetchone()[0] == 0
        assert conn.execute('SELECT COUNT(*) FROM monthly_status WHERE first_unpaid_due_date > as_of').fetchone()[0] == 0
        assert conn.execute('SELECT COUNT(*) FROM monthly_status WHERE past_due_cents = 0 AND days_past_due > 0').fetchone()[0] == 0
        assert conn.execute('SELECT COUNT(*) FROM monthly_status WHERE remaining_receivables_cents = 0 AND dpd_bucket <> "Closed"').fetchone()[0] == 0
        # A 12-month vintage requires twelve observed months (no immature future cohorts).
        assert conn.execute('SELECT COUNT(*) FROM monthly_status WHERE as_of < origination_month').fetchone()[0] == 0
    with (out / 'roll_rates.csv').open(newline='', encoding='utf-8') as fp:
        transitions = list(csv.DictReader(fp))
    for period, from_bucket in {(r['from_as_of'], r['from_bucket']) for r in transitions}:
        total = sum(float(r['transition_pct']) for r in transitions if (r['from_as_of'], r['from_bucket']) == (period, from_bucket))
        assert total == pytest.approx(100, abs=0.05)
    previous = (out / 'portfolio_kpis.csv').read_bytes()
    second = build.build(tmp_path / 'portfolio.sqlite', out, loans_per_month=3, seed=42)
    assert second == first
    assert (out / 'portfolio_kpis.csv').read_bytes() == previous


def test_fifo_dpd_changes_with_late_payment():
    conn = sqlite3.connect(':memory:')
    conn.executescript(build.SCHEMA)
    conn.execute("INSERT INTO loans VALUES (1,'2024-01-01','2024-01',100000,1000,6,'A')")
    for n, due in [(1,'2024-02-20'),(2,'2024-03-20'),(3,'2024-04-20'),
                   (4,'2024-05-20'),(5,'2024-06-20'),(6,'2024-07-20')]:
        conn.execute('INSERT INTO installments VALUES (?,?,?,?)', (1,n,due,20000))
    conn.execute("INSERT INTO calendar_months VALUES ('2024-03-31')")
    conn.execute("INSERT INTO calendar_months VALUES ('2024-04-30')")
    conn.execute("INSERT INTO payments VALUES (1,1,'2024-04-05',20000)")
    conn.executescript(build.sql_text('10_snapshot.sql'))
    mar = conn.execute("SELECT days_past_due,past_due_cents FROM monthly_status WHERE as_of='2024-03-31'").fetchone()
    apr = conn.execute("SELECT days_past_due,past_due_cents FROM monthly_status WHERE as_of='2024-04-30'").fetchone()
    assert mar == (40,40000)   # Oldest unpaid is Feb 20
    assert apr == (41,40000)   # Feb covered on Apr 5, now Mar 20 is oldest unpaid
    conn.close()


def test_bad_source_fails(tmp_path):
    db = sqlite3.connect(':memory:')
    db.executescript(build.SCHEMA)
    db.execute("INSERT INTO loans VALUES (1,'2024-01-01','2024-01',100000,1000,6,'A')")
    with pytest.raises(ValueError, match='installment_count_mismatch'):
        build.ensure_quality(db)
