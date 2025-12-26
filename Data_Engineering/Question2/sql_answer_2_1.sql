SELECT DISTINCT
    c.customer_id,
    c.name
FROM
    data_engineering_1_2.customers c
JOIN (
    SELECT
        customer_id,
        point_balance
    FROM
        data_engineering_1_2.point_balance pb1
    WHERE
        point_balance_date = (
            SELECT
                MAX(point_balance_date)
            FROM
                data_engineering_1_2.point_balance pb2
            WHERE
                pb2.customer_id = pb1.customer_id
        )
) latest_pb ON c.customer_id = latest_pb.customer_id
JOIN
    data_engineering_1_2.promotions p ON latest_pb.point_balance >= p.req_point
    AND LOWER(p.promotion_name) LIKE '%grab%'
ORDER BY
    c.customer_id;