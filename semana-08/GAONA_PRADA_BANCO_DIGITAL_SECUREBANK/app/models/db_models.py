from sqlalchemy import Column, Integer, String, Float, DateTime, Enum, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from ..models.schemas import AccountTypeEnum, TransactionTypeEnum

Base = declarative_base()

class Account(Base):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(String, unique=True, index=True)
    customer_name = Column(String)
    balance = Column(Float)
    account_type = Column(Enum(AccountTypeEnum))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    status = Column(String, default="active")

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(String, unique=True, index=True)
    account_id = Column(String, index=True)
    amount = Column(Float)
    transaction_type = Column(Enum(TransactionTypeEnum))
    metodo_pago = Column(String)
    fecha_transaccion = Column(DateTime, default=datetime.now)
    status = Column(String, default="completed")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)