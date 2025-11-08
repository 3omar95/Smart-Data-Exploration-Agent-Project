import os
import sqlite3

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

import streamlit as st

from llm_router import LLMRouter
from custom_agent import SmartDataAgent


def visualize_with_seaborn(df: pd.DataFrame):
    try:
        if df.empty:
            st.warning("No data returned.")
            return

        st.subheader("Choose visualization options")

        x_col = st.selectbox("X Axis", df.columns)
        y_col = st.selectbox("Y Axis (optional)", list(df.columns))
        chart_type = st.selectbox(
            "Chart Type",
            ["bar", "line", "scatter", "histogram", "box"]
        )
        if st.button("Render Chart"):
            fig, ax = plt.subplots(figsize=(8, 5))

            if chart_type == "bar":
                sns.barplot(data=df, x=x_col, y=y_col, ax=ax)
            elif chart_type == "line":
                sns.lineplot(data=df, x=x_col, y=y_col, ax=ax)
            elif chart_type == "scatter":
                sns.scatterplot(data=df, x=x_col, y=y_col, ax=ax)
            elif chart_type == "histogram":
                sns.histplot(data=df, x=x_col, ax=ax, kde=True)
            elif chart_type == "box":
                sns.boxplot(data=df, x=x_col, y=y_col, ax=ax)

            plt.xticks(rotation=30)
            st.pyplot(fig)

    except Exception as e:
        st.error(f"Failed to visualize: {e}")

BASE_DIR = os.getcwd()
DB_PATH = os.path.join(BASE_DIR, 'sales_demo.db')

st.set_page_config(page_title='Smart Data Exploration Agent – Demo', layout='wide')
st.title('🧠 Smart Data Exploration Agent – Demo (SQLite)')

# Provider + Model selection
st.sidebar.header('LLM Settings')
provider = st.sidebar.selectbox('Provider', ['qwen', 'ntqai', 'openai', 'anthropic'], index=0)
default_openai = 'gpt-4o-mini'
default_anthropic = 'claude-3-5-sonnet-latest'
default_qwen = 'CodeQwen1.5-7B-Chat'
default_ntqai = 'Nxcode-CQ-7B-orpo'
model = st.sidebar.text_input(
    'Model name',
    value=(
        default_openai if provider == 'openai'
        else default_anthropic if provider == 'anthropic'
        else default_qwen if provider == 'qwen'
        else default_ntqai
    )
)
st.sidebar.caption('Set API keys as env vars: OPENAI_API_KEY or ANTHROPIC_API_KEY')

if not os.path.exists(DB_PATH):
    st.error("Database not found. Please ensure 'sales_demo.db' exists in the same folder.")
    st.stop()

conn = sqlite3.connect(DB_PATH)

st.subheader('⚡ Quick Queries')
QUERY_MAP = {
    'Revenue by month': "SELECT strftime('%Y-%m', date) AS year_month, SUM(revenue) AS total_revenue FROM sales GROUP BY year_month ORDER BY year_month;",
    'Top 5 customers': "SELECT customer_id, SUM(revenue) AS total_revenue FROM sales GROUP BY customer_id ORDER BY total_revenue DESC LIMIT 5;",
    'Category contribution': "SELECT product_category, SUM(revenue) AS category_revenue FROM sales GROUP BY product_category ORDER BY category_revenue DESC;",
    'AOV': "SELECT ROUND(AVG(revenue), 2) AS average_order_value FROM sales;",
    'Revenue by week': "SELECT strftime('%Y-%W', date) AS year_week, SUM(revenue) AS total_revenue FROM sales GROUP BY year_week ORDER BY year_week;",
    'Last 14 days': "WITH max_day AS (SELECT DATE(MAX(date)) AS max_date FROM sales) SELECT DATE(date) AS day, SUM(revenue) AS total_revenue FROM sales, max_day WHERE DATE(date) > DATE(max_day.max_date, '-14 days') GROUP BY day ORDER BY day;"
}

choice = st.selectbox('Pick a query', list(QUERY_MAP.keys()))
sql_quick = QUERY_MAP[choice]
st.code(sql_quick, language='sql')
if st.button('Run quick query'):
    df_quick = pd.read_sql_query(sql_quick, conn)
    st.session_state['df_quick'] = df_quick
    st.session_state['show_quick_viz'] = False

if 'df_quick' in st.session_state:
    st.dataframe(st.session_state['df_quick'])
    if st.button('Visualize quick query results'):
        st.session_state['show_quick_viz'] = True

if st.session_state.get('show_quick_viz', False):
    visualize_with_seaborn(st.session_state['df_quick'])
    if st.button('Hide Visualization'):
        st.session_state['show_quick_viz'] = False

st.markdown('---')
st.subheader('🗣️ Natural Language → SQL via LLM')

nl = st.text_area("Ask a data question (e.g., 'Show revenue by product category in 2024 Q1')")

col1, col2 = st.columns(2)
with col1:
    if st.button('Generate SQL'):
        if not nl.strip():
            st.warning('Please enter a question.')
        else:
            try:
                router = LLMRouter(provider=provider, model=model)
                agent = SmartDataAgent(
                    con=conn,
                    router=router
                )
                df, sql_generated = agent.ask(nl)
                st.success('Generated SQL:')
                st.code(sql_generated, language='sql')
                st.session_state['generated_sql'] = sql_generated
                st.session_state['df'] = df
            except Exception as e:
                st.error(f'Failed to generate SQL: {e}')

with col2:
    if st.button('Run generated SQL'):
        sql_generated = st.session_state.get('generated_sql')
        if not sql_generated:
            st.warning("No generated SQL to run. Click 'Generate SQL' first.")
        else:
            try:
                df = st.session_state.get('df')
                st.dataframe(df)
                st.session_state['last_df'] = df
            except Exception as e:
                st.error(f'Query execution failed: {e}')

if 'last_df' in st.session_state and not st.session_state['last_df'].empty:
    st.markdown("---")
    st.subheader("📊 Visualization")

    if st.button('Visualize Results'):
        st.session_state['show_viz'] = True

    if 'last_df' in st.session_state and not st.session_state['last_df'].empty:
        if st.session_state.get('show_viz', False):
            visualize_with_seaborn(st.session_state['last_df'])
            if st.button('Hide Visualization'):
                st.session_state['show_viz'] = False
