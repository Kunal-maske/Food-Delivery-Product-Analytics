-- =========================================================
-- Food Delivery Product Analytics
-- SQL queries for beginner-friendly product analytics interviews
-- =========================================================

-- 1) Total revenue by city and restaurant
SELECT
    r.city,
    r.name AS restaurant_name,
    SUM(o.order_total) AS revenue,
    COUNT(*) AS order_count
FROM orders o
JOIN restaurants r
    ON r.id = o.restaurant_id
WHERE o.status = 'completed'
GROUP BY r.city, r.name
ORDER BY revenue DESC;

-- 2) Average Order Value (AOV)
SELECT
    ROUND(AVG(order_total), 2) AS avg_order_value
FROM orders
WHERE status = 'completed';

-- 3) Cancellation rate
WITH order_status AS (
    SELECT
        status,
        COUNT(*) AS order_count
    FROM orders
    GROUP BY status
)
SELECT
    ROUND(
        100.0 * SUM(CASE WHEN status = 'cancelled' THEN order_count ELSE 0 END)
        / NULLIF(SUM(order_count), 0),
        2
    ) AS cancellation_rate_pct
FROM order_status;

-- 4) Repeat customers
SELECT
    COUNT(*) AS repeat_customers
FROM (
    SELECT
        user_id,
        COUNT(*) AS order_count
    FROM orders
    GROUP BY user_id
    HAVING COUNT(*) >= 2
) repeated_users;

-- 5) Repeat customers by city
SELECT
    u.city,
    COUNT(*) AS repeat_customers
FROM (
    SELECT
        user_id,
        COUNT(*) AS order_count
    FROM orders
    GROUP BY user_id
    HAVING COUNT(*) >= 2
) repeat_users
JOIN users u
    ON u.id = repeat_users.user_id
GROUP BY u.city
ORDER BY repeat_customers DESC;

-- 6) Revenue by month (CTE + GROUP BY)
WITH monthly_revenue AS (
    SELECT
        DATE_TRUNC('month', order_date)::date AS month_start,
        SUM(order_total) AS monthly_revenue
    FROM orders
    WHERE status = 'completed'
    GROUP BY DATE_TRUNC('month', order_date)::date
)
SELECT
    month_start,
    monthly_revenue
FROM monthly_revenue
ORDER BY month_start;

-- 7) Monthly revenue growth using LAG
WITH monthly_revenue AS (
    SELECT
        DATE_TRUNC('month', order_date)::date AS month_start,
        SUM(order_total) AS monthly_revenue
    FROM orders
    WHERE status = 'completed'
    GROUP BY DATE_TRUNC('month', order_date)::date
),
revenue_growth AS (
    SELECT
        month_start,
        monthly_revenue,
        LAG(monthly_revenue) OVER (ORDER BY month_start) AS previous_month_revenue,
        ROUND(
            100.0 * (monthly_revenue - LAG(monthly_revenue) OVER (ORDER BY month_start))
            / NULLIF(LAG(monthly_revenue) OVER (ORDER BY month_start), 0),
            2
        ) AS month_over_month_growth_pct
    FROM monthly_revenue
)
SELECT *
FROM revenue_growth
ORDER BY month_start;

-- 8) Top restaurants by city using RANK
WITH restaurant_revenue AS (
    SELECT
        r.city,
        r.name AS restaurant_name,
        SUM(o.order_total) AS revenue
    FROM orders o
    JOIN restaurants r
        ON r.id = o.restaurant_id
    WHERE o.status = 'completed'
    GROUP BY r.city, r.name
)
SELECT
    city,
    restaurant_name,
    revenue,
    RANK() OVER (PARTITION BY city ORDER BY revenue DESC) AS city_rank
FROM restaurant_revenue
ORDER BY city, city_rank;

-- 9) Top restaurants by city using DENSE_RANK (handles ties)
WITH restaurant_revenue AS (
    SELECT
        r.city,
        r.name AS restaurant_name,
        SUM(o.order_total) AS revenue
    FROM orders o
    JOIN restaurants r
        ON r.id = o.restaurant_id
    WHERE o.status = 'completed'
    GROUP BY r.city, r.name
)
SELECT
    city,
    restaurant_name,
    revenue,
    DENSE_RANK() OVER (PARTITION BY city ORDER BY revenue DESC) AS dense_rank
FROM restaurant_revenue
ORDER BY city, dense_rank, restaurant_name;

-- 10) Show each user order sequence using ROW_NUMBER
SELECT
    user_id,
    id AS order_id,
    order_date,
    ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY order_date, id) AS order_sequence
FROM orders
WHERE status = 'completed'
ORDER BY user_id, order_sequence;

-- 11) Time between consecutive orders for each user using LAG
WITH user_order_timeline AS (
    SELECT
        user_id,
        order_date,
        LAG(order_date) OVER (PARTITION BY user_id ORDER BY order_date, id) AS previous_order_date
    FROM orders
    WHERE status = 'completed'
)
SELECT
    user_id,
    order_date,
    previous_order_date,
    DATE_PART('day', order_date - previous_order_date) AS days_since_previous_order
FROM user_order_timeline
WHERE previous_order_date IS NOT NULL
ORDER BY user_id, order_date
LIMIT 20;

-- 12) Compare each month with the next month using LEAD
WITH monthly_revenue AS (
    SELECT
        DATE_TRUNC('month', order_date)::date AS month_start,
        SUM(order_total) AS monthly_revenue
    FROM orders
    WHERE status = 'completed'
    GROUP BY DATE_TRUNC('month', order_date)::date
)
SELECT
    month_start,
    monthly_revenue,
    LEAD(monthly_revenue) OVER (ORDER BY month_start) AS next_month_revenue,
    ROUND(
        100.0 * (LEAD(monthly_revenue) OVER (ORDER BY month_start) - monthly_revenue)
        / NULLIF(monthly_revenue, 0),
        2
    ) AS revenue_change_vs_next_month_pct
FROM monthly_revenue
ORDER BY month_start;

-- 13) Best-performing restaurant by city using HAVING
SELECT
    r.city,
    r.name AS restaurant_name,
    SUM(o.order_total) AS revenue
FROM orders o
JOIN restaurants r
    ON r.id = o.restaurant_id
WHERE o.status = 'completed'
GROUP BY r.city, r.name
HAVING SUM(o.order_total) >= 15000
ORDER BY revenue DESC;

-- 14) Average order value by restaurant (join with restaurant details)
SELECT
    r.city,
    r.name AS restaurant_name,
    ROUND(AVG(o.order_total), 2) AS avg_order_value,
    COUNT(*) AS completed_orders
FROM orders o
JOIN restaurants r
    ON r.id = o.restaurant_id
WHERE o.status = 'completed'
GROUP BY r.city, r.name
ORDER BY avg_order_value DESC;

-- 15) Order funnel view: all orders, completed vs cancelled vs refunded
SELECT
    status,
    COUNT(*) AS order_count,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS pct_of_total
FROM orders
GROUP BY status
ORDER BY order_count DESC;
