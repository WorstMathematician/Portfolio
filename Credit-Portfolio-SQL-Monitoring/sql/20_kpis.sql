-- Delinquency rate denominator excludes fully paid/closed accounts.
-- Exposure denominator is remaining contractual receivables, INCLUDING scheduled interest.
SELECT as_of,
       SUM(CASE WHEN remaining_receivables_cents > 0 THEN 1 ELSE 0 END) AS open_accounts,
       SUM(CASE WHEN remaining_receivables_cents > 0 AND days_past_due >= 30 THEN 1 ELSE 0 END)
          AS dpd_30_plus_accounts,
       ROUND(100.0 * SUM(CASE WHEN remaining_receivables_cents > 0 AND days_past_due >= 30 THEN 1 ELSE 0 END)
          / NULLIF(SUM(CASE WHEN remaining_receivables_cents > 0 THEN 1 ELSE 0 END),0), 4)
          AS dpd_30_plus_pct,
       SUM(remaining_receivables_cents) AS open_receivables_cents,
       SUM(CASE WHEN days_past_due >= 30 THEN remaining_receivables_cents ELSE 0 END)
          AS dpd_30_plus_receivables_cents,
       ROUND(100.0 * SUM(CASE WHEN days_past_due >= 30 THEN remaining_receivables_cents ELSE 0 END)
          / NULLIF(SUM(remaining_receivables_cents),0), 4)
          AS dpd_30_plus_balance_pct,
       SUM(past_due_cents) AS overdue_contractual_cents,
       SUM(CASE WHEN days_past_due >= 90 THEN 1 ELSE 0 END) AS dpd_90_plus_accounts
FROM monthly_status GROUP BY as_of ORDER BY as_of;
