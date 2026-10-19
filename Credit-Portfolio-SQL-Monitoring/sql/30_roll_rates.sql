-- Link a loan's month t state to precisely the following calendar month.
-- Do not silently exclude loans that pay off; Closed is a meaningful terminal state.
WITH transitions AS (
  SELECT s.as_of AS from_as_of,
         n.as_of AS to_as_of, s.loan_id,
         s.dpd_bucket AS from_bucket, n.dpd_bucket AS to_bucket,
         s.remaining_receivables_cents AS from_receivables_cents
  FROM monthly_status s
  JOIN monthly_status n ON n.loan_id = s.loan_id
     AND n.as_of = DATE(s.as_of, 'start of month', '+2 months', '-1 day')
  WHERE s.remaining_receivables_cents > 0
), groups AS (
  SELECT from_as_of, from_bucket, to_bucket, COUNT(*) AS loans,
         SUM(from_receivables_cents) AS from_receivables_cents
  FROM transitions GROUP BY from_as_of, from_bucket, to_bucket
)
SELECT from_as_of, from_bucket, to_bucket, loans, from_receivables_cents,
       ROUND(100.0 * loans / NULLIF(SUM(loans) OVER (
          PARTITION BY from_as_of, from_bucket),0),4) AS transition_pct
FROM groups ORDER BY from_as_of, from_bucket, to_bucket;
