import os
from pathlib import Path
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


def init_db():
    """Initialize database schema and run SQL migrations.

    This function keeps the existing SQLAlchemy model-based creation
    (useful for dev) and, in addition, executes any .sql files found in
    the project-level `migrations/` folder. The SQL scripts are written
    to be idempotentes (create table if not exists, on conflict do nothing,
    drop trigger if exists, etc), então é seguro executar em todo startup.
    """
    from . import models  # noqa: F401 - ensure models are imported for metadata

    # 1) Cria objetos do SQLAlchemy (tabelas definidas em models.py)
    Base.metadata.create_all(bind=engine)

    # 2) Executa migrations em SQL puro (se existirem)
    try:
        project_root = Path(__file__).resolve().parent.parent
        migrations_dir = project_root / "migrations"
        if migrations_dir.exists() and migrations_dir.is_dir():
            sql_files = sorted(migrations_dir.glob("*.sql"))
            if sql_files:
                # Usa conexão bruta para permitir múltiplos statements por arquivo
                raw_conn = engine.raw_connection()
                try:
                    raw_conn.autocommit = True
                    cur = raw_conn.cursor()
                    for sql_path in sql_files:
                        with sql_path.open("r", encoding="utf-8") as f:
                            script = f.read()
                        # Executa o script completo; os .sql foram escritos para serem idempotentes
                        cur.execute(script)
                    cur.close()
                finally:
                    raw_conn.close()
    except Exception as e:
        # Em ambiente de dev, um print ajuda a diagnosticar; em prod use logging
        print(f"[DB] Falha ao executar migrations SQL: {e}")
