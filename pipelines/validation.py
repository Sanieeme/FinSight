import hashlib
import pandas as pd

REQUIRED = ["transaction_date", "description", "amount", "transaction_type", "category", "account", "user_email"]

def make_hash(row):
    raw = "|".join(str(row[c]).strip().lower() for c in REQUIRED)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()

def validate_transactions(df):
    missing = [c for c in REQUIRED if c not in df.columns]
    if missing:
        raise ValueError("Missing required columns: " + ", ".join(missing))
    data = df[REQUIRED].copy()
    data["transaction_date"] = pd.to_datetime(data["transaction_date"], errors="coerce").dt.date
    data["amount"] = pd.to_numeric(data["amount"], errors="coerce")
    for col in ["description", "transaction_type", "category", "account", "user_email"]:
        data[col] = data[col].astype("string").str.strip()
    valid = (
        data.transaction_date.notna() & data.amount.notna() & (data.amount > 0)
        & data.description.notna() & (data.description != "")
        & data.transaction_type.str.lower().isin(["income", "expense"])
        & data.category.notna() & (data.category != "")
        & data.account.notna() & (data.account != "")
        & data.user_email.str.contains(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", na=False)
    )
    clean, rejected = data[valid].copy(), data[~valid].copy()
    clean["transaction_type"] = clean.transaction_type.str.lower()
    clean["user_email"] = clean.user_email.str.lower()
    clean["record_hash"] = clean.apply(make_hash, axis=1)
    clean = clean.drop_duplicates("record_hash")
    return clean, rejected
