# Handles reading configuration from environment variables or .env file

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_PORT: int = 8000
    DB_DIALECT: str = "mysql"  # mysql | sqlite
    DB_HOST: str = "127.0.0.1"
    DB_PORT: int = 3306
    DB_USER: str = "root"
    DB_PASS: str = "pass"
    DB_NAME: str = "country_cache"
    LOG_LEVEL: str = "info"

    class Config:
        env_file = ".env"  # tells Pydantic to load values from .env

# instantiate settings object
settings = Settings()
