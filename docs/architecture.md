# Architecture

Batch flow: CSV source → ingestion → validation and deduplication → raw transaction table → dimensional warehouse → FastAPI / Streamlit analytics.

The warehouse is a star schema. `fact_transactions` stores transaction measures and foreign keys to `dim_date`, `dim_user`, `dim_account` and `dim_category`. Airflow, Kafka, Spark and dbt are planned next-stage extensions.
