# src/app.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import time
from sqlalchemy.exc import OperationalError

# ensure models are registered before create_all
from . import models

# import DB primitives from db.py
from .db import engine, Base, DB_URL

# routers
from .routes.countries import router as countries_router
from .routes.status import router as status_router

# log sanitized DB target (host:port/db)
print("[boot] USING_DB =", DB_URL.split("@")[-1].split("?")[0])

app = FastAPI(title="Country Currency & Exchange API")

@app.on_event("startup")
def init_db_with_retry():
    # Try for ~60 seconds without crashing the app
    attempts = 30
    for _ in range(attempts):
        try:
            Base.metadata.create_all(bind=engine)
            break
        except OperationalError:
            time.sleep(2)
        except Exception:
            time.sleep(2)

@app.get("/")
def root():
    return {"ok": True}

@app.get("/health")
def health():
    return {"ok": True}

# Global error handler
@app.exception_handler(Exception)
async def fallback_error_handler(request: Request, exc: Exception):
    if hasattr(exc, "status_code"):
        raise exc
    return JSONResponse(status_code=500, content={"error": "Internal server error"})

# Mount routers
app.include_router(countries_router)
app.include_router(status_router)
