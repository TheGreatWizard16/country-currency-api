# src/db.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .settings import settings

DB_URL = settings.sqlalchemy_uri()

# Pick connect_args by scheme
connect_args = {}
if DB_URL.startswith("mysql+"):
    connect_args = {"connect_timeout": 5}
elif DB_URL.startswith("sqlite:///"):
    connect_args = {"check_same_thread": False}

engine = create_engine(
    DB_URL,
    pool_pre_ping=True,
    pool_recycle=1800,
    echo=False,
    connect_args=connect_args,
)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
