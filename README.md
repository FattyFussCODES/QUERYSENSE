# QuerySense

QuerySense is an **AI-native Natural Language → SQL (Text-to-SQL)** system that allows users to interact with relational databases using natural language instead of writing SQL queries manually.

Powered by the **Google Gemini API**, QuerySense features a premium modern UI, dynamically intercepts natural English statements, generates perfectly formatted SQLite mappings out of your schema, executing them directly to return cleanly organized results.

> Database engine: **SQLite (default)**, **MySQL (optional)**

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [System Architecture](#system-architecture)
- [Project Structure](#project-structure)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Database Setup](#database-setup)
- [Running the Application](#running-the-application)
- [Future Improvements](#future-improvements)

## Overview

QuerySense provides a natural language interface that utilizes LLMs (Large Language Models) to convert English queries into SQL statements and executes them in the database automatically. 

### Example

**User Query**
> "Name of students who has gpa of less than 8.50"

**Generated SQL**
```sql
SELECT name FROM students WHERE gpa < 8.50
```

## Key Features

- **Generative AI SQL Translation**: Utilizes Google Gemini 2.5 Flash to automatically convert plain English conversational requests into accurate database queries.
- **Premium Glassmorphism UI**: Beautifully designed Dark Mode web interface with dynamic loaders and isolated SQL preview widgets.
- **Dynamic Schema Awareness**: Fetches the exact columns dynamically so the LLM automatically maps synonyms perfectly without rigid Regex pipelines.
- **Headless Backend**: FastAPI securely isolates API tokens and executes requests server-side securely. 

## System Architecture

```text
Natural Language Query (Browser GUI)
	↓
FastAPI Backend Route
	↓
Schema Ingestion -> Gemini API (LLM_SQL_Generator)
	↓
SQLite Execution
	↓
Structured JSON return -> Glassmorphism rendering
```

## Project Structure

```text
QuerySense/
├── main.py
├── requirements.txt
├── .env (You need to create this)
├── config/
│   └── db_config.py
├── database/
│   ├── schema.sql
│   ├── sample_data.sql
│   └── init_db.py
├── engine/
│   ├── llm_sql_generator.py
│   └── schema_loader.py
├── executor/
│   ├── db_connection.py
│   ├── query_executor.py
│   └── result_formatter.py
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
├── logs/
│   └── query_logger.py
├── api/
│   └── app.py
└── tests/
    └── test_queries.py
```

## Technology Stack

- **Backend**: Python, FastAPI
- **AI Middleware**: Google Gemini `google-generativeai`
- **Frontend**: Vanilla HTML/CSS/JS (Custom Aesthetics)
- **Database**: SQLite (default), MySQL (optional)

## Installation

1. Clone the repository and navigate inside:
```bash
git clone https://github.com/FattyFussCODES/QUERYSENSE.git
cd QUERYSENSE
```

2. Create and activate a Virtual Environment:
```powershell
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory and add your Gemini API Key:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

## Database Setup

QuerySense is pre-loaded with a massive student leaderboard sample database!

To initialize the database with all 96 records, simply run:
```powershell
python main.py --init-db
```

## Running the Application

To launch the backend API and host the Web Interface natively:
```powershell
uvicorn api.app:create_app --factory --host 127.0.0.1 --port 8000 --reload
```
Then visit **http://127.0.0.1:8000/** in your browser!

### Troubleshooting
If testing fails via `python -m unittest`, remember that the test suite directly pings the LLM API and tests expected conditions. Ensure you have network connectivity. 

## Future Improvements

- Add support for multiple tables (JOIN inference via AI validation).
- Persist Chat History UI so users can query in conversational blocks.
- Introduce streaming generation loaders.

---

### 👏 Built With ❤️ By
[AVIRAL BOHRA](https://github.com/FattyFussCODES)
