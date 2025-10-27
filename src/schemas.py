# Pydantic models for API responses (serialize DB objects safely)

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CountryOut(BaseModel):
    id: int
    name: str
    capital: Optional[str] = None
    region: Optional[str] = None
    population: int
    currency_code: Optional[str] = None
    exchange_rate: Optional[float] = None
    estimated_gdp: Optional[float] = None
    flag_url: Optional[str] = None
    last_refreshed_at: datetime

    class Config:
        from_attributes = True  # allows SQLAlchemy model -> schema

class StatusOut(BaseModel):
    total_countries: int
    last_refreshed_at: Optional[str] = None
