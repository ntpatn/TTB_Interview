SELECT
    c.customer_id,
    c.name,
    t.credit_card_number AS card_number,
    AVG(t.transaction_amount) AS avg_transaction_amount
FROM
    data_engineering_1_2.cc_transactions t
JOIN
    data_engineering_1_2.customers c ON t.customer_id = c.customer_id
JOIN
    data_engineering_1_2.merchants m ON t.merchant_id = m.merchant_id
WHERE
    t.transaction_date BETWEEN '2022-01-01' AND '2022-12-31'
    AND (LOWER(m.merchant_name) LIKE '%grab%' OR LOWER(m.merchant_name) LIKE '%food panda%')
GROUP BY
    c.customer_id,
    c.name,
    t.credit_card_number;