# Sets up SQLAlchemy connection engine + session factory

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .settings import settings

# Choose DB type based on .env
dialect = settings.DB_DIALECT.lower().strip()

if dialect == "sqlite":
    # SQLite for local quick testing
    DB_URL = f"sqlite:///./{settings.DB_NAME}"
    engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
elif dialect == "mysql":
    # MySQL using PyMySQL driver
    DB_URL = f"mysql+pymysql://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
    engine = create_engine(DB_URL, pool_pre_ping=True, pool_recycle=3600, echo=False)
else:
    raise RuntimeError(f"Unsupported DB_DIALECT: {settings.DB_DIALECT}")

# Session factory
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Declarative Base for model inheritance
Base = declarative_base()

# Dependency to get DB session per request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
