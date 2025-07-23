import sqlite3
from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import JSONResponse
import google.generativeai as genai
import os
import uvicorn
from pyngrok import ngrok
import nest_asyncio
import asyncio
import requests
import json
import threading

# --- 1. SETUP AND AUTHENTICATION ---
from google.colab import userdata
try:
    GEMINI_API_KEY = userdata.get('GEMINI_API_KEY')
    NGROK_AUTH_TOKEN = userdata.get('NGROK_AUTH_TOKEN')
except Exception as e:
    print("❌ Please make sure GEMINI_API_KEY and NGROK_AUTH_TOKEN are set in Colab Secrets.")
    raise e

genai.configure(api_key=GEMINI_API_KEY)
ngrok.set_auth_token(NGROK_AUTH_TOKEN)

# --- 2. DEFINE FASTAPI APP ---
app = FastAPI(title="E-commerce AI Agent")
DB_PATH = "ecommerce.db"

def get_schema():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    schema_info = ""
    for table in tables:
        table_name = table[0]
        schema_info += f"Table '{table_name}':\n"
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        for column in columns:
            schema_info += f"  - {column[1]} ({column[2]})\n"
    conn.close()
    return schema_info

def question_to_sql(question: str, schema: str) -> str:
    prompt = f"""You are an expert SQLite data analyst. Convert the question to a valid SQLite query based on the provided schema. Only return the SQL query. Schema: {schema}. Question: "{question}". SQL Query:"""
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text.strip().replace("```sql", "").replace("```", "").strip()

@app.get("/ask", summary="Ask the AI a question")
async def ask(question: str = Query(..., description="Ask a question about e-commerce data")):
    try:
        schema = get_schema()
        sql_query = question_to_sql(question, schema)
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(sql_query)
        result = cursor.fetchall()
        column_names = [description[0] for description in cursor.description]
        conn.close()
        formatted_result = [dict(zip(column_names, row)) for row in result]
        return JSONResponse(content={
            "question": question,
            "generated_sql_query": sql_query,
            "answer": formatted_result
        })
    except sqlite3.OperationalError as db_err:
        raise HTTPException(status_code=400, detail=f"Database error: {str(db_err)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

# --- 3. SERVER STARTUP & TESTING ---
def run_uvicorn():
    config = uvicorn.Config(app, host="127.0.0.1", port=8000, log_level="warning")
    server = uvicorn.Server(config)
    server.run()

async def start_server_and_get_url():
    public_url = ngrok.connect(8000).public_url
    print(f"✅ Server is live at: {public_url}")
    thread = threading.Thread(target=run_uvicorn, daemon=True)
    thread.start()
    await asyncio.sleep(3)  # wait for server to fully start
    return public_url

def run_all_tests(base_url):
    print("\n--- 🚀 Running Automated Tests ---")
    questions = [
    "What is my total sales?",
    "Calculate the RoAS",
    "Which product had the highest CPC?",
    "Which item had the most units sold in ad sales?",
    "Which item had the highest ad spend on any single day?",
    "What is the total number of ineligible products?"
]

    for i, question in enumerate(questions):
        print(f"\n➡️ Test {i+1}: Asking '{question}'")
        try:
            response = requests.get(f"{base_url}/ask", params={"question": question}, timeout=60)
            response.raise_for_status()
            print("✅ Response:")
            print(json.dumps(response.json(), indent=2))
        except requests.exceptions.RequestException as e:
            print(f"❌ Request failed: {e}")
    print("\n✅ All tests complete.")

# --- 4. MAIN ENTRY ---
async def main():
    public_url = await start_server_and_get_url()
    if public_url:
        run_all_tests(public_url)

if __name__ == "__main__":
    nest_asyncio.apply()
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"🔥 Unexpected error in main: {e}")
    finally:
        print("\n✅ Shutting down ngrok.")
        ngrok.kill()
