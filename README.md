# 🧠 AI Agent for E-commerce Data Intelligence

Build an AI-powered agent that **answers complex business questions from structured data** like a human analyst — powered by local LLMs or Gemini, and capable of understanding, querying, and visualizing product sales and ad performance.

## 🚀 Project Objective

This project builds an **end-to-end AI system** that:
- Understands natural language questions about e-commerce sales and ads
- Translates them into **SQL queries**
- Retrieves data from **structured SQLite databases**
- Responds in **human-readable format**
- (Bonus) Generates visualizations
- (Bonus) Streams live-like responses

---

## 🗃️ Datasets Used

1. **Product-Level Ad Sales and Metrics**
2. **Product-Level Total Sales and Metrics**
3. **Product-Level Eligibility Table**

All CSVs are converted to structured **SQLite tables**.

---

## 🛠️ Tech Stack

| Layer              | Tech Used                     |
|-------------------|-------------------------------|
| Backend            | Python + FastAPI              |
| LLM                | Gemini 2.5 (via API) / Local LLM |
| Database           | SQLite                        |
| Visualization      | Matplotlib / Plotly (Bonus)   |
| Hosting/Testing    | Ngrok / Colab / Localhost     |

---

## 🧩 System Architecture

```
User → FastAPI → LLM (Question → SQL) → SQLite DB → Response → User  
                             ↘ (Optional: Matplotlib Chart)
                             ↘ (Optional: Streamed Output)
```

---

## 📦 Setup Instructions

1. **Clone the Repository**

```bash
git clone https://github.com/yourusername/ecommerce-ai-agent.git
cd ecommerce-ai-agent
```

2. **Install Dependencies**

```bash
pip install -r requirements.txt
```

3. **Configure LLM API (If Using Gemini)**

```python
# Use Google Colab or add directly
GEMINI_API_KEY = "your-api-key"
```

4. **Run FastAPI Server**

```bash
uvicorn app:app --reload
```

5. **Expose Locally (Optional)**

```bash
ngrok http 8000
```

---

## 💡 Sample Questions You Can Ask

| Question                                    | What It Does                                      |
|---------------------------------------------|---------------------------------------------------|
| What is my total sales?                     | Aggregates total revenue from all products        |
| Calculate the RoAS                          | Computes Return on Ad Spend (Ad Revenue / Spend)  |
| Which product had the highest CPC?          | Finds the product with highest Cost Per Click     |
| What are sales for product X last month?    | Filters sales by product and time                 |

---

## 🖼️ Bonus: Visual Output

Supports optional plotting using:

- 📊 **Matplotlib** for bar/pie charts
- 📈 **Plotly** for interactive graphs

---

## 🔁 Bonus: Streamed Responses

Add real-time output typing effect using:

```python
from fastapi.responses import StreamingResponse
```

---

## 📂 Folder Structure

```
ecommerce-ai-agent/
│
├── data/                   # Raw CSVs and SQLite DBs
├── app.py                  # Main FastAPI application
├── agent.py                # LLM + SQL query generator
├── db_utils.py             # DB setup and connection logic
├── visualize.py            # Bonus: Plotting functions
├── requirements.txt
└── README.md
```

---


## ✅ Deliverables Checklist

- ✅ SQL DB setup from all 3 CSVs  
- ✅ FastAPI to receive and respond to questions  
- ✅ Gemini/Local LLM-powered question understanding  
- ✅ Dynamic SQL query generation + clean responses  
- ✅ Bonus: Visualizations  
- ✅ Bonus: Streamed response simulation  
- ✅ GitHub repo with codebase  
- ✅ Drive demo video with terminal & API call shown

---

## 🧠 Reimagine Data Analysis

This isn't just automation — it's **augmented intelligence** for business decision-making. Designed for scalability, modularity, and real-world use.

> Built with ❤️ to replace dashboards with conversations.

---

