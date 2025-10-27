# /status endpoint shows meta info

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db import get_db
from ..crud import get_status
from ..schemas import StatusOut

router = APIRouter(tags=["status"])

@router.get("/status", response_model=StatusOut)
def status(db: Session = Depends(get_db)):
    total, ts = get_status(db)
    return {"total_countries": total, "last_refreshed_at": ts}
