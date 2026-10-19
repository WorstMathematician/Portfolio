-- Each returned row is one validation. A nonzero count is a blocking failure.
SELECT 'orphan_installments' AS check_name, COUNT(*) AS failures
FROM installments i LEFT JOIN loans l USING(loan_id) WHERE l.loan_id IS NULL
UNION ALL
SELECT 'orphan_payments', COUNT(*)
FROM payments p LEFT JOIN loans l USING(loan_id) WHERE l.loan_id IS NULL
UNION ALL
SELECT 'nonpositive_loan_principal', COUNT(*) FROM loans WHERE principal_cents <= 0
UNION ALL
SELECT 'nonpositive_events',
       (SELECT COUNT(*) FROM installments WHERE amount_cents <= 0) +
       (SELECT COUNT(*) FROM payments WHERE amount_cents <= 0)
UNION ALL
SELECT 'payment_before_origination', COUNT(*)
FROM payments p JOIN loans l USING(loan_id) WHERE p.payment_date < l.origination_date
UNION ALL
SELECT 'installment_count_mismatch', COUNT(*) FROM loans l
WHERE (SELECT COUNT(*) FROM installments i WHERE i.loan_id=l.loan_id) <> l.term_months
UNION ALL
SELECT 'overpayment_total', COUNT(*) FROM loans l
WHERE (SELECT COALESCE(SUM(amount_cents),0) FROM payments p WHERE p.loan_id=l.loan_id) >
      (SELECT COALESCE(SUM(amount_cents),0) FROM installments i WHERE i.loan_id=l.loan_id);
