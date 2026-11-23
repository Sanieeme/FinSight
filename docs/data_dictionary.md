# Data dictionary

CSV fields: `transaction_date` (YYYY-MM-DD), `description`, positive `amount`, `transaction_type` (income/expense), `category`, `account`, `user_email`.

Warehouse:
- `raw_transactions`: source record, source filename, row number and hash.
- `fact_transactions`: amount, transaction type, description and dimension keys.
- `dim_date`: date, day, month, quarter, year and weekday.
- `dim_category`: category and transaction type.
- `dim_account`: account label.
- `dim_user`: demo user email.
