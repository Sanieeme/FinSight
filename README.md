# FinSight — Financial Data Intelligence Platform

FinSight imports financial transaction CSV files, validates records, loads a dimensional warehouse, exposes analytics through FastAPI and presents insights in Streamlit.

## Features
- CSV ingestion, validation and duplicate detection
- Raw transaction storage and ETL processing
- Star schema: fact transactions plus date, user, account and category dimensions
- Income, expenses, cash flow, savings rate and category analytics
- FastAPI endpoints and Streamlit dashboard
- Synthetic South African Rand demo data
- SQLite by default; PostgreSQL supported with Docker Compose
- Pytest tests

> Educational portfolio project only. Use synthetic data. Do not upload banking credentials or sensitive financial information.

## Run locally (macOS/Linux)
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python3 scripts/generate_sample_data.py
python3 scripts/run_etl.py
```
Terminal 1:
```bash
uvicorn backend.app.main:app --reload
```
API docs: http://127.0.0.1:8000/docs

Terminal 2:
```bash
streamlit run dashboard/app.py
```

## PostgreSQL
Set `DATABASE_URL` in `.env` to:
`postgresql+psycopg://finsight:finsight_dev_password@localhost:5432/finsight`
Then run `docker compose up -d db`.

## CSV columns
`transaction_date,description,amount,transaction_type,category,account,user_email`

Dates use YYYY-MM-DD, amounts must be positive, and transaction_type must be income or expense.

## API
- `GET /health`
- `POST /transactions/upload`
- `GET /analytics/summary`
- `GET /analytics/monthly`
- `GET /analytics/categories`
- `GET /transactions`

## Next upgrades
Add dbt, Airflow orchestration, Kafka streaming, Spark processing, authentication and deployment. These are planned extensions, not requirements for this first runnable version.
