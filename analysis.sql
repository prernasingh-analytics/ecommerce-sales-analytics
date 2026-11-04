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
