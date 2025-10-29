# src/settings.py
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Fallbacks (used only if Railway vars are missing)
    APP_PORT: int = 8000
    DB_DIALECT: str = "mysql"  # mysql | sqlite
    DB_HOST: str = "127.0.0.1"
    DB_PORT: int = 3306
    DB_USER: str = "root"
    DB_PASS: str = "pass"
    DB_NAME: str = "country_cache"
    LOG_LEVEL: str = "info"

    def sqlalchemy_uri(self) -> str:
        # Prefer Railway-provided URLs
        url = (
            os.getenv("DATABASE_URL")
            or os.getenv("RAILWAY_DATABASE_URL")
            or os.getenv("MYSQL_URL")            # sometimes present
            or os.getenv("MYSQL_PUBLIC_URL")     # rarely needed in same project
        )
        if url:
            return url.replace("mysql://", "mysql+pymysql://", 1)

        # Fall back to raw MYSQL* vars (from linked MySQL service)
        mh = os.getenv("MYSQLHOST")
        if mh:
            user = os.getenv("MYSQLUSER")
            pwd  = os.getenv("MYSQLPASSWORD")
            db   = os.getenv("MYSQLDATABASE")
            port = os.getenv("MYSQLPORT", "3306")
            return f"mysql+pymysql://{user}:{pwd}@{mh}:{port}/{db}"

        # Final fallback: your custom DB_* (e.g., local dev)
        if self.DB_DIALECT.lower() == "sqlite":
            return f"sqlite:///./{self.DB_NAME}"
        return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    class Config:
        env_file = ".env"

settings = Settings()
