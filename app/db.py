import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


def _build_database_url_from_env():
    user = os.getenv("DB_USER") or os.getenv("POSTGRES_USER") or "postgres"
    password = os.getenv("DB_PASS") or os.getenv("POSTGRES_PASSWORD") or "postgres"
    host = os.getenv("DB_HOST") or os.getenv("DB") or "localhost"
    port = os.getenv("DB_PORT") or os.getenv("POSTGRES_PORT") or "5432"
    db = os.getenv("DB_NAME") or os.getenv("POSTGRES_DB") or "postgres"
    return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"


DATABASE_URL = os.getenv("DATABASE_URL") or _build_database_url_from_env()

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
