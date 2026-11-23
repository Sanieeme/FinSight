from sqlalchemy import Column, Integer, String, Date, DateTime, Numeric, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from .database import Base

class RawTransaction(Base):
    __tablename__ = "raw_transactions"
    id = Column(Integer, primary_key=True)
    source_file = Column(String(255), nullable=False)
    source_row = Column(Integer, nullable=False)
    transaction_date = Column(Date, nullable=False)
    description = Column(String(255), nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)
    transaction_type = Column(String(20), nullable=False)
    category = Column(String(100), nullable=False)
    account = Column(String(100), nullable=False)
    user_email = Column(String(255), nullable=False)
    record_hash = Column(String(64), nullable=False, unique=True)
    ingestion_status = Column(String(20), default="loaded", nullable=False)
    ingested_at = Column(DateTime(timezone=True), server_default=func.now())

class DimUser(Base):
    __tablename__ = "dim_user"
    id = Column(Integer, primary_key=True)
    user_email = Column(String(255), unique=True, nullable=False)

class DimAccount(Base):
    __tablename__ = "dim_account"
    id = Column(Integer, primary_key=True)
    account_name = Column(String(100), unique=True, nullable=False)

class DimCategory(Base):
    __tablename__ = "dim_category"
    id = Column(Integer, primary_key=True)
    category_name = Column(String(100), nullable=False)
    transaction_type = Column(String(20), nullable=False)
    __table_args__ = (UniqueConstraint("category_name", "transaction_type"),)

class DimDate(Base):
    __tablename__ = "dim_date"
    id = Column(Integer, primary_key=True)
    full_date = Column(Date, unique=True, nullable=False)
    day = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    month_name = Column(String(20), nullable=False)
    quarter = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)
    weekday = Column(String(20), nullable=False)

class FactTransaction(Base):
    __tablename__ = "fact_transactions"
    id = Column(Integer, primary_key=True)
    raw_transaction_id = Column(Integer, ForeignKey("raw_transactions.id"), unique=True, nullable=False)
    date_id = Column(Integer, ForeignKey("dim_date.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("dim_user.id"), nullable=False)
    account_id = Column(Integer, ForeignKey("dim_account.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("dim_category.id"), nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)
    transaction_type = Column(String(20), nullable=False)
    description = Column(String(255), nullable=False)
