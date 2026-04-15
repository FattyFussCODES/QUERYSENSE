from __future__ import annotations

import os

import google.generativeai as genai


def _setup_gemini() -> None:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not set in the environment.")
    genai.configure(api_key=api_key)


def generate_sql_from_llm(query: str, schema_info: dict[str, list[str]], table: str = "students") -> str:
    _setup_gemini()
    
    model = genai.GenerativeModel("gemini-2.5-flash")
    
    columns = schema_info.get(table, [])
    schema_str = f"Table: {table}\nColumns: " + ", ".join(columns)
    
    prompt = f"""
You are an expert SQL Generator.
Given the following SQLite schema:
{schema_str}

Translate the following natural language query into a raw SQLite SELECT query.
- Use simple WHERE clauses.
- Order logically if limit is requested.
- Return ONLY the raw SQL. Do not wrap it in markdown block quotes (e.g. ```sql). Do not include any explanations.
- Output MUST be a single line exactly matching the SQL command.

Query: "{query}"
"""
    
    response = model.generate_content(prompt)
    sql = response.text.strip()
    
    # Fallback strip in case of markdown formatting
    if sql.startswith("```sql"):
        sql = sql[6:]
    if sql.startswith("```"):
        sql = sql[3:]
    if sql.endswith("```"):
        sql = sql[:-3]
        
    # Replace placeholders and fix any semi-colons
    sql = sql.strip().strip(";")
    
    return sql
