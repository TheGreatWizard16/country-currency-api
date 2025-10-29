# src/routes/status.py
from fastapi import APIRouter
from sqlalchemy import text, inspect
from sqlalchemy.exc import SQLAlchemyError
from ..db import engine, DB_URL

router = APIRouter(tags=["status"])

def _target():
    # shows "host:port/db" only; safe to log/return
    try:
        return DB_URL.split("@")[-1].split("?")[0]
    except Exception:
        return "unknown"

@router.get("/status")
def status():
    try:
        # 1) Can we open a connection?
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))

        # 2) Do we have a countries table yet? (supports either name)
        insp = inspect(engine)
        has_countries = insp.has_table("countries") or insp.has_table("country")

        return {
            "ok": True,
            "db": "up",
            "target": _target(),
            "has_countries_table": bool(has_countries),
        }
    except SQLAlchemyError as e:
        # Never 500 here; return a diagnostic payload so you can see the exact failure
        return {
            "ok": False,
            "db": "down",
            "target": _target(),
            "reason": e.__class__.__name__,
            "msg": str(e),
        }
