# src/settings.py
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Prefer a single DATABASE_URL (Railway injects DATABASE_URL / RAILWAY_DATABASE_URL / MYSQL_URL).
    Fall back to split MYSQL* parts if needed. Last resort: local sqlite so app still boots.
    """

    def sqlalchemy_uri(self) -> str:
        # 1) One-shot URLs that Railway provides
        url = (
            os.getenv("DATABASE_URL")
            or os.getenv("RAILWAY_DATABASE_URL")
            or os.getenv("MYSQL_URL")
            or os.getenv("MYSQL_PUBLIC_URL")
        )
        if url:
            # ensure PyMySQL driver
            return url.replace("mysql://", "mysql+pymysql://", 1)

        # 2) Split MYSQL* parts (also provided by Railway)
        host = os.getenv("MYSQLHOST")
        user = os.getenv("MYSQLUSER")
        pwd  = os.getenv("MYSQLPASSWORD")
        db   = os.getenv("MYSQLDATABASE")
        port = os.getenv("MYSQLPORT", "3306")
        if host and user and pwd and db:
            return f"mysql+pymysql://{user}:{pwd}@{host}:{port}/{db}"

        # 3) Final fallback for local dev (no Railway vars present)
        return "sqlite:///./data.db"

    class Config:
        env_file = ".env"

settings = Settings()
