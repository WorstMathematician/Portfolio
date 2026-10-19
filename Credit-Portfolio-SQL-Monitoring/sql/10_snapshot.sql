-- Month-end as-of snapshots. Future installments and future cash never enter as-of calculations.
-- FIFO: payments are assigned to the oldest contractual installments first.
-- All balances are integer cents; this is contractual receivables, NOT principal accounting balance.
CREATE TABLE monthly_status AS
WITH calendar_loan AS (
  SELECT c.as_of, l.loan_id, l.origination_month, l.origination_date,
         l.risk_tier,
         (SELECT SUM(i.amount_cents) FROM installments i WHERE i.loan_id = l.loan_id)
             AS contractual_total_cents,
         (SELECT COALESCE(SUM(i.amount_cents),0) FROM installments i
             WHERE i.loan_id = l.loan_id AND i.due_date <= c.as_of)
             AS scheduled_to_date_cents,
         (SELECT COALESCE(SUM(p.amount_cents),0) FROM payments p
             WHERE p.loan_id = l.loan_id AND p.payment_date <= c.as_of)
             AS paid_to_date_cents
    FROM calendar_months c
    JOIN loans l ON l.origination_date <= c.as_of
), unpaid AS (
  SELECT s.*,
         (SELECT MIN(i.due_date) FROM installments i
           WHERE i.loan_id = s.loan_id AND i.due_date <= s.as_of
             AND (SELECT SUM(j.amount_cents) FROM installments j
                  WHERE j.loan_id = i.loan_id AND j.due_date <= i.due_date)
                 > s.paid_to_date_cents
         ) AS first_unpaid_due_date
  FROM calendar_loan s
), measures AS (
  SELECT u.*,
         MAX(0, contractual_total_cents - paid_to_date_cents)
             AS remaining_receivables_cents,
         MAX(0, scheduled_to_date_cents - paid_to_date_cents)
             AS past_due_cents,
         CASE WHEN first_unpaid_due_date IS NULL THEN 0
              ELSE CAST(julianday(as_of)-julianday(first_unpaid_due_date) AS INTEGER)
         END AS days_past_due
  FROM unpaid u
)
SELECT as_of, loan_id, origination_month, risk_tier,
       contractual_total_cents, scheduled_to_date_cents, paid_to_date_cents,
       remaining_receivables_cents, past_due_cents, first_unpaid_due_date,
       days_past_due,
       CASE WHEN remaining_receivables_cents = 0 THEN 'Closed'
            WHEN days_past_due >= 90 THEN '90+'
            WHEN days_past_due >= 60 THEN '60-89'
            WHEN days_past_due >= 30 THEN '30-59'
            WHEN days_past_due > 0 THEN '1-29'
            ELSE 'Current' END AS dpd_bucket
FROM measures;
CREATE UNIQUE INDEX idx_status_loan_month ON monthly_status(loan_id, as_of);
CREATE INDEX idx_status_month_bucket ON monthly_status(as_of, dpd_bucket);
