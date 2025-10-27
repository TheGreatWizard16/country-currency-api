# Entry point of the app

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from .routes.countries import router as countries_router
from .routes.status import router as status_router

app = FastAPI(title="Country Currency & Exchange API")

@app.get("/health")
def health():
    # Simple health check
    return {"ok": True}

# Global error handler
@app.exception_handler(Exception)
async def fallback_error_handler(request: Request, exc: Exception):
    # Keep native HTTPException handling for proper codes
    if hasattr(exc, "status_code"):
        raise exc
    # Convert unknown errors to standard 500 response
    return JSONResponse(status_code=500, content={"error": "Internal server error"})

# Mount routers
app.include_router(countries_router)
app.include_router(status_router)
