# SQLAlchemy ORM models for DB tables

from sqlalchemy import Column, Integer, String, BigInteger, DECIMAL, Text, DateTime, func
from .db import Base

# Main countries table
class Country(Base):
    __tablename__ = "countries"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(128), unique=True, nullable=False)
    capital = Column(String(128), nullable=True)
    region = Column(String(64), nullable=True)
    population = Column(BigInteger, nullable=False)
    currency_code = Column(String(16), nullable=True)
    exchange_rate = Column(DECIMAL(18,6), nullable=True)  # rate vs USD
    estimated_gdp = Column(DECIMAL(24,2), nullable=True)
    flag_url = Column(Text, nullable=True)
    last_refreshed_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

# Meta table for storing last refresh timestamp
class MetaKV(Base):
    __tablename__ = "meta"
    key = Column(String(64), primary_key=True)
    value = Column(Text, nullable=False)
