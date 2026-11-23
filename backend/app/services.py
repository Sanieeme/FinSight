from sqlalchemy import func, case
from .models import FactTransaction, DimDate, DimCategory

def summary(db):
    income = db.query(func.coalesce(func.sum(case((FactTransaction.transaction_type=="income", FactTransaction.amount), else_=0)),0)).scalar()
    expenses = db.query(func.coalesce(func.sum(case((FactTransaction.transaction_type=="expense", FactTransaction.amount), else_=0)),0)).scalar()
    count = db.query(func.count(FactTransaction.id)).scalar() or 0
    income, expenses = float(income), float(expenses)
    net = income-expenses
    return {"income": round(income,2), "expenses": round(expenses,2), "net_cash_flow": round(net,2),
            "savings_rate": round(net/income*100,2) if income else 0, "transaction_count": count}

def monthly(db):
    rows = db.query(DimDate.year, DimDate.month,
        func.sum(case((FactTransaction.transaction_type=="income",FactTransaction.amount),else_=0)).label("income"),
        func.sum(case((FactTransaction.transaction_type=="expense",FactTransaction.amount),else_=0)).label("expenses")
        ).join(DimDate,FactTransaction.date_id==DimDate.id).group_by(DimDate.year,DimDate.month).order_by(DimDate.year,DimDate.month).all()
    return [{"month":f"{r.year}-{r.month:02d}","income":float(r.income or 0),"expenses":float(r.expenses or 0)} for r in rows]

def categories(db):
    rows = db.query(DimCategory.category_name,func.sum(FactTransaction.amount).label("total")).join(
        DimCategory,FactTransaction.category_id==DimCategory.id).filter(FactTransaction.transaction_type=="expense").group_by(
        DimCategory.category_name).order_by(func.sum(FactTransaction.amount).desc()).all()
    return [{"category":r.category_name,"total":float(r.total or 0)} for r in rows]

def transactions(db, limit=100):
    rows = db.query(FactTransaction,DimDate,DimCategory).join(DimDate,FactTransaction.date_id==DimDate.id).join(
        DimCategory,FactTransaction.category_id==DimCategory.id).order_by(DimDate.full_date.desc()).limit(limit).all()
    return [{"date":str(d.full_date),"description":f.description,"amount":float(f.amount),
             "type":f.transaction_type,"category":c.category_name} for f,d,c in rows]
