# Entry point of the app

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

# Routers
from .routes.countries import router as countries_router
from .routes.status import router as status_router

# --- DB init with retry so Railway healthcheck can pass even if MySQL is slow ---
import time
from sqlalchemy.exc import OperationalError
from .db import engine, Base

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
            # Swallow unexpected init errors; /health should still respond
            time.sleep(2)

@app.get("/health")
def health():
    # Simple health check; does not touch DB
    return {"ok": True}

# Global error handler
@app.exception_handler(Exception)
async def fallback_error_handler(request: Request, exc: Exception):
    # Let HTTPException bubble with its own status code
    if hasattr(exc, "status_code"):
        raise exc
    # Convert unknown errors to standard 500
    return JSONResponse(status_code=500, content={"error": "Internal server error"})

# Mount routers
app.include_router(countries_router)
app.include_router(status_router)
