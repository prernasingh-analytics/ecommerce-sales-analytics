-- Import source CSVs as orders, order_items, products, customers, category_translation.
-- This query excludes freight and limits to delivered orders.
SELECT substr(o.order_purchase_timestamp,1,7) AS purchase_month,
       ROUND(SUM(i.price),2) AS delivered_item_revenue_brl,
       COUNT(DISTINCT o.order_id) AS orders, COUNT(*) AS items
FROM orders o JOIN order_items i ON o.order_id=i.order_id
WHERE o.order_status='delivered'
GROUP BY 1 ORDER BY 1;

SELECT COALESCE(t.product_category_name_english,p.product_category_name,'Unknown') AS category,
       ROUND(SUM(i.price),2) AS item_revenue_brl
FROM orders o JOIN order_items i ON o.order_id=i.order_id
LEFT JOIN products p ON p.product_id=i.product_id
LEFT JOIN category_translation t ON t.product_category_name=p.product_category_name
WHERE o.order_status='delivered' GROUP BY 1 ORDER BY 2 DESC LIMIT 10;


-- QUERY 3: Customer Purchase Frequency and Repeat Purchase Rate
-- Skills: CTE, JOIN, COUNT DISTINCT, CASE WHEN

WITH customer_orders AS (
    SELECT
        c.customer_unique_id,
        COUNT(DISTINCT o.order_id) AS total_orders
    FROM orders o
    JOIN customers c
        ON o.customer_id = c.customer_id
    WHERE o.order_status = 'delivered'
    GROUP BY c.customer_unique_id
)
SELECT
    COUNT(*) AS total_customers,
    SUM(CASE WHEN total_orders = 1 THEN 1 ELSE 0 END)
        AS one_time_customers,
    SUM(CASE WHEN total_orders >= 2 THEN 1 ELSE 0 END)
        AS repeat_customers,
    ROUND(
        100.0 * SUM(CASE WHEN total_orders >= 2 THEN 1 ELSE 0 END)
        / NULLIF(COUNT(*), 0),
        2
    ) AS repeat_customer_percentage
FROM customer_orders;



-- QUERY 4: Customer Segmentation
-- Skills: CTEs, JOINs, CASE WHEN, date calculations
-- Matches the Python dashboard's recency and frequency logic.

WITH snapshot AS (
    SELECT
        datetime(MAX(order_purchase_timestamp), '+1 day') AS snapshot_time
    FROM orders
    WHERE order_status = 'delivered'
),
customer_summary AS (
    SELECT
        c.customer_unique_id,
        COUNT(DISTINCT o.order_id) AS purchase_frequency,
        MAX(o.order_purchase_timestamp) AS last_purchase,
        SUM(i.price) AS total_spent
    FROM orders o
    JOIN customers c
        ON o.customer_id = c.customer_id
    JOIN order_items i
        ON o.order_id = i.order_id
    WHERE o.order_status = 'delivered'
    GROUP BY c.customer_unique_id
),
segmented AS (
    SELECT
        cs.customer_unique_id,
        cs.total_spent,
        CASE
            WHEN cs.purchase_frequency >= 2
                 AND CAST(
                     julianday(s.snapshot_time) -
                     julianday(cs.last_purchase)
                     AS INTEGER
                 ) <= 90
                THEN 'Recent Repeat Buyers'
            WHEN cs.purchase_frequency >= 2
                THEN 'Other Repeat Buyers'
            WHEN CAST(
                     julianday(s.snapshot_time) -
                     julianday(cs.last_purchase)
                     AS INTEGER
                 ) <= 90
                THEN 'Recent One-Time Buyers'
            ELSE 'Older One-Time Buyers'
        END AS customer_segment
    FROM customer_summary cs
    CROSS JOIN snapshot s
)
SELECT
    customer_segment,
    COUNT(*) AS customers,
    ROUND(SUM(total_spent), 2) AS revenue_brl
FROM segmented
GROUP BY customer_segment
ORDER BY customers DESC;


-- QUERY 5: Monthly Revenue Growth
-- Skills: CTE, LAG window function, percentage change

WITH monthly_sales AS (
    SELECT
        SUBSTR(o.order_purchase_timestamp, 1, 7)
            AS purchase_month,
        SUM(i.price) AS revenue
    FROM orders o
    JOIN order_items i
        ON o.order_id = i.order_id
    WHERE o.order_status = 'delivered'
    GROUP BY 1
),
monthly_growth AS (
    SELECT
        purchase_month,
        revenue,
        LAG(revenue) OVER (ORDER BY purchase_month)
            AS previous_month_revenue
    FROM monthly_sales
)
SELECT
    purchase_month,
    ROUND(revenue, 2) AS revenue_brl,
    ROUND(
        100.0 * (revenue - previous_month_revenue)
        / NULLIF(previous_month_revenue, 0),
        2
    ) AS monthly_growth_percentage
FROM monthly_growth
ORDER BY purchase_month;


-- QUERY 6: Top 3 Product Categories in Each Customer State
-- Skills: Multiple JOINs, CTE, DENSE_RANK window function

WITH state_category_sales AS (
    SELECT
        c.customer_state,
        COALESCE(
            t.product_category_name_english,
            p.product_category_name,
            'Unknown'
        ) AS category,
        SUM(i.price) AS revenue
    FROM orders o
    JOIN customers c
        ON o.customer_id = c.customer_id
    JOIN order_items i
        ON o.order_id = i.order_id
    LEFT JOIN products p
        ON i.product_id = p.product_id
    LEFT JOIN category_translation t
        ON p.product_category_name =
           t.product_category_name
    WHERE o.order_status = 'delivered'
    GROUP BY c.customer_state, category
),
ranked_categories AS (
    SELECT
        customer_state,
        category,
        revenue,
        DENSE_RANK() OVER (
            PARTITION BY customer_state
            ORDER BY revenue DESC
        ) AS category_rank
    FROM state_category_sales
)
SELECT
    customer_state,
    category,
    ROUND(revenue, 2) AS revenue_brl,
    category_rank
FROM ranked_categories
WHERE category_rank <= 3
ORDER BY customer_state, category_rank;

