# src/routes/countries.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from ..db import get_db
from ..schemas import CountryOut
from .. import crud
from ..services.refresh import refresh_all
from ..services.image import summary_image_path
import os

router = APIRouter(prefix="/countries", tags=["countries"])

@router.post("/refresh")
def refresh(db: Session = Depends(get_db)):
    try:
        refresh_all(db)
        return {"status": "ok"}
    except SQLAlchemyError as e:
        return {"ok": False, "error": e.__class__.__name__, "msg": str(e)}

# IMPORTANT: define /image BEFORE /{name} so the param route doesn't swallow it
@router.get("/image")
def get_summary_image():
    path = summary_image_path()
    if not os.path.exists(path):
        return JSONResponse(status_code=404, content={"error": "Summary image not found"})
    return FileResponse(path, media_type="image/png")

@router.get("", response_model=list[CountryOut])
def list_countries(
    region: str | None = None,
    currency: str | None = None,
    sort: str | None = None,
    db: Session = Depends(get_db),
):
    try:
        return crud.list_countries(db, region=region, currency=currency, sort=sort)
    except SQLAlchemyError as e:
        # Return a controlled error instead of a 500
        return JSONResponse(status_code=500, content={"ok": False, "error": e.__class__.__name__, "msg": str(e)})

@router.get("/{name}", response_model=CountryOut)
def get_country(name: str, db: Session = Depends(get_db)):
    try:
        c = crud.get_country_by_name(db, name)
        if not c:
            raise HTTPException(status_code=404, detail={"error": "Country not found"})
        return c
    except SQLAlchemyError as e:
        return JSONResponse(status_code=500, content={"ok": False, "error": e.__class__.__name__, "msg": str(e)})

@router.delete("/{name}")
def delete_country(name: str, db: Session = Depends(get_db)):
    try:
        ok = crud.remove_country(db, name)
        if not ok:
            raise HTTPException(status_code=404, detail={"error": "Country not found"})
        return {"status": "deleted"}
    except SQLAlchemyError as e:
        return JSONResponse(status_code=500, content={"ok": False, "error": e.__class__.__name__, "msg": str(e)})
