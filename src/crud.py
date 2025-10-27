# Centralized DB operations (CRUD logic)

from sqlalchemy.orm import Session
from sqlalchemy import select, func, asc, desc, delete
from .models import Country, MetaKV
from .utils import parse_sort

def get_status(db: Session):
    total = db.scalar(select(func.count(Country.id))) or 0
    last = db.get(MetaKV, "last_refresh_ts")
    return total, (last.value if last else None)

def get_country_by_name(db: Session, name: str):
    stmt = select(Country).where(func.lower(Country.name) == name.lower())
    return db.scalars(stmt).first()

def list_countries(db: Session, region: str | None, currency: str | None, sort: str | None):
    stmt = select(Country)
    if region:
        stmt = stmt.where(Country.region == region)
    if currency:
        stmt = stmt.where(Country.currency_code == currency)
    col, direction = parse_sort(sort)
    colobj = getattr(Country, col)
    stmt = stmt.order_by(desc(colobj) if direction == "desc" else asc(colobj))
    return db.scalars(stmt).all()

def upsert_country(db: Session, data: dict):
    existing = get_country_by_name(db, data["name"])
    if existing:
        # Update existing record
        for k, v in data.items():
            setattr(existing, k, v)
        return existing, False
    # Insert new record
    c = Country(**data)
    db.add(c)
    return c, True

def remove_country(db: Session, name: str):
    c = get_country_by_name(db, name)
    if not c:
        return False
    db.execute(delete(Country).where(Country.id == c.id))
    db.commit()
    return True

def set_last_refresh(db: Session, iso_ts: str):
    # Update or insert refresh timestamp
    m = db.get(MetaKV, "last_refresh_ts")
    if not m:
        m = MetaKV(key="last_refresh_ts", value=iso_ts)
        db.add(m)
    else:
        m.value = iso_ts
