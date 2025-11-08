-- Demo SQL Queries for Smart Data Exploration Agent
-- Each block includes a natural-language prompt and the SQL used.
-- Assumes a table named `sales` with columns:
-- transaction_id TEXT, customer_id TEXT, product_category TEXT, quantity INT, price REAL, date TEXT, revenue REAL

/* Prompt: What's the total revenue in 2024 by month? */
SELECT strftime('%Y-%m', date) AS year_month,
       SUM(revenue) AS total_revenue
FROM sales
GROUP BY year_month
ORDER BY year_month;

/* Prompt: Who are the top 5 customers by total revenue? */
SELECT customer_id,
       SUM(revenue) AS total_revenue
FROM sales
GROUP BY customer_id
ORDER BY total_revenue DESC
LIMIT 5;

/* Prompt: What is the revenue contribution of each product category? */
SELECT product_category,
       SUM(revenue) AS category_revenue,
       ROUND(100.0 * SUM(revenue) / (SELECT SUM(revenue) FROM sales), 2) AS pct_of_total
FROM sales
GROUP BY product_category
ORDER BY category_revenue DESC;

/* Prompt: What's the average order value (AOV)? */
SELECT ROUND(AVG(revenue), 2) AS average_order_value
FROM sales;

/* Prompt: How many repeat customers (with >= 2 transactions) do we have? */
WITH counts AS (
  SELECT customer_id, COUNT(*) AS num_orders
  FROM sales
  GROUP BY customer_id
)
SELECT COUNT(*) AS repeat_customers
FROM counts
WHERE num_orders >= 2;

/* Prompt: Show revenue by week number */
SELECT strftime('%Y-%W', date) AS year_week,
       SUM(revenue) AS total_revenue
FROM sales
GROUP BY year_week
ORDER BY year_week;

/* Prompt: Give me daily revenue for the last 14 days in the dataset */
WITH max_day AS (
  SELECT DATE(MAX(date)) AS max_date FROM sales
)
SELECT DATE(date) AS day, SUM(revenue) AS total_revenue
FROM sales, max_day
WHERE DATE(date) > DATE(max_day.max_date, '-14 days')
GROUP BY day
ORDER BY day;

/* Prompt: Average revenue per customer in 2024 */
SELECT ROUND(SUM(revenue) * 1.0 / COUNT(DISTINCT customer_id), 2) AS avg_rev_per_customer
FROM sales
WHERE strftime('%Y', date) = '2024';

/* Prompt: What product category has the highest average order value? */
SELECT product_category,
       ROUND(AVG(revenue), 2) AS avg_order_value
FROM sales
GROUP BY product_category
ORDER BY avg_order_value DESC
LIMIT 1;
