# 🧠 Smart Data Exploration Agent

This repository showcases my independent AI systems project focused on **LLM-powered data analytics** and **semantic query automation**.  
The system integrates **Large Language Models (LLMs)**, **semantic similarity reasoning**, and a **validation feedback loop** to enable intelligent data exploration on relational databases using natural language.

---

## 🎯 Project Aim
To build an intelligent agent capable of:
- Understanding *natural language queries* related to structured data.  
- Automatically generating, validating, and executing *SQL queries* across multi-table databases.  
- Applying *semantic similarity* to align user intent with database fields.  
- Using a *feedback loop* to self-correct SQL execution errors.  
- Providing *interactive data visualizations* through a Streamlit interface.

---

## 🧰 Core Technologies
- **OpenAI & Anthropic** – LLM-based SQL generation (GPT-4o, Claude 3.5).  
- **Transformers & Sentence-Transformers** – Semantic mapping with Hugging Face models.  
- **Pandas & NumPy** – Data management and preprocessing.  
- **SQLite3** – Local relational database.  
- **Plotly** – Interactive data visualization and charting.   
- **Streamlit** – Web interface for real-time exploration.

---

## ⚙️ System Components

### 🔄 LLM Router
- Unified interface connecting **OpenAI**, **Claude**, and **Hugging Face** models.  
- Manages temperature, token limits, and fallback model selection.

### 🧩 Automatic Schema Detection
- Dynamically extracts **tables**, **columns**, and **data types** from the connected database.

### 🧠 Semantic Comparison
- Uses **Sentence-Transformers** to map user query terms to schema fields.  
- Ensures query intent aligns with the available database attributes.

### ✅ Validation Scoring (LLM Judge)
- A secondary LLM (Mistral-7B) evaluates generated SQL queries.  
- Produces a *validation score* for evaluation.

### 🔁 Feedback Loop
- Detects SQL execution errors (e.g., missing columns or syntax issues).  
- Re-prompts the LLM with error context for refinement.  
- Iteratively repairs queries until valid execution or clear failure.

### 📊 Visualization Layer
- After successful query execution, users can visualize results directly in Streamlit using **Plotly**:  
  - 📊 Bar Charts  
  - 📈 Line Charts
  - and more...
- Visualizations are **fully interactive**, allowing users to hover, zoom, and explore data dynamically.

---

## 🧭 System Overview

| Component | Description |
|------------|-------------|
| **Schema Detection** | Extracts tables and columns automatically |
| **Semantic Comparison** | Aligns user intent with schema using embeddings |
| **SQL Generation** | Converts natural language to executable SQL |
| **LLM Judge** | Evaluates correctness via validation scoring |
| **Feedback Loop** | Repairs invalid SQL using iterative LLM prompting |
| **Visualization** | User-controlled analytics in Streamlit |

---

## 💡 Example Query Flow

**User Prompt:**  
> “Show the top items in terms of quantity sold in 2024 Q1”

**System Process:**
1. Schema detection identifies relevant tables (`online`).  
2. Semantic mapper confirms existence of `item_id`, `quantity` and `date`.  
3. The LLM generates SQL:
   ```sql
   SELECT item_id, SUM(quantity) as total_quantity
   FROM online
   WHERE strftime('%Y', date) = '2024' AND strftime('%m', date) BETWEEN '01' AND '03'
   GROUP BY item_id
   ORDER BY total_quantity DESC
   LIMIT 10;

4. Feedback loop corrects the query if execution fails.
5. User visualizes the result — e.g., a bar chart by item_id.

---

## 📈 Visualization Interface

The Streamlit dashboard provides:

* Quick-query shortcuts.
* Conversational natural-language input.
* Real-time SQL generation and output preview.
* Visualization selector with Plotly integration.

Example interface flow:

1. Enter a natural-language query (e.g., “Show total sales by category”).
2. The agent generates and validates SQL automatically.
3. Choose a visualization type (bar, line, or summary view).
4. View interactive charts and underlying data.

---

## 📊 Results & Findings

| Metric                     | Description                             | Result       |
| -------------------------- | --------------------------------------- | ------------ |
| **Validation Score (Avg)** | LLM-Judge evaluation on SQL correctness | **7.4 / 10** |

**Key Insights**

* Automatic schema extraction scales effectively across different datasets.
* The feedback loop enhances reliability for incomplete or ambiguous queries.
* Semantic similarity mapping handles paraphrased inputs robustly.
* LLM-Judge validation provides transparency into query generation quality.
* The system performed best on *aggregation* and *filtering* queries.
* More complex analytical queries, such as those requiring *correlation detection* or *SQL window functions* showed higher failure, highlighting opportunities for model fine-tuning. 

---

## 🧩 Project Assets & Accessibility  

To maintain originality and prevent full replication of the system, **certain backend agent files and logic components have been intentionally removed** from this repository.  
These include specific modules responsible for **schema validation**, **semantic mapping**, and **LLM orchestration**, which form the core reasoning engine of the system.

The current version still provides a **complete architectural overview**, **functional workflow**, and **demo-ready setup** for understanding how LLMs can be used for natural language database exploration.

Included Assets:
- 🖼️ **UI Screenshot** — Available in the `/assets` folder, showcasing the Streamlit interface and visualization controls.  
- 🎥 **Demo Video** — Available in the `/assets` folder. A walkthrough of the end-to-end query flow, from natural language input to SQL generation and visualization.  

This approach ensures the repository remains **educational, demonstrative, and portfolio-ready**, while protecting proprietary implementation details.

---

## 🚀 Future Improvements

* 💪 Upgrade compute resources to support larger transformer models.
* 🧠 Extend the LLM-Judge with textual feedback and suggestions.
* 🧩 Fine-tune models on SQL-specific reasoning datasets.
* 🌐 Add support for PostgreSQL and DuckDB backends.
* 🧾 Enable automated report generation with charts and summaries.
* 💬 Implement session-based memory for multi-turn conversations.

---

## 🔗 Resources

* **Dataset Source:** [Kaggle – Retail Sales Multi-Table Dataset](https://www.kaggle.com/competitions/ml-zoomcamp-2024-competition)

---

## ✅ Skills Demonstrated

* Large Language Model Integration (OpenAI, Claude, Hugging Face)
* Semantic Search and Query Alignment (Sentence-Transformers)
* Natural Language → SQL Translation
* Feedback Loop Engineering and Error Recovery
* LLM-Based Validation and Scoring
* Interactive Data Visualization with Plotly
* AI System Architecture and Streamlit Deployment

---
