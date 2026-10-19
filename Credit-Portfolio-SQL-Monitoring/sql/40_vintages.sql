-- Report explicit month-on-book; include only observed snapshots at month 6 or 12.
WITH seasoned AS (
  SELECT s.*, (CAST(SUBSTR(as_of,1,4) AS INTEGER)-CAST(SUBSTR(origination_month,1,4) AS INTEGER))*12
       + CAST(SUBSTR(as_of,6,2) AS INTEGER)-CAST(SUBSTR(origination_month,6,2) AS INTEGER)
       AS months_on_book FROM monthly_status s
)
SELECT origination_month, months_on_book, risk_tier,
       COUNT(*) AS originated_loans_in_cohort,
       SUM(CASE WHEN days_past_due >= 30 THEN 1 ELSE 0 END) AS dpd_30_plus_accounts,
       ROUND(100.0 * SUM(CASE WHEN days_past_due >= 30 THEN 1 ELSE 0 END) / COUNT(*),4)
         AS dpd_30_plus_pct_of_original_cohort,
       SUM(remaining_receivables_cents) AS remaining_receivables_cents
FROM seasoned WHERE months_on_book IN (6,12)
GROUP BY origination_month, months_on_book, risk_tier
ORDER BY origination_month, months_on_book, risk_tier;
