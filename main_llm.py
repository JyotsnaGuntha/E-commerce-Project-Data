import sqlite3
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load API key
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize FastAPI
app = FastAPI()

DB_PATH = "ecommerce.db"

# Function to ask Gemini to convert question into SQL
def question_to_sql(question: str) -> str:
    prompt = f"""
    You are an expert data analyst. 
    Convert the following question into an SQL query for the database:
    Tables: ad_sales, total_sales, eligibility (you know these from the datasets).
    Question: "{question}"
    Only return the SQL query, nothing else.
    """
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text.strip()

# Route to answer questions
@app.get("/ask")
def ask(question: str = Query(..., description="Ask a question about sales data")):
    try:
        # Convert question to SQL
        sql_query = question_to_sql(question)

        # Execute SQL query
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(sql_query)
        result = cursor.fetchall()
        conn.close()

        return JSONResponse(content={
            "question": question,
            "sql_query": sql_query,
            "result": result
        })
    except Exception as e:
        return JSONResponse(content={"error": str(e)})
