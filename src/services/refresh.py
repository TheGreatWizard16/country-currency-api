# Fetches data from restcountries + open-er-api, merges and caches into DB

import random, httpx, datetime
from fastapi import HTTPException
from sqlalchemy.orm import Session
from ..crud import upsert_country, set_last_refresh
from ..services.image import generate_summary_image

COUNTRIES_URL = "https://restcountries.com/v2/all?fields=name,capital,region,population,flag,currencies"
FX_URL = "https://open.er-api.com/v6/latest/USD"

def _compute_gdp(population: int, rate: float | None):
    if rate is None or rate == 0:
        return None
    mult = random.randint(1000, 2000)  # random multiplier per refresh
    return (population * mult) / rate

def refresh_all(db: Session):
    # Fetch both APIs, or raise 503 if either fails
    try:
        with httpx.Client(timeout=20) as client:
            c_res = client.get(COUNTRIES_URL)
            if c_res.status_code != 200:
                raise RuntimeError("restcountries.com")
            countries = c_res.json()

            f_res = client.get(FX_URL)
            if f_res.status_code != 200:
                raise RuntimeError("open-er-api.com")
            fx = f_res.json()
            rates = fx.get("rates")
            if not isinstance(rates, dict):
                raise RuntimeError("rates missing")
    except Exception:
        raise HTTPException(
            status_code=503,
            detail={
                "error": "External data source unavailable",
                "details": "Could not fetch data from restcountries or open-er-api",
            },
        )

    # Insert / update country records
    try:
        for item in countries:
            name = item.get("name")
            pop = item.get("population")
            if not name or pop is None:
                continue  # skip invalid data

            cap = item.get("capital")
            region = item.get("region")
            flag = item.get("flag")
            currs = item.get("currencies") or []

            if len(currs) == 0:
                # No currency info
                data = {
                    "name": name,
                    "capital": cap,
                    "region": region,
                    "population": int(pop),
                    "currency_code": None,
                    "exchange_rate": None,
                    "estimated_gdp": 0.0,
                    "flag_url": flag,
                }
            else:
                code = (currs[0] or {}).get("code")
                rate = rates.get(code) if code else None
                if code and rate is not None:
                    gdp = _compute_gdp(int(pop), float(rate))
                    data = {
                        "name": name,
                        "capital": cap,
                        "region": region,
                        "population": int(pop),
                        "currency_code": code,
                        "exchange_rate": float(rate),
                        "estimated_gdp": float(gdp) if gdp else None,
                        "flag_url": flag,
                    }
                else:
                    # Currency not in exchange table
                    data = {
                        "name": name,
                        "capital": cap,
                        "region": region,
                        "population": int(pop),
                        "currency_code": code,
                        "exchange_rate": None,
                        "estimated_gdp": None,
                        "flag_url": flag,
                    }

            upsert_country(db, data)

        # Update refresh timestamp
        iso_now = datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
        set_last_refresh(db, iso_now)
        db.commit()
    except Exception:
        db.rollback()
        raise

    # Generate summary image (non-critical)
    try:
        generate_summary_image(db)
    except Exception:
        pass
