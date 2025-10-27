# Routes for /countries endpoints

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from sqlalchemy.orm import Session
from ..db import get_db
from ..schemas import CountryOut
from .. import crud
from ..services.refresh import refresh_all
from ..services.image import summary_image_path
import os

router = APIRouter(prefix="/countries", tags=["countries"])

@router.post("/refresh")
def refresh(db: Session = Depends(get_db)):
    # Pull new data + regenerate image
    refresh_all(db)
    return {"status": "ok"}

@router.get("", response_model=list[CountryOut])
def list_countries(
    region: str | None = None,
    currency: str | None = None,
    sort: str | None = None,
    db: Session = Depends(get_db),
):
    return crud.list_countries(db, region=region, currency=currency, sort=sort)

@router.get("/{name}", response_model=CountryOut)
def get_country(name: str, db: Session = Depends(get_db)):
    c = crud.get_country_by_name(db, name)
    if not c:
        raise HTTPException(status_code=404, detail={"error": "Country not found"})
    return c

@router.delete("/{name}")
def delete_country(name: str, db: Session = Depends(get_db)):
    ok = crud.remove_country(db, name)
    if not ok:
        raise HTTPException(status_code=404, detail={"error": "Country not found"})
    return {"status": "deleted"}

@router.get("/image")
def get_summary_image():
    # Serve generated summary image
    path = summary_image_path()
    if not os.path.exists(path):
        return JSONResponse(status_code=404, content={"error": "Summary image not found"})
    return FileResponse(path, media_type="image/png")
