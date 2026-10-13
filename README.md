
@'
# Enterprise AI Data Analysis Agent

An AI-powered sales data analysis application built with Python, FastAPI, SQLite, SQLAlchemy, and Google Gemini.

## Features

- Calculate total sales revenue.
- Identify the top-selling product by revenue.
- Analyze sales revenue by region.
- Store and retrieve sales records using SQLite.
- Ask natural-language questions about sales data through an AI endpoint.
- Use local Python-based fallback responses when the AI service is unavailable.
- Explore and test API endpoints using Swagger UI.

## Tech Stack

- Python
- FastAPI
- SQLite
- SQLAlchemy
- Google Gemini API
- Pandas
- Pytest
- Swagger UI

## Project Structure

```text
enterprise-ai-data-agent/
├── agent.py
├── database.py
├── llm_agent.py
├── main.py
├── sales.csv
├── test_agent.py
├── .gitignore
├── README.md
└── requirements.txt
```

## Setup Instructions

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd enterprise-ai-data-agent
```

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure the Gemini API key

Create a local file named `gemini_test.env` in the project root:

```text
GEMINI_API_KEY=your_gemini_api_key
```

Replace the example value with your own API key. Never upload this file or share your API key publicly.

### 5. Run the application

```powershell
python -m uvicorn main:app --reload
```

### 6. Open Swagger UI

Visit:

http://127.0.0.1:8000/docs

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Check the application |
| GET | `/sales` | Retrieve sales records |
| GET | `/sales/summary` | View sales summary |
| GET | `/sales/top-product` | Find the top product |
| GET | `/sales/regions` | View revenue by region |
| POST | `/ask` | Ask a question about sales data |

## Run Tests

```powershell
python -m pytest -v
```

## Example Question

```json
{
  "question": "What is the total sales revenue?"
}
```

The application processes the question and returns an answer based on the available sales data.

## Project Goal

This project demonstrates data analysis, REST API development, database integration, automated testing, and natural-language interaction with business data.
'@ | Set-Content -Encoding utf8 README.md
