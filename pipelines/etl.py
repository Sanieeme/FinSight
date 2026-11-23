from pathlib import Path
import pandas as pd
from sqlalchemy import select
from backend.app.models import RawTransaction, DimUser, DimAccount, DimCategory, DimDate, FactTransaction
from .validation import validate_transactions

def get_or_create(db, model, filters, values):
    obj = db.execute(select(model).filter_by(**filters)).scalar_one_or_none()
    if obj is None:
        obj = model(**values)
        db.add(obj)
        db.flush()
    return obj

def process_csv(db, file_path):
    path = Path(file_path)
    frame = pd.read_csv(path)
    clean, rejected = validate_transactions(frame)
    loaded = duplicates = 0
    for index, row in clean.iterrows():
        exists = db.execute(select(RawTransaction).where(RawTransaction.record_hash == row.record_hash)).scalar_one_or_none()
        if exists:
            duplicates += 1
            continue
        raw = RawTransaction(source_file=path.name, source_row=int(index)+2,
            transaction_date=row.transaction_date, description=str(row.description),
            amount=float(row.amount), transaction_type=str(row.transaction_type),
            category=str(row.category), account=str(row.account), user_email=str(row.user_email),
            record_hash=row.record_hash)
        db.add(raw)
        db.flush()
        user = get_or_create(db, DimUser, {"user_email": raw.user_email}, {"user_email": raw.user_email})
        account = get_or_create(db, DimAccount, {"account_name": raw.account}, {"account_name": raw.account})
        category = get_or_create(db, DimCategory,
            {"category_name": raw.category, "transaction_type": raw.transaction_type},
            {"category_name": raw.category, "transaction_type": raw.transaction_type})
        d = raw.transaction_date
        date_dim = get_or_create(db, DimDate, {"full_date": d}, {
            "full_date": d, "day": d.day, "month": d.month, "month_name": d.strftime("%B"),
            "quarter": (d.month-1)//3+1, "year": d.year, "weekday": d.strftime("%A")})
        db.add(FactTransaction(raw_transaction_id=raw.id, date_id=date_dim.id, user_id=user.id,
            account_id=account.id, category_id=category.id, amount=raw.amount,
            transaction_type=raw.transaction_type, description=raw.description))
        loaded += 1
    db.commit()
    return {"loaded": loaded, "rejected": len(rejected), "duplicates": duplicates}
