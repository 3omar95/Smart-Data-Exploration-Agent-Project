import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import os

BASE_DIR = os.getcwd()
DB_PATH = os.path.join(BASE_DIR, 'sales_demo.db')
OUT_DIR = os.path.join(BASE_DIR, 'outputs')
os.makedirs(OUT_DIR, exist_ok=True)

QUERIES = {
    'revenue_by_month': '''
        SELECT strftime('%Y-%m', date) AS year_month, SUM(revenue) AS total_revenue
        FROM sales
        GROUP BY year_month
        ORDER BY year_month;
    ''',
    'top5_customers': '''
        SELECT customer_id, SUM(revenue) AS total_revenue
        FROM sales
        GROUP BY customer_id
        ORDER BY total_revenue DESC
        LIMIT 5;
    ''',
    'category_contribution': '''
        SELECT product_category, SUM(revenue) AS category_revenue
        FROM sales
        GROUP BY product_category
        ORDER BY category_revenue DESC;
    ''',
    'aov': '''
        SELECT ROUND(AVG(revenue), 2) AS average_order_value
        FROM sales;
    ''',
    'repeat_customers': '''
        WITH counts AS (
          SELECT customer_id, COUNT(*) AS num_orders
          FROM sales
          GROUP BY customer_id
        )
        SELECT COUNT(*) AS repeat_customers
        FROM counts
        WHERE num_orders >= 2;
    ''',
    'revenue_by_week': '''
        SELECT strftime('%Y-%W', date) AS year_week, SUM(revenue) AS total_revenue
        FROM sales
        GROUP BY year_week
        ORDER BY year_week;
    ''',
    'last_14_days': '''
        WITH max_day AS (
          SELECT DATE(MAX(date)) AS max_date FROM sales
        )
        SELECT DATE(date) AS day, SUM(revenue) AS total_revenue
        FROM sales, max_day
        WHERE DATE(date) > DATE(max_day.max_date, '-14 days')
        GROUP BY day
        ORDER BY day;
    ''',
    'avg_rev_per_customer_2024': '''
        SELECT ROUND(SUM(revenue) * 1.0 / COUNT(DISTINCT customer_id), 2) AS avg_rev_per_customer
        FROM sales
        WHERE strftime('%Y', date) = '2024';
    ''',
    'best_aov_category': '''
        SELECT product_category, ROUND(AVG(revenue), 2) AS avg_order_value
        FROM sales
        GROUP BY product_category
        ORDER BY avg_order_value DESC
        LIMIT 1;
    '''
}

def run_query(conn, sql):
    return pd.read_sql_query(sql, conn)

def save_table(df, name):
    out_csv = os.path.join(OUT_DIR, f"{name}.csv")
    df.to_csv(out_csv, index=False)
    print(f"[Saved] {out_csv}")

def plot_series(df, x, y, title, filename, kind='line'):
    plt.figure()
    if kind == 'bar':
        df.plot(x=x, y=y, kind='bar', legend=False)
    else:
        df.plot(x=x, y=y, kind='line', legend=False)
    plt.title(title)
    plt.xlabel(x)
    plt.ylabel(y)
    out_png = os.path.join(OUT_DIR, f"{filename}.png")
    plt.savefig(out_png, bbox_inches='tight')
    plt.close()
    print(f"[Chart] {out_png}")

def main():
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError('sales_demo.db not found. Build it before running.')
    conn = sqlite3.connect(DB_PATH)

    # 1) Revenue by month
    df_month = run_query(conn, QUERIES['revenue_by_month'])
    save_table(df_month, 'revenue_by_month')
    if not df_month.empty:
        plot_series(df_month, 'year_month', 'total_revenue', 'Revenue by Month', 'revenue_by_month', kind='line')

    # 2) Top 5 customers
    df_top5 = run_query(conn, QUERIES['top5_customers'])
    save_table(df_top5, 'top5_customers')
    if not df_top5.empty:
        plot_series(df_top5, 'customer_id', 'total_revenue', 'Top 5 Customers by Revenue', 'top5_customers', kind='bar')

    # 3) Category contribution
    df_cat = run_query(conn, QUERIES['category_contribution'])
    save_table(df_cat, 'category_contribution')
    if not df_cat.empty:
        plot_series(df_cat, 'product_category', 'category_revenue', 'Revenue by Product Category', 'category_contribution', kind='bar')

    # 4) AOV
    df_aov = run_query(conn, QUERIES['aov'])
    save_table(df_aov, 'aov')

    # 5) Repeat customers
    df_repeat = run_query(conn, QUERIES['repeat_customers'])
    save_table(df_repeat, 'repeat_customers')

    # 6) Revenue by week
    df_week = run_query(conn, QUERIES['revenue_by_week'])
    save_table(df_week, 'revenue_by_week')
    if not df_week.empty:
        plot_series(df_week, 'year_week', 'total_revenue', 'Revenue by Week', 'revenue_by_week', kind='line')

    # 7) Last 14 days
    df_last14 = run_query(conn, QUERIES['last_14_days'])
    save_table(df_last14, 'last_14_days')
    if not df_last14.empty:
        plot_series(df_last14, 'day', 'total_revenue', 'Daily Revenue (Last 14 Days)', 'last_14_days', kind='line')

    # 8) Avg revenue per customer (2024)
    df_avg_cust = run_query(conn, QUERIES['avg_rev_per_customer_2024'])
    save_table(df_avg_cust, 'avg_rev_per_customer_2024')

    # 9) Best AOV category
    df_best = run_query(conn, QUERIES['best_aov_category'])
    save_table(df_best, 'best_aov_category')

    conn.close()
    print('[Done] Outputs saved to:', OUT_DIR)

if __name__ == '__main__':
    main()
